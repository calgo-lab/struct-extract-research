import glob
import os
from llm_ollama import extract_courses
from time import gmtime, strftime

ocr_model_name = "EasyOCR"  # TODO: change accordingly
OUTPUT = f"/data/output/{ocr_model_name}"
LLM = "qwen3:235b"  # TODO: change accordingly

text_dict = {}
text_path = f"/data/output/{ocr_model_name}/text"
text_paths = glob.glob(f"{text_path}/*.txt")
for text in text_paths:
    text_name = os.path.basename(text).split(".")[0]
    print(text_name)
    text_dict[text_name] = text

print(f"LLM: {LLM} start. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
params = LLM.split(":")[1]
if not os.path.exists(f"{OUTPUT}/{params}_rt"):
    os.makedirs(f"{OUTPUT}/{params}")
for name, text in text_dict.items(): 
    df = extract_courses(text, LLM)
    df.to_csv(f"{OUTPUT}/{params}/{name}.csv")
print(f"LLM: {LLM} done. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    