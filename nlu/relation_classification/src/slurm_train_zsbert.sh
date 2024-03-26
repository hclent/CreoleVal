#!/bin/bash -e

#SBATCH --job-name=zsbert
#SBATCH --account=project_465000909
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50GB
#SBATCH --output=zs_finetune_%j.out
#SBATCH --error=zs_finetune_%j.err

set -x



SEED=$1
TRANSFORMER=$2
SENTENCE_TRANSFORMER=$3
BATCH_SIZE=$4

wd=$(pwd)
echo "working directory ${wd}"

# LUMI

SIF=/scratch/project_465000909/lumi-pytorch-rocm-5.6.1-python-3.10-pytorch-v2.1.0-dockerhash-aa8dbea5e0e4.sif
# SIF=/home/cs.aau.dk/ng78zb/pytorch_23.10-py3.sif
echo "sif ${SIF}"


chmod +x ${wd}
chmod +x ${wd}/train_zsbert.sh

echo "setting transformer to ${TRANSFORMER} and sentence embedding to ${SENTENCE_TRANSFORMER}"
echo "batch size ${BATCH_SIZE}, SEED ${SEED}"

# aicloud
#srun singularity exec --nv --cleanenv --bind ${wd}:${wd} \
#    ${SIF} ${wd}/train_zsbert.sh ${SEED} ${TRANSFORMER} ${SENTENCE_TRANSFORMER} ${BATCH_SIZE}

srun singularity exec \
    -B /scratch/project_465000909:/scratch/project_465000909 \
    -B ${wd}:${wd} \
    ${SIF} ${wd}/train_zsbert.sh ${SEED} ${TRANSFORMER} ${SENTENCE_TRANSFORMER} ${BATCH_SIZE}
