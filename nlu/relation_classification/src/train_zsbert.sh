#!/bin/bash -e

# activate creole
source /home/cs.aau.dk/ng78zb/miniconda3/etc/profile.d/conda.sh
conda activate creole

TRANSFORMER=$1
SENTENCE_TRANSFORMER=$2
BATCH_SIZE=$3


#
#model=('bert-base-multilingual-cased' 'xlm-roberta-base' )
#sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
seeds=(2 3 5 7 9)

echo "TRAINING SBERT"

for s in "${seeds[@]}"; do
  echo "seed $s"
  CUDA_VISIBLE_DEVICES=0 python ZS_BERT/model/train_wiki.py -s ${s} -b ${BATCH_SIZE} -t ${TRANSFORMER} -se ${SENTENCE_TRANSFORMER}
done
