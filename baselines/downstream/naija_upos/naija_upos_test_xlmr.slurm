#!/bin/bash
#SBATCH -A default_project
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=1:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=naija_upos_test_xlmr

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>

cd $loggingdir

bert='xlmr'
algo='baseline'
lang='naija'
task='upos'


serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo

input_file='data/naija/naija-sud/pcm_nsc-ud-test.conllu'
output_file=$serialized_dir_a/test.pred.conll

python $codebase/predict.py $serialized_dir_a/2022.11.24_20.11.35/model.pt $input_file $output_file --device 0 
