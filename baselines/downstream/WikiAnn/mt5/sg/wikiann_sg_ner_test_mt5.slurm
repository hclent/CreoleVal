#!/bin/bash
#SBATCH --cluster=wice
#SBATCH -A lp_wice_pilot
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=1:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=wikiann_sg_ner_test_mt5

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>

cd $loggingdir

bert='mt5'
algo='baseline'
lang='wikiann_sg'
task='ner'

serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo

input_file='data/WikiAnn_data/sg/sg-test.txt'
output_file=$serialized_dir_a/test.pred.tsv

python $codebase/predict.py $serialized_dir_a/2022.12.19_11.28.20/model.pt $input_file $output_file --device 0 
