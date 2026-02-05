# 1: pip install easyocr pandas ollama pydantic
import easyocr
import glob
import os
from llm_ollama import extract_courses
from time import gmtime, strftime

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    IMAGES = "/data/images"
    OUTPUT = "/data/output/EasyOCR"
else:
    print("Path /data/ not found, terminating program!")
    exit()

if not os.path.exists(OUTPUT):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

image_paths = glob.glob(f"{IMAGES}/*.jpg")

# instantiate EasyOCR reader
reader = easyocr.Reader(lang_list=["en"], gpu=True)

# run OCR over all images
text_dict = {}
for image in image_paths:
    image_name = os.path.basename(image).split(".")[0] 
    result = reader.readtext(image=image, detail=0, paragraph=True)
    # TODO: decide if some formatting should be done, bounding boxes exist as they do in PPOCRv5
    text = ""
    for paragraph in result:
        text += paragraph.strip()
        text += '\t'

    with open(f"{OUTPUT}/text/{image_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)

    text_dict[image_name] = text

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
    