#!/bin/bash -e

# activate creole
#source /home/cs.aau.dk/ng78zb/miniconda3/etc/profile.d/conda.sh
#conda activate creole

# LUMI
#$WITH_CONDA
#conda activate v2t

TRANSFORMER=$1
SENTENCE_TRANSFORMER=$2
BATCH_SIZE=$3
SEED=$4


#
#model=('bert-base-multilingual-cased' 'xlm-roberta-base' )
#sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
#seeds=(563 757 991) # prime numbers

echo "Running inference on Creoles"
echo "seed ${SEED}"

#for s in "${seeds[@]}"; do
#  echo "seed $s"
#  CUDA_VISIBLE_DEVICES=0 python ZS_BERT/model/train_wiki.py -s ${s} -b ${BATCH_SIZE} -t ${TRANSFORMER} -se ${SENTENCE_TRANSFORMER} -cr bi
#done

# sentence_embedder, tokenizer, seed, batch_size
python ZS_BERT/model/inference_batch.py ${TRANSFORMER} ${SENTENCE_TRANSFORMER}  ${SEED} ${BATCH_SIZE}
