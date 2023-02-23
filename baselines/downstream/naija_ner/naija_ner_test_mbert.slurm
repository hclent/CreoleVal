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
#SBATCH --job-name=naija_ner_test_mbert

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>

cd $loggingdir

bert='mbert'
algo='baseline'
lang='naija'
task='ner'

serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo/

input_file='data/naija/masakhane-ner-pcm/test.txt'
output_file=$serialized_dir_a/test.pred.txt


python $codebase/predict.py $serialized_dir_a/2022.11.25_11.36.46/model.pt $input_file $output_file --device 0 
