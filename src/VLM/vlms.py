# 1: pip install pandas ollama pydantic
import base64
import glob
import os
import subprocess
from pathlib import Path
from time import gmtime, strftime, sleep
from vlm_ollama import extract_courses

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    IMAGES = "/data/images"
    OUTPUT = "/data/output"
else:
    print("Path /data/ not found, terminating program!")
    exit()

# models and context sizes
VLMS = ["gemma3:27b", "ministral-3:14b", "llava:7b", "qwen2.5vl:32b", "qwen3-vl:32b"]

image_paths = glob.glob(f"{IMAGES}/*.jpg")

for vlm_model in VLMS:
    vlm_output = f"{OUTPUT}/{vlm_model.replace(':', '_')}_rt"
    print(f"Creating output folder at {vlm_output}.")
    os.makedirs(f"{vlm_output}", exist_ok=True)

    for i, image in enumerate(image_paths):
        image_name = os.path.basename(image).split(".")[0] 
        print(f"Image {i}: {image_name}; VLM: {vlm_model} - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
        # ollama expects a base64 encoded image string
        image_b64 = base64.b64encode(Path(image).read_bytes()).decode()
        df = extract_courses(image_b64, vlm_model)
        df.to_csv(f"{vlm_output}/{image_name}.csv")

    # end one model before starting the next
    subprocess.run(["ollama", "stop", f"{vlm_model}"])
    sleep(30)
