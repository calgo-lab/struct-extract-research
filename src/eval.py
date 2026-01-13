# Script that evaluates the similarity of the .csv output of any tested model and the ground-truth .csv using data science typical metrics.
import pandas as pd 

output = "output/test.csv"
gt = "data/eval/2_9.csv"

# read in
output_df = pd.read_csv(output)
gt_df = pd.read_csv(gt)
df_list = [output_df, gt_df]

# normalize (with the goal to evaluate if all the correct data has been extracted, NOT to evaluate if stuff like capitalization is correct!) 
# TODO: check if thats okay
for df in df_list:
    # drop index column
    df.drop(df.columns[df.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    # strip leading/trailing spaces
    for col in ['academic_field', 'course_name', 'grade', 'awarded_credits']:
        df[col] = df[col].astype(str).str.strip()    
    # course_name to lowercase
    df['course_name'] = df['course_name'].str.lower()
    # grade: numeric -> float, letter -> lowercase
    df['grade'] = df['grade'].apply(
        lambda x: float(x) if pd.to_numeric(x, errors='coerce') is not None and str(x).replace('.', '', 1).isdigit()
        else x.lower()
    )
    # awarded_credits: numeric -> float, letter -> lowercase
    df['awarded_credits'] = df['awarded_credits'].apply(
        lambda x: float(x) if pd.to_numeric(x, errors='coerce') is not None and str(x).replace('.', '', 1).isdigit()
        else x.lower()
    )
    # TODO: define and enforce default for N/A values
    # <CODE HERE>

# 1. figure out if all courses have been recognized
# 2. check if coures names have been extracted correctly
#   - look if each value in course_name in ground truth is in extracted .csv
#   - increment respective found/not found counter
#   - calculate accuracy 
# 3. check if credits/grades have been extracted correctly
#   - if 2. is found check if those two are correct
#   - calculate accuracy only with using the courses that have been extracted correctly
#   - perhaps calc accuracy with total nr of courses

# think about how precision/recall would be possible (how to define TP, FP, FN, TN?)
# TODO: there could be duplicate courses, get all courses 
doesnt_exist_counter = 0
correct_credits = 0
correct_grade = 0
total_counter = len(output_df.course_name.values)
for gt_row in gt_df.itertuples():
    # iterate over all courses, get out all instances of the same course
    # TODO: figure out how to not add stuff double (if a course name exists twice, it would do +=2 twice - maybe with the doesnt exist counter?)
    matching_rows = []
    for output_row in output_df.itertuples():
        if gt_row.course_name == output_row.course_name:
            matching_rows.append(output_row)
    
    if len(matching_rows) != 0:
        # check if credits and grade match
        # use two for loops to avoid issues with doubled values
        # TODO: check if break is needed, check if two for loops are needed
        for matching_row in matching_rows:
            if gt_row.awarded_credits == matching_row.awarded_credits:
                correct_credits += 1
                break
        for matching_row in matching_rows:
            if gt_row.grade == matching_row.grade:
                correct_grade += 1
                break
    else:
        doesnt_exist_counter += 1

# calculate accuracy
accuracy_courses = (total_counter - doesnt_exist_counter) / total_counter
accuracy_credits_course = correct_credits / (total_counter - doesnt_exist_counter)
accuracy_credits_all = correct_credits / total_counter
accuracy_grade_course = correct_grade / (total_counter - doesnt_exist_counter)
accuracy_grade_all = correct_grade / total_counter

# pretty print results
results = {
    "Metric": [
        "Accuracy Courses",
        "Accuracy Credits (Correct Courses)",
        "Accuracy Credits (All)",
        "Accuracy Grades (Correct Courses)",
        "Accuracy Grades (All)"
    ],
    "Value": [
        accuracy_courses,
        accuracy_credits_course,
        accuracy_credits_all,
        accuracy_grade_course,
        accuracy_grade_all
    ]
}

df = pd.DataFrame(results)
df["Value"] = df["Value"].map(lambda x: f"{x:.2f}")

print(df.to_string(index=False))
