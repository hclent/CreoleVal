# Tatoeba task
Created for the Creole Suite by Marcell Fekete. Accuracy scores are out of a 100.


## Getting Started

### Environment Setup
Tested with `Ubuntu 22` and `Python 3.10`.

1. Create a Python virtual environment, either `venv` or `conda`;
2. Install the necessary dependencies with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt` if using `conda`.
3. Additionally install PyTorch with your preferred configuration https://pytorch.org/

### Generating Results
1. Activate your Python environment;
2. Run `bash ./run_experiments.sh` from `tatoeba_task/` as your working directory.
3. Results are stored in the `experiments/` folder.

The script will download the necessary data and run the experiments for the models `bert-base-multilingual-cased`, `xlm-roberta-base`, `google/mt5-base`, and `random` (for random baseline). By default `python3` is used to run the Python code, change this as needed.

### Analysis
* Run the `plot_distributions.py` script with the input folder `data/` and output folder `./plots/length` as arguments. This will plot sentence lengths per language pair.
* Run the `create_tables.py` script with the input folder `experiments/` as an argument.
* `analysis.py`: calculates _tokenizer fertility_ and _token overlap between source and target sentences_ and plots them with a default output in `./plots/analysis/`

## Contents

### Folders
- `./data/` folder: contains test samples in the format of tsv files
- `./experiments/` folder: contains experiment outputs per language model (and random baseline)
- `./plots/length/` folder: contains barplots plotting the length distribution of the test samples
- `./plots/analysis` folder: contains plots of _tokenizer fertility_ and _token overlap between source and target sentences_ per language pair per language model  
- `./tables/` folder: contains the aggregated results of the experiments with accuracy and average cosine similarity scores per language
- `./tatoeba/` folder: if the `download_tatoeba.sh` or `run_experiments.sh` script is run, it contains the data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository arranged in folders per language

### Scripts
- `create_tables.py`: aggregates experimental results with a default output in `./tables/`
- `download_tatoeba.sh`: downloads data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository and arranges it in the right format for further processing with a default output in `./tatoeba/`
- `prepare_data.py`: creates test samples conforming with the Tatoeba task with a default output in `./data/`
- `run_experiments.sh`: downloads and prepares the data from the [Tatoeba Challenge](https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/data/README.md) repository and carries out the sentence pair retrieval task, by default for `bert-base-multilingual-cased`, `xlm-roberta-base`, `google/mt5-base` and `random` (for random baseline) with outputs in `./experiments/`
It does this by calling the other scripts `run_tatoeba.py`: carries out the sentence pair retrieval task with a default output in `./experiments/`