Following are selected settings used for the OCR models during instantiating. 

| OCR-MODEL     | INPUT-TYPE | PARAMETERS                                                                                                                            |
| ------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| docTR         | PDF        | pretrained=True, assume_straight_pages=False, straighten_pages=True, detect_language=True                                             |
| EasyOCR       | JPG        | lang=en                                                                                                                               |
| MinerU        | PDF        | lang=en, inline_formula_enable=True                                                                                                   |
| PPOCRv5       | JPG        | lang=en, use_doc_orientation_classify=True, use_doc_unwarping=True, use_textline_orientation=True                                     |
| PPStructureV3 | PDF        | lang=en, use_doc_orientation_classify=True, use_doc_unwarping=True, use_textline_orientation=True, use_table_recognition=True         |
| Pytesseract   | JPG        | lang=en                                                                                                                               |

English has been selected where possible or necessary. Additionally, if models or modes for the OCR engines were configurable, the best options as mentioned in the respective engine’s documentation were chosen.