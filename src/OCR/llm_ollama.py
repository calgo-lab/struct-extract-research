import json
import pandas as pd
from ollama import generate, GenerateResponse
from pydantic import BaseModel
from typing import  List, Literal

class Course(BaseModel):
    academic_field: Literal["Computer Science", "Mathematics"]
    course_name: str
    grade: float | str | None = None
    awarded_credits: float | None = None
class Courses(BaseModel):
    courses: List[Course]

def extract_courses(text, llm_model) -> pd.DataFrame:
    response: GenerateResponse = generate(
        model=llm_model,
        prompt=f"""
                # Goal
                You will be given the OCR result of a document likely to be a students transcript of completed courses eventually with additional information like earned credits or accomplished grades for each course.
                Your goal is to figure out whether the OCR result is such a students transcript and in case that it is extract each course name whose field of study falls within either Computer Science or Mathematics.
                If information like credits or grades are given for a course, it is also your goal to extract those.
                Return everything as a single JSON following the Pydantic Schema `Courses(BaseModel)` I am about to show and explain to you.

                # Schema
                --- BEGIN SCHEMA ---
                ```python
                class Course(BaseModel):
                    academic_field: Literal["Computer Science", "Mathematics"]
                    course_name: str
                    grade: float | str | None = None
                    awarded_credits: float | None = None
                class Courses(BaseModel):
                    courses: List[Course]
                ```
                --- END SCHEMA ---
                    
                ## Field Definitions of Schema
                The Schema is made up out of two BaseModels - Course and Courses. Courses defines a list of Course BaseModels. 
                Each `Course(BaseModel)` has four fields:
                    1. academic_field: This field can either be "Computer Science" or "Mathematics" depending on whether each extracted course better fits Computer Science or Mathematics. 
                    2. course_name: The name of that course as a string. Something like "Linear Algebra", "Operating Systems", "Programming I Lab".
                    3. grade: The grade the student acquired for each Course, only if given in the OCR result. Can be a string if its a letter like "A" or "BB+" or a numerical value like a score or grade "15", "2.3". If not given default to the python value `None`. 
                    4. awarded_credits: The credits the student was awarded for taking the course. Always a number; therefore, only the numerical type float ist defined.  If not given default to the python value `None`. 
                It is important that each Course object always holds all four fields, even if "grade" and "awarded_credits" are only filled with `None` due to no fitting value being present.

                ## Example-Outputs
                Following are a couple example JSON-outputs following the schema. Be aware that those are to show different cases and their outputs. Only use values which are in the actually given OCR result for your output.:
                    1. Two examples where all informations where given in the OCR result:
                        `{{'courses': [{{'academic_field': 'Computer Science', 'course_name': 'Web Technologies', 'grade': 'B', 'awarded_credits': 5}}, {{'academic_field': 'Mathematics', 'course_name': 'Linear Algebra', 'grade': 'D', 'awarded_credits': 2}}]}}`
                        `{{'courses': [{{'academic_field': 'Computer Science', 'course_name': 'Operating Systems', 'grade': 2.0, 'awarded_credits': 15}}, {{'academic_field': 'Computer Science', 'course_name': 'Programming Fun in Python', 'grade': 1.0, 'awarded_credits': 9}}]}}`
                    2. Example where no credits where mentioned in the OCR result:
                        `{{'courses': [{{'academic_field': 'Mathematics', 'course_name': 'Differential Equations & Linear Algebra', 'grade': 'A++', 'awarded_credits': 'None'}}]}}`
                    3. Example which was no transcript or had no courses fitting "Mathematics" or "Computer Science":
                        `{{'courses': []}}`

                # Rules 
                - Extract every course that, when considered independently, can either be categorized under "Computer Science" or "Mathematics". 
                    - "Computer Science" includes every course that directly or indirectly is about Computers: Programming, Operating Systems, Python Lab. Do not confuse Computer Science and general Engineering
                    - "Mathematics" includes every course that directly or indirectly is about basics of or a field in Mathmatics: Mathematics for Programmers, Linear Algebra, Statistics. 
                  Use your own judgement.
                - While you may use judgment to handle OCR noise during classification if a transcript is given or if a course may fall under the given definition, extract every piece of information exactly as given in the OCR result. Do not fix any typos for the output and keep capitalization as is. Be very strict about this!
                    - You are allowed to remove text if it is not part of i.e. the course name but stands right next to it.
                - If a document has multiple languages, prioritize the English designations.
                - If multiple types of credits are denominated, use the ones commonly known as "ECTS". If no credits at all are mentioned, default to `None`.
                - If multiple types of grades are given for a course, prioritize letter-grades (only such like A, B+, CC, 0 not full words) over numerical grades. If no grades at all are mentioned, default to `None`.
                - After classification and extraction, return a JSON that follows the given Pydantic Schema. Do not add any comments before, inbetween or after. If the OCR result you got is no student transcript of any kind or there are no courses that fit the definition of Mathematics or Computer Science return an empty result.

                # OCR Result
                Here is the OCR result. Classify and extract as is explained.

                --- BEGIN OCR RESULT ---
                {text}
                --- END OCR RESULT ---

                # Output
                Before outputting, verify:
                    - Did I check if the OCR results represents any kind of student transcript?
                    - Did I extract each course that may fit under the given definitions of "Computer Science" and "Mathematics"?
                    - Did I use the right label ("Computer Science", "Mathematics") for each extracted course in academic_field?
                    - Did I check for credits and grades for each extracted course?
                    - Did I use `None` for every credit and grade cell that I could not find a value for in the extracted document?
                    - Did I follow all the rules explained in # Rules while doing my job?

                Return only valid JSON following the schema. No additional text before or after.
            """,
            options = {
                "temperature" : 0,
                "num_ctx": 8192  # to be safe
            },
            stream=False,
            format=Courses.model_json_schema()
    )
    try:
        data = json.loads(response["response"])
        df = pd.DataFrame(data["courses"])
        # if empty courses list was returned, create an empty df with column headers
        if df.empty:
            df = pd.DataFrame(columns=["academic_field", "course_name", "grade", "awarded_credits"])
        # fill empty cells (None) with "N/A"
        df['grade'] = df['grade'].fillna("N/A")
        df['awarded_credits'] = df['awarded_credits'].fillna("N/A")
    except Exception as e:
        # if answer is not following the structure, return empty df
        df = pd.DataFrame(columns=["academic_field", "course_name", "grade", "awarded_credits"])

    return df   
