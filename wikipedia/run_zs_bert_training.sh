#!/bin/bash

m=$1


#conda create -n creole python=3.10

conda activate re

#pip install -r requirements.txt


# download ukp data
UKP="data/ukp/wiki_all.json"
FILE_ID="1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK"


if test -f $UKP;
  then
    echo "UKP file exists ..."
  else
    echo "downloading UKP English data... to data/ukp/wiki_all.json"
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK' -O $UKP

fi



######### TRAIN ZS_BERT
echo "Redirect to the ZS_BERT directory ..."

cd src/ZS_BERT/model

echo "training zs_bert with" $m  "unseen classes, multilingual bert transformer, and bert base sentence embedder..."
python train_wiki.py -m $m -re 768 -t bert-base-multilingual-cased -se bert-base-nli-mean-tokens





