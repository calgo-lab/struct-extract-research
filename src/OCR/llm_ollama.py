import json
import pandas as pd
from ollama import chat, ChatResponse
from pydantic import BaseModel
from typing import  List, Literal

class Course(BaseModel):
    academic_field: Literal["Computer Science", "Mathematics"]
    course_name: str
    grade: float
    awarded_credits: float

class Courses(BaseModel):
    courses: List[Course]

# TODO: Optimize prompt, +determine one specific type of "N/A"
def extract_courses(text, llm_model) -> pd.DataFrame:
    response: ChatResponse = chat(
        model=llm_model,
        messages=[
            {
                "role": "user",
                "content": f"""
                    You are given the OCR result of a scanned page 
                    1. Determine if it is an academic record or transcript showing a single student's grades and/or earned credits. 
                    2. If yes, identify all courses whose subject matter falls under the academic fields of "Computer Science" or "Mathematics" — this includes courses that are clearly related even if the document does not use those exact headings. Use your judgment to classify them based on their titles, descriptions, or course codes. 
                    Extract those using the following schema for a course:
                    ```python
                    class Course(BaseModel):
                    academic_field: Literal["Computer Science", "Mathematics"]
                    course_name: str
                    grade: float
                    awarded_credits: float
                    ```
                    3. If it is not an academic record or transcript, return no results.
                    Here is the OCR result: 
                    {text}
                """
            }
        ],
        format=Courses.model_json_schema()
    )

    data = json.loads(response["message"]["content"])
    df = pd.DataFrame(data["courses"])
    return df
