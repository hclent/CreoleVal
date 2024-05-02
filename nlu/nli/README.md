# Baselines

## Prerequisites
Tested with `Ubuntu 22` and `Python 3.10` and `Nvidia A10` GPU.
- Ensure you have the `machamp` submodule initialized in case you did not clone with `--recursive` flag:
  ```bash
  git submodule update --init --recursive
  ```
- Setup a working Python environment and install the `requirements.txt` from the [MaChAmp](..) directory.
- Download the datasets with `./download_singlish_upos.sh` and `./download_ud_naija.sh`

All experiments here run with [MaChAmp](https://github.com/machamp-nlp/machamp.git). Configuration files were updated to work with **v0.4.2** of the software.


## Requirements
All experiments here run with [MaChAmp](https://github.com/machamp-nlp/machamp.git).  Configuration files were updated to work with **v0.4.2** of the software.

To get MaChAmp and install its requirements, you can run:

```
git submodule update --init --recursive (if you didn't clone CreoleVal with --recursive flag)
pip install -r machamp/requirements.txt
```

It's recommended to do this in a virtual environment.  (PS. If there are issues with the jsonnet installation, try installing it via conda-forge, i.e. `conda install -c conda-forge jsonnet`).


## Running the Experiments
The `configs` folder contains all the MaChAmp configuration files for the model hyperparameters and datasets.

Filenames beginning with `params_` contain model hyperparameters where the pretrained transformer models can be changed by changing the following line to any Huggingface transformer model:
  ```
    "transformer_model": "bert-base-multilingual-cased",
  ```
  - For all experiments, there are config files for **mBERT**, **mT5**, and **XLM-R**.
  - Filenames beginning with `nli` contain the data filepaths and configurations. Ensure that filepaths mentioned in these files are same as the filepaths to the data files on your system (should be the case if you use the instructions & scripts in this repo).

**Output** of a train file will create a `logs` dir where all your models, metrics, scores and test files will be stored.


### Jamaican NLI

- **Data**: [GLUE MNLI](https://github.com/nyu-mll/GLUE-baselines) _(pretraining)_ + [`jampatoisnli`](https://github.com/ruth-ann/jampatoisnli) _(finetuning)_
  - Download script: [`download_jampatois_nli.sh`](download_jampatois_nli.sh)
- **Config**: [`configs/nli_glue.json`](configs/nli_glue.json) _(pretraining)_ and [`configs/nli_jamaican.json`](configs/nli_jamaican.json) _(finetuning)_
- **Train**: `./train_and_finetune_jamnli.sh {mbert,mt5,xlmr}`
- **Predict**: `./predict.sh logs/nli_jamaican_<model>_<date> data/jampatoisnli/test.tsv`