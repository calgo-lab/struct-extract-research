import os
from llm_ollama import extract_courses
from pathlib import Path
from time import gmtime, strftime

OCR_NAMES = ["docTR", "EasyOCR", "MinerU", "PPOCRv5", "PPStructureV3", "Pytesseract"]  
OUTPUT = f"/data/output"
LLM = "qwen3:0.6b"  # TODO: change accordingly

for ocr_name in OCR_NAMES:
    ocr_output = f"{OUTPUT}/{ocr_name}"
    text_dict = {}
    text_path = Path(f"/data/output/{ocr_name}/text")
    # get all texts
    for path in text_path.glob("*.txt"):
        text_name = path.stem
        with path.open("r", encoding="utf-8") as f:
            text = f.read()
        text_dict[text_name] = text
    print(text_dict)  # check if that works!
    
    print(f"LLM: {LLM}; OCR: {ocr_name} start. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    params = LLM.split(":")[1]
    llm_output = f"{ocr_output}/{params}_rt"
    if not os.path.exists(llm_output):
        os.makedirs(llm_output)
    for name, text in text_dict.items(): 
        df = extract_courses(text, LLM)
        df.to_csv(f"{llm_output}/{name}.csv")
    print(f"LLM: {LLM}; OCR: {ocr_name} done. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    