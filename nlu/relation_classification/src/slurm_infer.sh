#!/bin/bash -e

#SBATCH --job-name=infer
#SBATCH --mem=50GB
#SBATCH --time=2-00:00:00
#SBATCH --output=zs_infer_%j.out
#SBATCH --error=zs_infer_%j.err

set -x


TRANSFORMER=$1
SENTENCE_TRANSFORMER=$2
BATCH_SIZE=$3



wd=$(pwd)
echo "working directory ${wd}"

# LUMI

#SIF=/scratch/project_465000909/lumi-pytorch-rocm-5.6.1-python-3.10-pytorch-v2.1.0-dockerhash-aa8dbea5e0e4.sif
SIF=/home/cs.aau.dk/ng78zb/pytorch_23.10-py3.sif
echo "sif ${SIF}"


chmod +x ${wd}
chmod +x ${wd}/infer_zsbert.sh

echo "setting transformer to ${TRANSFORMER} and sentence embedding to ${SENTENCE_TRANSFORMER}"

seeds=(563 757 991)
# aicloud
for s in "${seeds[@]}]}"; do
  srun singularity exec --nv --cleanenv --bind ${wd}:${wd} \
    ${SIF} ${wd}/infer_zsbert.sh ${SENTENCE_TRANSFORMER} ${TRANSFORMER} ${s} ${BATCH_SIZE}

done