# Baselines

## Requirements

All experiments here run with [MaChAmp](https://github.com/machamp-nlp/machamp.git).  Configuration files were updated to work with **v0.4.2** of the software.

To get MaChAmp and install its requirements, you can run:

```
git clone --branch v0.4.2 https://github.com/machamp-nlp/machamp.git
pip install -r machamp/requirements.txt
```

It's recommended to do this in a virtual environment.  (PS. If there are issues with the jsonnet installation, try installing it via conda-forge, i.e. `conda install -c conda-forge jsonnet`).

## Running the Experiments

- The `configs` folder contains all the MaChAmp configuration files for the model hyperparameters and datasets.
  - Filenames beginning with `params_` contain model hyperparameters where the pretrained transformer models can be changed by changing the following line to any Huggingface transformer model:
  ```
    "transformer_model": "bert-base-multilingual-cased",
  ```
  - For all experiments, there are config files for **mBERT**, **mT5**, and **XLM-R**.
  - Filenames beginning with `ner`, `senti`, `nli` and `upos` contain the data filepaths and configurations. Ensure that filepaths mentioned in these files are same as the filepaths to the data files on your system (should be the case if you use the instructions & scripts in this repo).

- The scripts in this directory can be used to train and evaluate all the models.
  - `train.sh <TASK> <MODEL>` trains a model. Example usage:
    ```bash
    ./train.sh senti_afri xlmr
    ```
  - `train_and_finetune_jamnli.sh <MODEL>` is used for Jamaican NLI; see below.
  - `predict.sh <MODELDIR> <TESTFILE>` predicts with and evaluates a model. Example usage:
    ```bash
    ./predict.sh logs/senti_afri_xlmr_baseline/<date>/ data/afrisenti/pcm_test.tsv
    ```
  - [`run_all_experiments.sh`](run_all_experiments.sh) shows how to run everything at once.

- Running a train file will create a `logs` dir where all your models, metrics, scores and test files will be stored.


### AfriSenti

- **Data**: [AfriSenti-SemEval Shared Task 12](https://github.com/afrisenti-semeval/afrisent-semeval-2023)
  - Download script: [`download_afrisenti.sh`](download_afrisenti.sh)
- **Config**: [`configs/senti_afri.json`](configs/senti_afri.json)
- **Train**: `./train.sh senti_afri {mbert,mt5,xlmr}`

### Jamaican NLI

- **Data**: [GLUE MNLI](https://github.com/nyu-mll/GLUE-baselines) _(pretraining)_ + data in [`data/jam-nli-data`](data/jam-nli-data) _(finetuning)_
  - To download, run the following inside this folder:
    ```bash
    wget https://github.com/nyu-mll/GLUE-baselines/raw/master/download_glue_data.py
    python download_glue_data.py --data_dir data/glue --tasks MNLI
    ```
- **Config**: [`configs/nli_glue.json`](configs/nli_glue.json) _(pretraining)_ and [`configs/nli_jamaican.json`](configs/nli_jamaican.json) _(finetuning)_
- **Train**: `./train_and_finetune_jamnli.sh {mbert,mt5,xlmr}`

### Oyewusi Sentiment

- **Data**: [`data/Oyewusi`](data/Oyewusi) (in this repo)
- **Config**: [`configs/senti_oyewusi.json`](configs/senti_oyewusi.json)
- **Train**: `./train.sh senti_oyewusi {mbert,mt5,xlmr}`

### Naija NER

- **Data**: [MasakhaNER 2.0](https://github.com/masakhane-io/masakhane-ner/tree/main/MasakhaNER2.0/data/pcm/)
  - Download script: [`download_masakhaner.sh`](download_masakhaner.sh)
- **Config**: [`configs/ner_naija.json`](configs/ner_naija.json)
- **Train**: `./train.sh ner_naija {mbert,mt5,xlmr}`

### Naija UPOS

- **Data**: [UD Naija-NSC](https://github.com/UniversalDependencies/UD_Naija-NSC)
  - Download script: [`download_ud_naija.sh`](download_ud_naija.sh)
- **Config**: [`configs/upos_naija.json`](configs/upos_naija.json)
- **Train**: `./train.sh upos_naija {mbert,mt5,xlmr}`

### Singlish UPOS

- **Data**: [Singlish STB-ACL](https://github.com/wanghm92/Sing_Par/tree/master/ACL17_dataset/treebank/gold_pos)
  - Download script: [`download_singlish_upos.sh`](download_singlish_upos.sh)
- **Config**: [`configs/upos_singlish.json`](configs/upos_singlish.json)
- **Train**: `./train.sh upos_singlish {mbert,mt5,xlmr}`

### WikiAnn NER

- **Data**: `data/WikiAnn_data/<lang>`
  - `<lang>` can be one of: bi, cbk_zam, ht, pap, pih, sg, tpi
- **Config**: `configs/ner_wikiann_<lang>.json`
- **Train**: `./train.sh ner_wikiann_<lang> {mbert,mt5,xlmr}`
