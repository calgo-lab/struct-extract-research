# Script that evaluates the similarity of the .csv output of any tested model and the ground-truth .csv using data science typical metrics.
import pandas as pd 

output = "output/test.csv"
gt = "data/eval/2_9.csv"

# helper function
def normalize_number(x):
    # grade: numeric -> float, letter -> lowercase
    try:
        return float(x)
    except (ValueError, TypeError):
        return str(x).lower()
    
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
    # academic_field and course_name to lowercase
    df['academic_field'] = df['academic_field'].str.lower()
    df['course_name'] = df['course_name'].str.lower()
    # normalize possibly numerical values to floats, if NaN, just use the string
    df['grade'] = df['grade'].apply(normalize_number)
    df['awarded_credits'] = df['awarded_credits'].apply(normalize_number)
    # TODO: define and enforce default for N/A values
    df = df.fillna("N/A")  # temp filling of empty cells, doesn't take care of N/A placeholders
    # <CODE HERE>

# evaluate 
gt_set = set(gt_df.itertuples(index=False, name=None))
out_set = set(output_df.itertuples(index=False, name=None))
# TODO: check if this assignment makes sense
# tp: exact row exists in both ground truth and output
tp = len(gt_set & out_set)
# fp: row exists only in output
fp = len(out_set - gt_set)
# fn: row only exists in ground truth
fn = len(gt_set - out_set)

# precision/recall/f1, but if empty tp/fp/fn exist, use -1 for debugging #TODO: figure out what to actually do with those - what would a 0 from tp + fp actually mean?
precision = tp / (tp + fp) if (tp + fp) > 0 else -1
recall = tp / (tp + fn) if (tp + fn) > 0 else -1
f1 = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else -1

# pretty print results
results = {
    "Metric": [
        "Precision",
        "Recall",
        "F1"
    ],
    "Value": [
        precision,
        recall,
        f1
    ]
}

df = pd.DataFrame(results)
df["Value"] = df["Value"].map(lambda x: f"{x:.2f}")

print(df.to_string(index=False))

# TODO: if needed: add "detail-metrics" going over single rows/look where issues lay
# for example:
# gt_courses = set(zip(gt_df.academic_field, gt_df.course_name))
# out_courses = set(zip(output_df.academic_field, output_df.course_name))

# course_precision = len(gt_courses & out_courses) / len(out_courses)
# course_recall = len(gt_courses & out_courses) / len(gt_courses)
