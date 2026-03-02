# Related Work
## First Selection
1: https://ijeret.org/index.php/ijeret/article/view/273

2: https://www.mdpi.com/2076-3417/10/21/7640

3: https://link.springer.com/article/10.1007/s11192-018-2921-5

4: https://arxiv.org/abs/2410.09871

5: https://ieeexplore.ieee.org/abstract/document/11004392

6: https://arxiv.org/abs/2501.02189

7: https://ieeexplore.ieee.org/abstract/document/10769058

8: https://oulurepo.oulu.fi/handle/10024/56750

9: https://aclanthology.org/2025.acl-long.57/

10: https://aclanthology.org/2025.xllm-1.2/

11: https://arxiv.org/abs/2510.27119

12: https://arxiv.org/abs/2602.14743

13: https://proceedings.neurips.cc/paper_files/paper/2024/hash/d0718553fd6b227a353c6432cf893285-Abstract-Datasets_and_Benchmarks_Track.html

14: https://pmc.ncbi.nlm.nih.gov/articles/PMC11751965/

15: https://arxiv.org/abs/2310.05092

### 1

- shady journal
- no benchmark

### 2

- is about machine reading comprehension 

### 3

- about information extraction from scientific articles (pre age of AI)

### 4

- explores PDF Parsing tools

### 5

- benchmark of OCR tools

### 6

- survey on VLMs: architecture, summary and categorization of benchmarks

### 7

- benchmark on VLMs

### 8

- (website didn't work)

### 9

- benchmark on VLMs for different tasks

### 10

- benchmark of table extraction with OCR vs VLMs/Multimodal LLMs
- also uses pydantic schema!

### 11

- benchmark of unstructured data into structured formats

### 12

- benchmark for structured data extraction

### 13

- automated image to struct extract benchmark (image of webpage, generation of html, comparing of images)

### 14

- evaluation of LLM extraction from unstructured documents

### 15

- benchmark for fine grained information extraction using LLMs

---

## Selection for related work:

documents to machine readable format/PDF Parsing: 5, 10

extracting relevant information: 14, 15

structured output: 12, 13

--- 

### 5 - Khan

- OCR Benchmark
- using CBC Reports Dataset
- measure time needed, accuracy, errors
- PaddleOCR and EasyOCR showing the best results, with PaddleOCR being far better than EasyOCR though
- -> results of this benchmark influenced selection of OCR models choosen for this benchmark

### 10 - Nunes

> this paper has some nice reference for how to include hardware!

- benchmarks OCR and MMLLMs in their ability to extract tables from images
- probably the closest to the benchmark in this paper, missing the extraction step, still holding valuable information to build upon
- prompting LLMs with a given pydantic schema to force a structured output as was done in this benchmark aswell
- using selection of non complex tables out of the the PubTables-1M dataset for testdata
- using both propietary and free models, with candidates of both being able to perform exceedingly well F1 of 85+ to 95+ depending on the aspect of measurement 

### 14 - Ntinopulos

- LLM and table transformer benchmark for information extraction out of unstructured and semi structured health records, most of those proprietary
- zero-shot setting, evaluating based on entity extraction and binary classification tasks
- proprietary models showing good to really good results (> 0.9 F1 Score) over multiple same-prompt iterations, while especially some of the free model struggled to extract well
- table transformer TATR outperforms LLms when only structural layout is considereed, once content of cells is of importance LLMs beat combination of table transformer and OCR

### 15 - Gao

- evaluates fine grained extraction with multiple types of information 
- checking on ability of LLMs to generalize to unseen task form and information types
- encoder-decoder architecture generalizes better to unseen information types while decoder only architecture performs better for unseen task forms
- also indicates that performance is not always proportional scale/amount of parameters of a model
- overall promising but not exceedingly well results, no model achieves avg F1 values of 60 or above

### 12 - Tenckhoff

- benchmarks LLM capability to extract structured data and generate valid JSON from natural-language text
- evalutes 22 models across five prompting strategies
- dataset is synthetically generated
- exclusive focus on open.source LLMs with proprietary GPT-4o as a point of reference 
- "While GPT-4o was added as a closed-weight reference, it did not exhibit a clear advantage over the best open-source models (e.g. Gemma3 - 27B), reinforcing the practical competitiveness of deployable open systems." (quote from conclusion)
- apart from that its been shown that prompting strategy aswell as the model architecture are at least as important as the model scale in terms of JSON parsing tasks, once again underlying the narrative that size does not need to correlate with performance

### 13 - Roberts

- benchmark of VLMs capabilities to extracting structure from images with the speciality of not needing human judgement and therefor being a fully automatic benchmark-system
- done by prompting the VLM to output ie HTML or LaTeX code, which then is rendered and overlayed with the original image to produce a similarity score
- using webpages, LaTeX documents and sheet music as input data out of difference sources
- both closed APi models and open-weight models are being tested with closed-weight outperfoming those open-weight ones significantly, GPT-4 Omni being the best performing VLM for most categories (ie webpages and latex, but not sheet music)
- VLMs struggle to pick up visual nuances and are sensitive to prompts, hinting that adaption methods for generating prompts may work better than standardizeed zero-shot prompting
