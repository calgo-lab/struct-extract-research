from paddleocr import PaddleOCR
from typing import List

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
    
# TODO: figure out what to use (models, features like img orientation, unwarping...) in the actual benchmark
# for setup-tests I'll use mobile-model variants without extra models
paddleocr = PaddleOCR(
    lang="en",
    device="gpu",
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="PP-OCRv5_mobile_rec"
)

result = paddleocr.predict("data/images/2_9.jpg")

# GET TEXT FROM RESULT
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
                
print(text)
