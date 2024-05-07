# Baselines


## Prerequisites
Tested with `Ubuntu 22` and `Python 3.10` and `Nvidia A10` GPU.
- Ensure you have the `machamp` submodule initialized in case you did not clone with `--recursive` flag:
  ```bash
  git submodule update --init --recursive
  ```
- Setup a working Python environment and install the `requirements.txt` from the [MaChAmp](..) directory.
- Download the datasets with `./download_afrisenti.sh`.

All experiments here run with [MaChAmp](https://github.com/machamp-nlp/machamp.git). Configuration files were updated to work with **v0.4.2** of the software.


## Requirements
All experiments here run with [MaChAmp](https://github.com/machamp-nlp/machamp.git).  Configuration files were updated to work with **v0.4.2** of the software.

To get MaChAmp and install its requirements, you can run:

```
git submodule update --init --recursive # (if you didn't clone CreoleVal with --recursive flag)
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
  - Filenames beginning with `senti` contain the data filepaths and configurations. Ensure that filepaths mentioned in these files are same as the filepaths to the data files on your system (should be the case if you use the instructions & scripts in this repo).

**Output** of a train file will create a `logs` dir where all your models, metrics, scores and test files will be stored.


### AfriSenti

- **Data**: [AfriSenti-SemEval Shared Task 12](https://github.com/afrisenti-semeval/afrisent-semeval-2023)
  - Download script: [`download_afrisenti.sh`](download_afrisenti.sh)
- **Config**: [`configs/senti_afri.json`](configs/senti_afri.json)
- **Train**: `./train.sh senti_afri {mbert,mt5,xlmr}`
- **Predict**: `./predict.sh logs/senti_afri_<model>_<date> data/afrisenti/pcm_test.tsv`

### Oyewusi Sentiment

- **Data**: The data is originally from [Data Science Nigeria](https://github.com/DataScienceNigeria/Research-Papers-by-Data-Science-Nigeria/tree/master/Semantic%20Enrichment%20of%20Nigerian%20Pidgin%20English%20for%20Contextual%20Sentiment%20Classification) but we include our train/dev/test splits in [`data/Oyewusi`](data/Oyewusi) in this repo for reproducibility. 
- **Config**: [`configs/senti_oyewusi.json`](configs/senti_oyewusi.json)
- **Train**: `./train.sh senti_oyewusi {mbert,mt5,xlmr}`
- **Predict**: `./predict.sh logs/senti_oyewusi_xlmr_baseline/<date>/ data/oyewusi/test.tsv`