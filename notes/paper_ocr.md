# OCR models frequently used or mentioned in recent research

## 1. Open-Source OCR Libraries: A Comprehensive Study for Low Resource Language
> **Metadata**
> 	**Link:** https://aclanthology.org/2024.icon-1.48.pdf
> 	**published in:** ACL Anthology

- using OCR for the Malayalam language by leveraging models used for languages such as english or french
- mentioned OCR: Tesseract OCR, Keras OCR, MMOCR, PaddleOCR, EasyOCR 
- top 3, english: Tesseract OCR, PaddleOCR; MMOCR
- only new for us: MMOCR, won't take that in though as it seems to not be actively developed anymore/up to date with current technological standards (??)


## 2. KITAB-Bench: A Comprehensive Multi-Domain Benchmark for Arabic OCR and Document Understanding
>**Metadata**
>	**Link:** https://aclanthology.org/2025.findings-acl.1135.pdf
>	**published in:** ACL Anthology

- specifies on extraction of arabic tests
- uses LLMs aswell for generation of data for visuals and tables (uses multiple - closed aswell as open)
- also uses VLMs along OCRs
- for OCR it uses: Tesseract, EasyOOCR, AzureOCR (last one is closed, so wont be used)

## 3. Benchmarking Performance Analysis of Optical Character Recognition Techniques
> **Metadata**
> 	**Link:** https://ieeexplore.ieee.org/abstract/document/11004392
> 	**published in:** IEEE

- benchmarks "widely used OCR engines"
- engines used: PaddleOCR, EasyOCR, Keras-OCR, Tesseract, OpenCV, PyMuPDF, DocTR
- based on CBC Reports Dataset (200 patient reports with different fonts etc.)
- evaluation via accuracy (Word Error Rate and Character Error Rate) and execution time
- top 3, most accurate: PaddleOCR, EasyOCR; docTR

## 4. # Comparative Study of Different Optical Character Recognition Models on Handwritten and Printed Medical Reports
> **Metadata**
> 	**Link:** https://ieeexplore.ieee.org/abstract/document/10100213
> 	**published in:** IEEE

- uses tesseract and propietary OCR engines, therefor not of further interest for us
