# src

This folder holds the code for all different implementations of models and methods that are to be tested.

Most will receive their own `requirements.txt` to allow for a "plug and play" style of swapping out different scripts when benchmarking on the BHT-Cluster.

Below will be a short explanation on how to get every implemented tool going.

---

## OCR

### PPOCRv5
*[Docs](https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/OCR.html)*

**PPOCRv5 takes image files as input.**

1. Install the PaddlePaddle Version respective to your OS and CUDA Version: [Link](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/linux-pip_en.html)
2. Install PaddleOCR via pip: `pip install paddleocr[all]`
