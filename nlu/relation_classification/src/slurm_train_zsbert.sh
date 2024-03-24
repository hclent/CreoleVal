#!/bin/bash -e

#SBATCH --job-name=zsbert
#SBATCH --output=zsbert_train_%j.out
#SBATCH --error=zsbert_train_%j.err
#SBATCH --mem=50GB
#SBATCH --time=2-00:00:00

set -x

SEED=$1
TRANSFORMER=$2
SENTENCE_TRANSFORMER=$3
BATCH_SIZE=$4

wd=$(pwd)
echo "working directory ${wd}"

SIF=/home/cs.aau.dk/ng78zb/pytorch_23.10-py3.sif
echo "sif ${SIF}"


chmod +x ${wd}
chmod +x ${wd}/train_zsbert.sh

echo "setting transformer to ${TRANSFORMER} and sentence embedding to ${SENTENCE_TRANSFORMER}"
echo "batch size ${BATCH_SIZE}, SEED ${SEED}"
srun singularity exec --nv --cleanenv --bind ${wd}:${wd} \
    ${SIF} ${wd}/train_zsbert.sh ${SEED} ${TRANSFORMER} ${SENTENCE_TRANSFORMER} ${BATCH_SIZE}