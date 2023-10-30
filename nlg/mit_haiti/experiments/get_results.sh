#!/bin/bash

# ====== EN --> HT ======
python translate.py -sl en
python eval.py -sl en -r 'results.txt'


# ====== FR --> HT ======
python translate.py -sl fr
python eval.py -sl fr -r 'results.txt'


# ====== ES --> HT ======
python translate.py -sl es
python eval.py -sl es -r 'results.txt'