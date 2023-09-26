#!/bin/bash

LANG=$1

MODEL_PATH=$2
# "../../../model/best_f1_0.7081677743338072_wiki_epoch_4_m_5_alpha_0.4_gamma_7.5"

conda activate re

echo "Redirect to the ZS_BERT directory ..."

cd src/ZS_BERT/model

python inference.py ../../../data/relation_extraction/"$LANG".json ../../../data/relation_extraction/properties/"$LANG".json $MODEL_PATH

