#!/bin/bash
#SBATCH --cluster=wice
#SBATCH -A lp_wice_pilot
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=8:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=jam_mnli_mt5_10ep_lr0.0001_dp0.4

source activate creole

codebase=/data/leuven/351/vsc35188/machamp
loggingdir=/scratch/leuven/351/vsc35188/CreoleNLP-Baselines/creole-dro
downstreamdir=$loggingdir/downstream

cd $loggingdir

bert="mt5"
trainlang="glue"
finetune="jamaican"
task="nli"  

parameters_config=$downstreamdir/configs/params_nli_mt5.json

python $codebase/train.py --parameters_config $parameters_config --dataset_config $downstreamdir/configs/$task\_$trainlang.json --name $finetune-$task-$bert-training
