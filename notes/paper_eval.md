# Evaluation methods of papers dealing with similar problems

## 1. Figure Text Extraction in Biomedical Literature
> **Metadata**
> 	**Link:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0015338
> 	**published in:** PLOS One

- extraction from text out of figures in biomedical papers
- evaluation of an off-the-shelf OCR tool + development of a figure text extraction tool based on said OCR (image preprocessing, char recognition, text correction)
- using precision, recall and f1 to evaluate text localization and (figure) text extraction
- Data/Gold Standard: Figures from PubMed Central, transcribed manually, then measured with an agreement between two transcribers

- Evaluation:
	- ignored numbers and special symbols (+, -, @, #, % etc.)
	- strict: only correct if each character sequence matched gold standard
	- **Precision:** number of correctly recognized words / number of recognized words
	- **Recall:** number of correctly retrieved words / number of transcribed figure texts in figures
	- **F1**: harmonic mean

## 2. Information extraction from scientific articles: a survey
> **Metadata**
> 	**Link:** https://link.springer.com/article/10.1007/s11192-018-2921-5
> 	**published in:** Springer Nature

- extraction of certain relevant insights from papers out of ACM and IEEE
- "Evaluation of an IE system is usually performed by means of comparing the extracted information with the respective gold standard data-set." (S.7)
- uses Precision, Recall, F-measure
- Precision: "focuses on evaluating how many of the extracted information is correct" (S.7)
- Recall: "focused on evaluating that how much of the correct information is extracted" (S.7)
- evaluates individual fields: Title, Author, Abstract... + Avg.

## 3. A Benchmark and Evaluation for Text Extraction from PDF
> **Metadata**
> 	**Link:** https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7991564
> 	**published in:** IEEE Xplore

- creating ground truth by parsing LaTeX of scientific papers for arxiv
- not using basic metrics but instead having a look at differences in newlines, paragraphs and word differences by count giving a % amount of difference to the gold standard/ground truth

## 4. PaddleOCR 3.0 Technical Report
> **Metadata**
> 	**Link:** https://arxiv.org/abs/2507.05595
> 	**published in:** arxiv

- test of own models using known PDF-Datasets and selfmade private datasets covering different scenarios
- annotations of those are the ground truth
- evaluation via 1-EditDistance 

## 5.  A Comparative Study of PDF Parsing Tools Across Diverse Document Categories
> **Metadata**
> 	**Link:** https://arxiv.org/abs/2410.09871
> 	**published in:** arxiv

- benchmark of PDF parsing tools using different data-sources
- using annotiations in JSON by unwrapping those in python and turning them into formatted strings as ground truth
- evaluation split for text and table extraction
- text extract eval: F1 Score using Levenshtein Similarity, BLEU, Local Alignment
- table extract eval: Intersection over Union to compare similarity between tables using Jaccard Similarity (S.7)
