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
#SBATCH --job-name=singlish_upos_test_mbert

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>

cd $loggingdir

bert='mbert'
algo='baseline'
lang='singlish'
task='upos'

serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo

input_file='data/singlish/test.conll'
output_file=$serialized_dir_a/test.pred.conll

python $codebase/predict.py $serialized_dir_a/2022.11.25_12.55.37/model.pt $input_file $output_file --device 0 
