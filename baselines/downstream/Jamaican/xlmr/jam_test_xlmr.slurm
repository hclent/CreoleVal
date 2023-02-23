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
#SBATCH --job-name=jamaican_nli_test_xlmr

source activate creole

codebase=<path_to_machamp_folder>
loggingdir=<path_to_baselines_folder>

cd $loggingdir

serialized_dir_a=$loggingdir/logs/nli_jamaican_xlmr_finetuned

input_file='data/jam-nli-data/jamnli-test.tsv'
output_file=$serialized_dir_a/test.pred.tsv

python $codebase/predict.py $serialized_dir_a/2023.01.06_16.15.44/model.pt $input_file $output_file --device 0 
