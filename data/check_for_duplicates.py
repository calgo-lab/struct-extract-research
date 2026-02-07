# Script that checks if there are any duplicates in ground truth
# Background is to validate the usage of sets for evaluation purposes
import glob
import pandas as pd

eval_data_path = "data/eval"
eval_data = glob.glob(f"{eval_data_path}/*.csv")

dup_count = 0

for path in eval_data[:1]:
    df = pd.read_csv(path)
    for dup_bool in df.duplicated():
        if dup_bool == True:
            dup_count +=1 

print(f"Ground Trouth holds {dup_count} duplicate \"Token\" (rows).")
