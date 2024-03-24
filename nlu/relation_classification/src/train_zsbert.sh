#!/bin/bash -e

# activate creole
source /home/cs.aau.dk/ng78zb/miniconda3/etc/profile.d/conda.sh
conda activate creole

SEED=$1
TRANSFORMER=$2
SENTENCE_TRANSFORMER=$3
BATCH_SIZE=$4


#
#model=('bert-base-multilingual-cased' 'xlm-roberta-base' )
#sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')

echo "TRAINING SBERT"
CUDA_VISIBLE_DEVICES=0 python ZS_BERT/model/train_wiki.py -s ${SEED} -b ${BATCH_SIZE} -t ${TRANSFORMER} -se ${SENTENCE_TRANSFORMER}

