# 1: pip install paddlepaddle-gpu==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
# 2: pip install paddleocr[all] pandas ollama pydantic
import glob
import os
from paddleocr import PPStructureV3
from time import gmtime, strftime
from typing import List
from llm_ollama import extract_courses
# FIXME: correct paths as in example
IMAGES = "/data/images"
OUTPUT = "/data/output/PPSTRUCTUREv3"
LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

image_paths = glob.glob(f"{IMAGES}/*.jpg")
    
# TODO: using max settings, decide whether to use these or to find a common ground with others
paddleocr = PPStructureV3(
    lang="en",
    device="gpu",
    ocr_version="PP-OCRv5",
    layout_detection_model_name=,
    chart_recognition_model_name=,
    region_detection_model_name=,
    doc_orientation_classify_model_name=,
    doc_unwarping_model_name=,
    text_detection_model_name=,
    textline_orientation_model_name=,
    text_recognition_model_name=,
    table_classification_model_name=,
    table_orientation_classify_model_name=,
    table_orientation_classify_model_name=
    use_doc_orientation_classify=True,
        use_doc_unwarping=None,
        use_textline_orientation=None,
        use_seal_recognition=None,
        use_table_recognition=None,
        use_formula_recognition=None,
        use_chart_recognition=None,
        use_region_detection=None,
        format_block_content=None,
        markdown_ignore_labels=None,
)

PaddleOCR(
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
    use_textline_orientation=True
)

# run OCR over all images, use structure from PPStructureV3
text_dict = {}
for image in image_paths:
    image_name = os.path.basename(image)  #FIXME: fix to proper name extraction -> "2_25"
    result = paddleocr.predict(image)

    text_dict[image_name] = text

# extract relevant entries with each ollama model
for llm_model in LLMS: 
    print(f"LLM: {llm_model} start. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    params = llm_model.split(":")[1]
    for name, text in text_dict.items(): 
        df = extract_courses(text, llm_model)
        df.to_csv(f"{OUTPUT}/{params}/{name}.csv")
    print(f"LLM: {llm_model} done. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
