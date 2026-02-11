# Script that evaluates the similarity of the .csv output of any tested model and the ground-truth .csv using data science typical metrics.
import glob
import os
import pandas as pd 
from sklearn.metrics import precision_score, recall_score, f1_score, jaccard_score

OUTPUT_FOLDER = "data/output"
GROUND_TRUTH_PATHS = {
    os.path.basename(path): path 
    for path in glob.glob("data/ground_truth/*.csv")
}
OCR = ["docTR", "EasyOCR", "MinerU", "PPOCRv5", "PPStructureV3", "Pytesseract"]
OCR_PARAMS = ["0.6b", "4b", "14b", "32b", "235b"]
# name: path
VLM = {
    "Gemma 3": "gemma3_27b",
    "LLava": "llava_7b",
    "Ministral 3": "ministral-3_14b",
    "Qwen2.5-VL": "qwen2.5vl_32b",
    "Qwen3-VL": "qwen3-vl_32b"
}

# set output floating point format
pd.options.display.float_format = '{:.3f}'.format

## -- helper functions -- 
# normalize (with the goal to evaluate if all the correct data has been extracted, NOT to evaluate if stuff like capitalization is correct!) 
def normalize_df(df, columns_to_drop):
    # drop index column/unnamed columns
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    # strip leading/trailing spaces
    for col in ['academic_field', 'course_name', 'grade', 'awarded_credits']:
        df[col] = df[col].astype(str).str.strip()    
    # academic_field and course_name to lowercase
    df['academic_field'] = df['academic_field'].str.lower()
    df['course_name'] = df['course_name'].str.lower()
    # if None was sent as a String it hasn't been replaced with "N/A" like `None` yet (check `llm/vlm_ollama.py`)
    df['grade'] = df['grade'].replace("None", "N/A")
    df['awarded_credits'] = df['awarded_credits'].replace("None", "N/A")
    # normalize possibly numerical values to floats, if NaN, just use the (lowercase) string
    df['grade'] = df['grade'].apply(normalize_number)
    df['awarded_credits'] = df['awarded_credits'].apply(normalize_number)
    df = df.drop(columns=columns_to_drop)
    return df

def normalize_number(x):
    # grade: numeric -> float, letter -> lowercase
    try:
        return float(x)
    except (ValueError, TypeError):
        return str(x).lower()
    
def create_evaluation(df_gt, df_output):
    # create tokens out of dataframes
    #  -> a token is one row for academic_field, course_name, grade and awarded_credits
    gt_token = set(df_gt.itertuples(index=False, name=None))
    output_token = set(df_output.itertuples(index=False, name=None))
    all_token = list(gt_token | output_token)

    if len(all_token) == 0:
        return {
            "Precision": 0,
            "Recall": 0,
            "F1": 0,
            "Jaccard": 0
        }
    
    y_true = [1 if row in gt_token else 0 for row in all_token]
    y_pred = [1 if row in output_token else 0 for row in all_token] 
    # TP: y_true[i] == 1, y_pred[i] == 1
    # FP: y_true[i] == 0, y_pred[i] == 1
    # FN: y_true[i] == 1, y_pred[i] == 0
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    jc = jaccard_score(y_true, y_pred, zero_division=0)
    return {
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Jaccard": jc
    }

# -- main program --
eval_configs = {
    "all": {
        "exclude_cols": []
    },
    "only_courses": {
        "exclude_cols": ["academic_field", "grade", "awarded_credits"]
    },
    "no_credits": {
        "exclude_cols": ["awarded_credits"]
    },
    "no_grades": {
        "exclude_cols": ["grade"]
    }
}

results_storage = {name: [] for name in eval_configs.keys()}

# EVAL OCR
for ocr_engine in OCR:
    for params in OCR_PARAMS:
        # "output" means the LLMs/VLMs output
        output_paths = {
            os.path.basename(path): path 
            for path in glob.glob(f"{OUTPUT_FOLDER}/{ocr_engine}/{params}/*.csv")
        }
        param_results = {name: [] for name in eval_configs.keys()}
        for file_name in GROUND_TRUTH_PATHS.keys():
            for name, config in eval_configs.items():
                # create normalized dataframe out of csv
                df_gt = normalize_df(pd.read_csv(GROUND_TRUTH_PATHS[file_name]), config["exclude_cols"])
                df_output = normalize_df(pd.read_csv(output_paths[file_name]), config["exclude_cols"])
                # run evaluation (Precision, Recall, F1, Jaccard)
                results = create_evaluation(df_gt, df_output)
                param_results[name].append(results)

        # calculate mean values
        for name in eval_configs.keys():
            tmp_df = pd.DataFrame(param_results[name])
            mean_results = {
                "Eval Config": name,
                "OCR Engine": ocr_engine,
                "Model": f"Qwen3:{params}",
                "Precision": tmp_df["Precision"].mean(),
                "Recall": tmp_df["Recall"].mean(),
                "F1": tmp_df["F1"].mean(),
                "Jaccard": tmp_df["Jaccard"].mean()
            }
            results_storage[name].append(mean_results)

# EVAL VLM
for vlm_name, vlm_dir_name in VLM.items():
    # "output" means the LLMs/VLMs output
    output_paths = {
        os.path.basename(path): path 
        for path in glob.glob(f"{OUTPUT_FOLDER}/{vlm_dir_name}/*.csv")
    }
    param_results = {name: [] for name in eval_configs.keys()}
    for file_name in GROUND_TRUTH_PATHS.keys():
        for name, config in eval_configs.items():
            # create normalized dataframe out of csv
            df_gt = normalize_df(pd.read_csv(GROUND_TRUTH_PATHS[file_name]), config["exclude_cols"])
            df_output = normalize_df(pd.read_csv(output_paths[file_name]), config["exclude_cols"]) 
            # run evaluation (Precision, Recall, F1, Jaccard)
            results = create_evaluation(df_gt, df_output)
            param_results[name].append(results)
        
    # calculate mean values
    for name in eval_configs.keys():
        tmp_df = pd.DataFrame(param_results[name])
        mean_results = {
            "Eval Config": name,
            "OCR Engine": "N/A",
            "Model": f"{vlm_name}",
            "Precision": tmp_df["Precision"].mean(),
            "Recall": tmp_df["Recall"].mean(),
            "F1": tmp_df["F1"].mean(),
            "Jaccard": tmp_df["Jaccard"].mean()
        }
        results_storage[name].append(mean_results)

result_df = pd.DataFrame(columns=["Eval Config", "OCR Engine", "Model", "Precision", "Recall", "F1", "Jaccard"])
for entry in results_storage.values():
    result_df = pd.concat([result_df, pd.DataFrame(entry)], ignore_index=True)

print(result_df)
result_df.to_json("data/benchmark_results.json")
