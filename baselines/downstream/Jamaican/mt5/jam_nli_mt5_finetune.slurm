#!/bin/bash
#SBATCH --cluster=wice
#SBATCH -A lp_wice_pilot
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=3:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=jam_mnli_mt5_finetune

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>
downstreamdir=$loggingdir/downstream

cd $loggingdir

bert="mt5"
algo="baseline"  
trainlang="glue"
finetune="jamaican"
task="nli"  

parameters_config=$downstreamdir/configs/params_nli_mt5.json

python $codebase/train.py --parameters_config $parameters_config --dataset_config $downstreamdir/configs/$task\_$finetune.json --retrain $loggingdir/logs/$finetune-$task-$bert-training/2023.01.07_22.18.35/model.pt --name nli_jamaican_mt5_finetuned
