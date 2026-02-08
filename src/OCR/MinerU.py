# 1: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
# 2: pip install mineru[all] pandas ollama pydantic
# 3: pip install opencv-python-headless==4.12.0.88 (because of a new opencv bug)
import glob
import os
from mineru.backend.hybrid.hybrid_analyze import doc_analyze as hybrid_doc_analyze
from mineru.backend.vlm.vlm_middle_json_mkcontent import union_make as vlm_union_make
from mineru.cli.common import prepare_env, read_fn
from mineru.data.data_reader_writer import FileBasedDataWriter
from mineru.utils.enum_class import MakeMode
from llm_ollama import extract_courses
from time import gmtime, strftime

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    PDFS = "/data/pdfs"  
    OUTPUT = "/data/output/MinerU"
else:
    print("Path /data/ not found, terminating program!")
    exit()

if not os.path.exists(f"{OUTPUT}/text"):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

pdf_paths = glob.glob(f"{PDFS}/*.pdf")

text_dict = {}
# extraction based on https://github.com/opendatalab/MinerU/blob/master/demo/demo.py
for pdf in pdf_paths:
    pdf_name = os.path.basename(pdf).split(".")[0]
    pdf_bytes = read_fn(pdf)
    # create temporary output dirs
    local_image_dir, local_md_dir = prepare_env(OUTPUT, pdf_name, "hybrid_auto")
    image_writer = FileBasedDataWriter(local_image_dir)

    # run OCR
    middle_json, infer_result, _vlm_ocr_enable = hybrid_doc_analyze(
        pdf_bytes,
        image_writer=image_writer,
        parse_method="hybrid_auto",
        language="en",
        inline_formula_enable=True
    )

    # extract text from output as markdown (formatted)
    pdf_info = middle_json["pdf_info"]
    text = vlm_union_make(pdf_info, MakeMode.MM_MD)
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
    