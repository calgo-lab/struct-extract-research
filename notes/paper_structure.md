# Structure

> In this MarkDown Document I go through the way similar research papers have been structured in order to determine a structure for my own.

## Own Points

**following is a list of Points I think are worth mentioning in my paper**
- Why this entire benchmark is useful
- Data specifications
- Models
    - what open source, of the shelf models did I use
    - how did I configure them
    - why only one LLM?
- Test setup
    - Models
        - what open source, of the shelf models did I use
        - how did I configure them
        - why only one LLM?
    - Prompt  
- Metrics
    - what Metrics
    - the "Token-System" I am using
- (Hardware) 
- Results
    - ...
- Conclusion of the benchmark

---

### [Assessing the quality of information extraction](https://arxiv.org/html/2404.04068v1#S3)
(Abstract) <- in any case, won't be listed for the other papers
- Introduction
- Related Work
- How is structure extracted (Schema) + How do LLMs work with those
- How is the benchmark set up (How does it work, What metrics)
- Results and Conclusion

### [Multi-Modal AI for Structured Data Extraction from Documents](https://ijeret.org/index.php/ijeret/article/view/273/260)
*journal is shady!*

- Introduction
- Problems that are tackled 
- Related Work
- How does their proposed tech work
- Benchmark setup and eval explanation
- Results, Conclusion, Future Work

### [Figure Text Extraction in Biomedical Literature](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0015338)
- Introduction (incl. related work)
- Methods/Inner workings of their proposal
- Eval metric explanation
- Results
- Discussion of results

### [A Survey on Machine Reading Comprehension—Tasks, Evaluation Metrics and Benchmark Datasets](https://www.mdpi.com/2076-3417/10/21/7640)
- Introduction (why, related works, motivation, outline)
- Tasks to be benchmarked
- Different test scenarios defined
- Eval metric definition
- Results
- Discussion of data
- Conlusiosn to each scenario and dataset

### [Informatione xtraction from scientific articles: a survey](https://link.springer.com/article/10.1007/s11192-018-2921-5)
- Introduction (why, related works)
- Methodology
- Eval Metrics
- Results and Discussion of different approaches
- Conclusions and future work

### [A Benchmark and Evaluation for Text Extraction from PDF](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=799156)
- Introduction
- Related Work
- Generation of ground truth/Methodololgy
- Eval of tools (which tools, benchmark setup, eval methods) <- no results!
- Results and Conclusion

### [A Comparative Study of PDF Parsing Tools Across Diverse Document Categories](https://arxiv.org/abs/2410.09871)
- Introduction
- Related Work
- Methodology (dataset used, outline for how ground truth was obtained)
- Evaluation (procedure and metrics)
- Tools used (which Parsers, each explained for a bit)
- Results (Tables, Plots)
- Discussion
- Conclusion and future work

### [OmniDocBench: Benchmarking Diverse PDF Document Parsing with Comprehensive Annotations](https://arxiv.org/abs/2412.07626)
- Introduction (why, what are the issues)
- Related Work
- VLM based doc extraction explained
- Dataset
- Eval Methodology (how was extracted, how did the matching work)
- Benchmark results and discussion
- Conclusion

### [Open-Source OCR Libraries: A Comprehensive Study for Low Resource Language](https://aclanthology.org/2024.icon-1.48/)
- Introduction
- Goal/Objective
- Related Works
- Methodology (Pre-Processing, Text detection etc, Evaluation metrics, Implementation, results)
- Discussion and Conclusion

### [KITAB-Bench: A Comprehensive Multi-Domain Benchmark for Arabic OCR and Document Understanding](https://aclanthology.org/2025.findings-acl.1135/)
- Introduction
- Related Work
- Data (what sets, statistics)
- Eval frameworks and metrics
- Experiment setup
- Results and discussion
- Conclusion
- Limitations and future directions

### [Benchmarking Performance Analysis of Optical Character Recognition Techniques](https://ieeexplore.ieee.org/abstract/document/11004392)
- Introduction
- Related Work
- Methodolog (data prep, ocr applications, measurements and metrics)
- results and discussion
- conclusion

### [Comparative Study of Different Optical Character Recognition Models on Handwritten and Printed Medical Reports](https://ieeexplore.ieee.org/abstract/document/10100213)
- Introduction
- Related Work
- Approach (goal of study, expierment setup)
- Models
- Dataset
- Results
- Conclusion

### [A Survey of State of the Art Large Vision Language Models: Alignment, Benchmark, Evaluations and Challenges](https://arxiv.org/abs/2501.02189)
- Introduction
- VLMs state
- Explanation of inner workings of VLM training
- Data
- Eval Metrics
- Challenges of VLMs
- Limitations

---

## Result 
- Abstract
- Introduction
    - Whats the current state (OCR, LLM, VLM)
    - What are we going to look at
- Related work
- Methodology
    - Goal
    - Data+Ground Truth Extraction
    - OCR+LLM based Extraction
    - VLM based Extraction
- Evaluation
    - Data preparation
    - Data "Tokenization"
    - Metrics
- Results (Tables, Plots and Evaluating)
- Conclusion
- References
(Appendix)
- Data Examples
- Hardware
- Prompts
