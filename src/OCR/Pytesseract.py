# 0: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
# 1: (sudo) apt install tesseract-ocr
# 2: pip install pytesseract pandas ollama pydantic
import glob
import os
import pytesseract
from llm_ollama import extract_courses
from PIL import Image
from time import gmtime, strftime

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    IMAGES = "/data/images"
    OUTPUT = "/data/output/Pytesseract"
else:
    print("Path /data/ not found, terminating program!")
    # keep for now, in case more local debugging is needed
    #os.environ["TESSDATA_PREFIX"] = r'C:/Program Files/Tesseract-OCR/tessdata'
    #pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    exit()

if not os.path.exists(f"{OUTPUT}/text"):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

image_paths = glob.glob(f"{IMAGES}/*.jpg")

text_dict = {}
for image in image_paths:
    image_name = os.path.basename(image).split(".")[0] 
    text = pytesseract.image_to_string(Image.open(image), lang="eng")
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
