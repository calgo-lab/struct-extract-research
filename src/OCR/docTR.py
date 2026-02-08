# 0: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
# 1: pip install python-doctr pandas ollama pydantic
# 3: pip install opencv-python-headless==4.12.0.88 (because of a new opencv bug)
import glob
import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from llm_ollama import extract_courses
from time import gmtime, strftime

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    PDFS = "/data/pdfs"  
    OUTPUT = "/data/output/docTR"
else:
    print("Path /data/ not found, terminating program!")
    exit()

if not os.path.exists(f"{OUTPUT}/text"):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

pdf_paths = glob.glob(f"{PDFS}/*.pdf")

text_dict = {}

for pdf in pdf_paths:
    pdf_name = os.path.basename(pdf).split(".")[0]
    # model choice based on: https://mindee.github.io/doctr/using_doctr/using_models.html
    model = (ocr_predictor(
        det_arch="db_resnet50",
        reco_arch="master", 
        pretrained=True,
        assume_straight_pages=False,
        straighten_pages=True,
        detect_language=True
    )).cuda()  # .cuda() is needed for GPU-usage
    result = model(DocumentFile.from_pdf(pdf))
    # plain text with linebreaks
    text = result.render()
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
