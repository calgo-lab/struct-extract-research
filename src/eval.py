# Script that evaluates the similarity of the .csv output of any tested model and the ground-truth .csv using data science typical metrics.
import pandas as pd 
from sklearn.metrics import precision_score, recall_score, f1_score

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
# FIXME: check again if sets are the way to go - each row SHOULD only exist once, does it really though; is a check and notification if it doesnt enough?
# idea: use list for gt and delete elements if match exists while iterating through predictions! 
gt_rows = set(gt_df.itertuples(index=False, name=None))
pred_rows = set(output_df.itertuples(index=False, name=None))
all_rows = list(gt_rows | pred_rows)
y_true = [1 if row in gt_rows else 0 for row in all_rows]
y_pred = [1 if row in pred_rows else 0 for row in all_rows]

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
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
