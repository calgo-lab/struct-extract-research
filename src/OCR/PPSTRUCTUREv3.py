# 1: pip install paddlepaddle-gpu==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
# 2: pip install paddleocr[all] pandas ollama pydantic
# 3: pip install opencv-python-headless==4.12.0.88 (because of a new opencv bug)
import glob
import os
from paddleocr import PPStructureV3
from time import gmtime, strftime
from llm_ollama import extract_courses

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    # using pdfs instead of images, due to ppstructure sometimes running into a numpy error with those
    PDFS = "/data/pdfs"  
    OUTPUT = "/data/output/PPSTRUCTUREv3"
else:
    print("Path /data/ not found, terminating program!")
    exit()

if not os.path.exists(OUTPUT):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

pdf_paths = glob.glob(f"{PDFS}/*.pdf")

# TODO: using same settings as with PaddleOCR, but added use_table_recognition, as we want to find out impact of structure of those
paddleocr = PPStructureV3(
    lang="en",
    device="gpu",
    ocr_version="PP-OCRv5",
    doc_orientation_classify_model_name="PP-LCNet_x1_0_doc_ori",
    doc_unwarping_model_name="UVDoc",
    text_detection_model_name="PP-OCRv5_server_det",
    textline_orientation_model_name="PP-LCNet_x1_0_textline_ori",
    text_recognition_model_name="PP-OCRv5_server_rec",
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True,
    use_table_recognition=True
)

# run OCR over all pdfs, use structure from PPStructureV3
text_dict = {}
for pdf in pdf_paths:
    pdf_name = os.path.basename(pdf).split(".")[0]
    result = paddleocr.predict(pdf)
    md_dict = result[0].markdown
    text = md_dict["markdown_texts"]
    with open(f"{OUTPUT}/text/{pdf_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)
    text_dict[pdf_name] = text

# extract relevant entries with each ollama model
for llm_model in LLMS: 
    print(f"LLM: {llm_model} start. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    params = llm_model.split(":")[1]
    if not os.path.exists(f"{OUTPUT}/{params}"):
        os.makedirs(f"{OUTPUT}/{params}")
    for name, text in text_dict.items(): 
        df = extract_courses(text, llm_model)
        df.to_csv(f"{OUTPUT}/{params}/{name}.csv")
    print(f"LLM: {llm_model} done. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
