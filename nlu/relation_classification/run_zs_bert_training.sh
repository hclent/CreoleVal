#!/bin/bash

# Usage: remember to create and activate the conda environment before running this script
echo "Remember:
  - Create and activate your corresponding Conda environment before running this script;
  - This script calls Python3 by default;
"


if [ ! -d data/ukp ]; then
  mkdir -p data/ukp;
fi
if [ ! -d output ]; then
  mkdir -p output;
fi
if [ ! -d model ]; then
  mkdir -p model;
fi


# Download data
UKP="data/ukp/wiki_all.json"
FILE_ID="1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK"

if test -f $UKP;
  then
    echo "UKP file exists ..."
  else
    echo "downloading UKP English data... to data/ukp/wiki_all.json"
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK' -O $UKP
fi

# test if relation_classification/src/ZS_BERT/Wiki-ZSL/train.json exists
if [ ! -f src/ZS_BERT/Wiki-ZSL/train.json ]; 
  then
    wget https://huggingface.co/datasets/yiyic/ukp_m5/resolve/main/train.json -O src/ZS_BERT/Wiki-ZSL/train.json
  else
    echo "Found src/ZS_BERT/Wiki-ZSL/test.json ..."
fi

if [ ! -f src/ZS_BERT/Wiki-ZSL/test.json ]; 
  then
    wget https://huggingface.co/datasets/yiyic/ukp_m5/resolve/main/test.json -O src/ZS_BERT/Wiki-ZSL/test.json
  else
    echo "Found src/ZS_BERT/Wiki-ZSL/test.json ..."
fi


######### TRAIN ZS_BERT
echo "Redirect to the ZS_BERT directory ..."

# echo "training zs_bert with" $m  "unseen classes, multilingual bert transformer, and bert base sentence embedder..."
python3 src/ZS_BERT/model/train_wiki.py -re 768 -t bert-base-multilingual-cased -se bert-base-nli-mean-tokens --Wiki_ZSL_data src/ZS_BERT/Wiki-ZSL/ -cr bi cbk-zam jam tpi --Creole_data data/relation_extraction