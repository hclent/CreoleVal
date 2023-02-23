#!/bin/bash
#SBATCH --cluster=wice
#SBATCH -A intro_vsc35188
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=3:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=naija_senti_train

source activate creole

codebase=/data/leuven/351/vsc35188/machamp
loggingdir=/scratch/leuven/351/vsc35188/CreoleNLP-Baselines/creole-dro
downstreamdir=$loggingdir/downstream

cd $loggingdir

bert=$1  #bert or mbert
algo="baseline"  #baseline or dro
lang="naija"  #naija or singlish
task="senti"  #ner (naija) or upos (singlish or naija)

parameters_config=$downstreamdir/configs/params_$bert.json

python $codebase/train.py --parameters_config $parameters_config --dataset_config $downstreamdir/configs/$task\_$lang.json --name $lang-$task-$bert-$algo
