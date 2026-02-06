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

*for this selection the most popular OCR-models under the tag `OCR` on Github aswell as some featured in recent papers have been chosen*

- [Pytesseract](https://github.com/madmaze/pytesseract)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
    - PP-OCRv5
    - PP-StructureV3
- [MinerU](https://github.com/opendatalab/MinerU)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [docTR](https://github.com/mindee/doctr)

*additionally frequently named OCR, that havent been part of the list yet but perfomed well in other papers or on GitHub*

- [MMOCR](https://github.com/open-mmlab/mmocr)  - hasn't been updated for a while, maybe don't use it
- [Umi-OCR](https://github.com/hiroi-sora/Umi-OCR) - not a model but software running on either Paddle or Rapid


### VLM

*popular VLMs on GitHub and Ollama*

- PaddleOCR-VL
- Gemma3 -27b (similar size for the others, if possible)

*additionally frequently named models, that havent been part of the list yet but perfomed well in other papers*

- DeepSeek-OCR -3b
- Qwen3-VL -32b
- Qwen2.5VL -32b
- Llava -34b
- Ministral-3 -14b

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
