# Evaluation

*Following is a plan on how the evaluation is going to happen - based on how its done in papers evaluate similar problems.*

---

## Input
- csv file with multiple columns, can contain strings* or numbers* - **ground truth**
- csv file with multiple columns (can differ from ground truth), can contain strings* or numbers* - **evaluee** 
- *strings: same values can happen in a column
- *numbers: same values can happen in a column

## Output
- some sort of value that gives information about how close the extracted result is at the ground truth in its entirety

---

## Evaluation Process
### 1. Normalization

*While most features are important, as we want to make sure documents have been extracted as-is (ie. with typos) certain aspects will be cleaned up beforehand, as they'd skew results without holding any real (semantical) information.*

    - strip leading and trailing whitespaces
    - strings to lowercase
    - normalize numbers to be floats with consistent decimal precision (based on highest precision between two datapoints)
    - use one consistent entry for "N/A" values

### 2. Evaluation 

*This aims to evaluate how well each option is in extracting **relevant** contents exactly as they are in the document. As the selection is usually done by LLM (which aren't deterministic), order of entries will be ignored.*

---
Evaluation generally will be done using metrics common in this field: Precision, Recall, F1 as used in [[Ref3](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0015338&type=printable)], [[Ref6](https://link.springer.com/article/10.1007/s11192-018-2921-5)], [[Ref12](https://arxiv.org/abs/2507.05595)], [[Ref13](https://arxiv.org/abs/2410.09871)].

For that extracted information will be compared with gold standard data-set [[Ref6](https://link.springer.com/article/10.1007/s11192-018-2921-5)]. As entries can (and do) occur multiple times in a column. A columnwise/entrywise comparison isn't as feasible. Instead an entire row made consisting of "academic_field","course_name", "grade" and "awarded_credits" will be treated as a single token for comparison. 

Following the definition as made in [[Ref6](https://link.springer.com/article/10.1007/s11192-018-2921-5)] for Precision and Recall

>Precision focuses on evaluating how many of the extracted information
is correct `TP / TP + FP`

>Recall, on the other hand, is focused on evaluating that how much of the correct
information is extracted `TP / TP + FN`

a True Positive (TP), False Positive (FP) and False Negative (NP) have to be defined.

These will be defined after the definition of those values by the Jaccard Similarity as is done in [[Ref13](https://arxiv.org/abs/2410.09871)]:

<blockquote>

J(A,B) = ∣A∪B∣ / ∣A∩B∣​ -> J(TP, FP, FN) = TP / (TP + FP + FN)

TP = values in both sets 

FP = values only in set A

FN = values only in set B

</blockquote>

which transfered to our problem is:
- **TP**: Token from extracted is exactly as-is in ground truth.
- **FP**: Token from extracted doesn't exist as-is in ground truth.
- **FN**: Token from ground trouth doesn't exist as-is in ground truth.

---

*In [[Ref18](https://arxiv.org/abs/2412.07626)] tables are also compared more literally. Tables are being transformed to HTML followed by calculating a Tree-Edit-Distance based Similarity (TEDS) aswell as Normalized Edit Distance. While also an option, its not as practical in measuring the explicit set goal of this benchmark. Therefor the focus will be on the standard IR metrics via Jaccard Similarity.*
