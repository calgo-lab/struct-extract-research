# Research-Plan

## Goal
The goal is to create an extensive benchmark of multiple machine learning–based methods for extracting specified information from unstructured documents and representing it in a structured format. The benchmark will evaluate multiple standalone OCR models combined with an LLM for information extraction, as well as VLM-based models.

## Data
The evaluation dataset consists of 100 course transcripts from applications to the Master’s program “Data Science” at the Berliner Hochschule für Technik. From each transcript, all courses, corresponding grades, and earned credits (where indicated) have been extracted and recorded in CSV format.

Have a look at: OmniDocBench and PubTabNet

## Hardware
*w.i.p.*

## Models
### OCR

*for this selection the most popular OCR-models under the tag `OCR` on Github have been chosen*

- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
    - PP-OCRv5
    - PP-StructureV3
- [MinerU](https://github.com/opendatalab/MinerU)
- [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) 
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)

*additionally frequently named models, that havent been part of the list yet but perfomed well in other papers*

- [MMOCR](https://github.com/open-mmlab/mmocr)  - hasn't been updated for a while, maybe don't use it
- [docTR](https://github.com/mindee/doctr)

### VLM

*popular VLMs on GitHub and Ollama*

- PaddleOCR-VL
- Gemma3

*additionally frequently named models, that havent been part of the list yet but perfomed well in other papers*

- DeepSeek-OCR - check because of "OCR"-name
- Qwen3-VL
- Qwen2.5VL
- Llava
- Gemini3-flash-preview

### LLM

*only using one LLM, deciding for Qwen3 as it offers a lot of different sizes in Ollamas model zoo*
- Qwen3

    - 0.6b
    - 4b
    - 14b
    - 32b
    - 235b

## Evaluation
check `evaluation.md`

---