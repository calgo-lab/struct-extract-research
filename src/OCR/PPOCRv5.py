# 1: pip install paddlepaddle-gpu==3.3.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu126/
# 2: pip install paddleocr[all] pandas ollama pydantic
# 3: pip install opencv-python-headless==4.12.0.88 (because of a new opencv bug)
import glob
import os
from paddleocr import PaddleOCR
from time import gmtime, strftime
from typing import List
from llm_ollama import extract_courses

if os.path.exists("/data/images"):
    print("Path /data/... found.")
    IMAGES = "/data/images"
    OUTPUT = "/data/output/PPOCRv5"
else:
    print("Path /data/ not found, terminating program!")
    exit()

if not os.path.exists(OUTPUT):
    print(f"Creating output folder at {OUTPUT}.")
    os.makedirs(OUTPUT)
    os.makedirs(f"{OUTPUT}/text")

LLMS = ["qwen3:0.6b", "qwen3:4b", "qwen3:14b", "qwen3:32b", "qwen3:235b"]

image_paths = glob.glob(f"{IMAGES}/*.jpg")

class TextElement:
    """
    Simple class to define a Text-Element and its bounding box coordinates obtained by performing OCR using PP-OCRv5.
    """
    def __init__(self, text, top_left, bot_left, top_right, bot_right):
        self.text = text
        # Tuples; [0] = x-coordinate, [1] = y-coordinate
        self.top_left = top_left
        self.bot_left = bot_left
        self.top_right = top_right
        self.bot_right = bot_right
    
    def __repr__(self):
        return f"TextElement('{self.text}', with top left corner of bounding box at {self.top_left})"

# TODO: using max settings, decide whether to use these or to find a common ground with others
paddleocr = PaddleOCR(
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

# run OCR over all images, create basic structure for text
text_dict = {}
for image in image_paths:
    image_name = os.path.basename(image).split(".")[0] 
    result = paddleocr.predict(image)

    # get text from result
    text_elements: List[TextElement] = []
    ocr_item = result[0] 
    # for each recognized text element (each "box" in the visual output of the OCR result) extract text and coordinates
    for idx in range(len(result[0]["rec_polys"])):
        box_coords = ocr_item["rec_polys"][idx]
        text = ocr_item["rec_texts"][idx]

        if text.strip():  # if text not empty
            top_left = tuple(box_coords[0])
            bot_left = tuple(box_coords[3])
            top_right = tuple(box_coords[1])
            bot_right = tuple(box_coords[2])

            text_elements.append(TextElement(text,top_left, bot_left, top_right, bot_right))    
    # post-process to create formatted string
    text = ""
    for i, element in enumerate(text_elements):
        text += element.text.strip()

        if i + 1 >= len(text_elements):
            continue
        # TODO: decide if we want to add this layer of structure or if we want to keep each output "as raw as possible"
        # # check if next text is on similar height, if not -> \n
        # elif vertical_overlap_ratio(element, text_elements[i + 1]) <= 0.75:  # if needed, tweak ratio threshold
        #     text += '\n'
        # else:
        #     text += '\t' 
        text += '\t'

    with open(f"{OUTPUT}/text/{image_name}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(text)

    text_dict[image_name] = text

# extract relevant entries with each ollama model
for llm_model in LLMS: 
    print(f"LLM: {llm_model} start. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
    params = llm_model.split(":")[1]
    for name, text in text_dict.items(): 
        df = extract_courses(text, llm_model)
        df.to_csv(f"{OUTPUT}/{params}/{name}.csv")
    print(f"LLM: {llm_model} done. - {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")


# helper functions
# def __vertical_overlap_ratio(e1, e2):
#     """
#     Simple function to compute the ratio of vertical overlap of two bounding boxes. 
#     """
#     # get biggest possible vertical line of both boxes
#     top1 = min(e1.top_left[1], e1.top_right[1])
#     bot1 = max(e1.bot_left[1], e1.bot_right[1])
#     top2 = min(e2.top_left[1], e2.top_right[1])
#     bot2 = max(e2.bot_left[1], e2.bot_right[1])

#     # find intersection
#     overlap_top = max(top1, top2)
#     overlap_bot = min(bot1, bot2)
#     overlap_height = max(0, overlap_bot - overlap_top)

#     # find smallest height to normalize
#     height1 = bot1 - top1
#     height2 = bot2 - top2

#     min_height = min(height1, height2)
#     if min_height == 0:
#         return 0 
    
#     return overlap_height / min_height
