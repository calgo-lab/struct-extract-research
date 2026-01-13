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

# next up: figure out metrics to use
# define goals for that and then look up which metrics may fit best, likely to be precision/recall
