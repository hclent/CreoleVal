# Tatoeba task

Created for the Creole Suite by Marcell Fekete.

Accuracy scores are out of a 100.

## Instructions

* Create a virtual environment and install necessary dependencies (see [Section Dependencies](#dependencies)).
* Run the `run_experiments.sh` bash script, which downloads and processes all the necessary Creole datasets from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository, and carries out the sentence pair retrieval task for 3 default models: `bert-base-multilingual-cased`, `xlm-roberta-base`, `google/mt5-base`, and `random` (for random baseline).
* Run the `plot_distributions.py` script with the input folder `./data/` and output folder `./plots/length` as arguments.
* Run the `create_tables.py` script with the input folder `./experiments/` as an argument.

## Dependencies

Make sure to install the following libraries:

`transformers` `pandas` `nltk` `seaborn` `matplotlib` `faiss-gpu` (or `faiss-cpu`)

It is recommended to use the `requirements.txt` file in the `./tatoeba_task/` folder.

## Contents

### Folders

`./data/` folder: contains test samples in the format of tsv files

`./experiments/` folder: contains experiment outputs per language model (and random baseline)

`./plots/length/` folder: contains barplots plotting the length distribution of the test samples

`./plots/analysis` folder: contains plots of _tokenizer fertility_ and _token overlap between source and target sentences_ per language pair per language model  

`./tables/` folder: contains the aggregated results of the experiments with accuracy and average cosine similarity scores per language

`./tatoeba/` folder: if the `download_tatoeba.sh` or `run_experiments.sh` script is run, it contains the data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository arranged in folders per language

### Scripts

`analysis.py`: calculates _tokenizer fertility_ and _token overlap between source and target sentences_ and plots them with a default output in `./plots/analysis/`

`create_tables.py`: aggregates experimental results with a default output in `./tables/`

`download_tatoeba.sh`: downloads data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository and arranges it in the right format for further processing with a default output in `./tatoeba/`

`plot_distributions.py`: plots the distribution of sentence lengths per test sample with a default output in `./plots/`

`prepare_data.py`: creates test samples conforming with the Tatoeba task with a default output in `./data/`

`run_experiments.sh`: downloads and prepares the data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository and carries out the sentence pair retrieval task, by default for `bert-base-multilingual-cased`, `xlm-roberta-base`, `google/mt5-base` and `random` (for random baseline) with outputs in `./experiments/`
It does this by calling the other scripts

`run_tatoeba.py`: carries out the sentence pair retrieval task with a default output in `./experiments/`
