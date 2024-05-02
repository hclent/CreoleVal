# UD Part-of-Speech Tagging with Singlish

## Overview
The task covers Singlish (singlish) and Nigerian Pidgin (pcm) part-of-speech tagging. The data is from the Universal Dependencies project.

## Prerequisites
Tested with `Ubuntu 22` and `Python 3.10` and `Nvidia A10` GPU.
- Ensure you have the `machamp` submodule initialized in case you did not clone with `--recursive` flag:
  ```bash
  git submodule update --init --recursive
  ```
- Setup a working Python environment and install the `requirements.txt` from the [MaChAmp](..) directory.
- Download the datasets with `./download_singlish_upos.sh` and `./download_ud_naija.sh`.

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
  - Filenames beginning with `upos` contain the data filepaths and configurations. Ensure that filepaths mentioned in these files are same as the filepaths to the data files on your system (should be the case if you use the instructions & scripts in this repo).

**Output** of a train file will create a `logs` dir where all your models, metrics, scores and test files will be stored.


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
