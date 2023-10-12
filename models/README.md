Baseline models
===============

Baseline pretrained models can be found on hf hub:

- Ancestor-based models (creoles clustered by ancestor language):
  - English [`lgrobol/xlm-r-CreoleEval_eng`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_eng)
  - French [`lgrobol/xlm-r-CreoleEval_fra`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_fra)
  - Kongo [`lgrobol/xlm-r-CreoleEval_kon`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_kon)
  - Malay [`lgrobol/xlm-r-CreoleEval_msa`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_msa)
  - Northern Ngbandi [`lgrobol/xlm-r-CreoleEval_ngb`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_ngb)
  - Portuguese [`lgrobol/xlm-r-CreoleEval_por`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_por)
  - Spanish [`lgrobol/xlm-r-CreoleEval_spa`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_spa)
- A model fine-tuned on all the Creole data:  [`lgrobol/xlm-r-CreoleEval_all`](https://huggingface.co/lgrobol/xlm-r-CreoleEval_all)

- These models are all obtained by fine-tuning XLM-RoBERTa-base as a MLM on (part of the) CreoleEval data that is not used in tasks. The hyperparameters are taken from Wang et al. ([2020](https://aclanthology.org/2020.findings-emnlp.240/)).
