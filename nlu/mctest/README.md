# MCTest for Mauritian Creole & Haitian Kreyòl

This folder contains our new **machine comprehension dataset** as well as
scripts to **run experiments** on it.

## Getting Started
### Environment Setup
Tested with `Ubuntu 22`, `Python 3.10` and `NVidia a40` GPU.
1. Create a Python virtual environment, either `venv` or `conda`;
2. Install the necessary dependencies with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt` if using `conda`.
3. Additionally install PyTorch with your preferred configuration https://pytorch.org/

### Training
1. Activate the virtual environment;
2. Run `./train.sh` script which will automatically fine-tune `mBERT` and `XLM-R` models on the downstream task;
3. Output will be saved in `./output` folder.


## To-Do
- Move all Python code to a folder `src`
- Cleanup `src/preproc.py` code
- Remove `requirements.pip-freeze.txt` they contain full paths for the laptop that was used to generate them, so its useless?
- Maybe one-two sentences on what exactly is going on in this task? i.e. "Read and comprehend a given text passage, and then answer a question by selecting 1 out of 4 answers"

## Additional Information
### Dataset
The dataset is based on [MCTest](https://aclanthology.org/D13-1020/). The
[`MCTest`](MCTest) folder has the original dataset and information from the
original authors.

_Important note:_ Our translators identified an error with the original English
`mc160.dev.17` story: namely, in question 3, the correct answer (B) incorrectly
says "pink" flowers rather than "yellow" flowers.  We have fixed the English
version, included in this repo, and our translations have also been corrected to
reflect the text of the original story.

### Translations
**`MC160.dev`** set has been translated into Marutian Creole and Haitian Creole
by professional translators.  This consists of 30 stories pertaining to a total
of 120 questions (4 multiple choice questions per story).

Notably, we have **two** distinct translations for Haitian:
- [`MCTestHat1/mc160.dev.json`](MCTestHat1/mc160.dev.json) is a direct
  translation, matching the English.
- [`MCTestHat2/mc160.dev.json`](MCTestHat2/mc160.dev.json) is a localized
  translation, with names, places, and activities adjusted to be more relevant
  to Haitian people.

See [`MCTest/CreoleTranslations`](MCTest/CreoleTranslations) for the original
`.txt` translations and the `.tsv` file formats as well.

**NB: Once this data has been uploaded to the MIT-Ayiti website, we will remove
it from the Github, and instead provide a download script to fetch it from the
MIT-Ayiti platform**

### Details on Data Preprocessing
First, we convert the translated `.txt` files into `.tsv` to match the original
English `.tsv` files (see `./MCTest/CreoleTranslations`).  Then we convert these
to `.json` format, as we found it more tidy to work with (these are the
`./MCTest*X*` directries, where X={160, Hat1, Hat2, Mar, 500}.  The
`./MCTest160` dir is the original train, dev, test data in English. The `Hat1`,
`Hat2`, and `Mar` datasets have the translated `mc160.dev.json` files, for
**Hait**ian and **Maur**itian. ).  The `./MCTest500` dir is the English MC500
dataset, as json.

Code for this (though not tidied up...) can be found in `preproc.py`.


## Experiments

### Requirements

All experiments here run with [Huggingface
Transformers](https://huggingface.co/docs/transformers/index) under PyTorch.

To install all required packages, you can run:

```
pip install -r requirements.txt
```

It's recommended to do this in a virtual environment or within a container; we
ran our code in a container based on the docker image
`docker://nvcr.io/nvidia/pytorch:22.08-py3`.  For reference, we include our full
Python environment as `requirements.pip-freeze.txt`.

### Running the Experiments

Please see [`train.sh`](train.sh) and [`evaluate.sh`](evaluate.sh) for concrete
examples on how to train and evaluate the models.

The experiments use separate scripts for mBERT ([`run_mbert.py`](run_mbert.py))
and XLM-R ([`run_xlmr.py`](run_xlmr.py)) as the latter does not make use of the
`token_type_id`s.  We use the Huggingface
[`AutoModelForMultipleChoice`](https://huggingface.co/transformers/v3.3.1/model_doc/auto.html?highlight=automodelformultiplechoice#transformers.AutoModelForMultipleChoice)
to instantiate the models.

- - -

## License

As this data is translated from Microsoft's MCTest dataset, it inherits the same
[license](MCTest/LICENSE.pdf) as the original.
