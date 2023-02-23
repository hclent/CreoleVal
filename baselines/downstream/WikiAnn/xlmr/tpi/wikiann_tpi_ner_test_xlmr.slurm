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
#SBATCH --job-name=wikiann_tpi_ner_test_xlmr


source activate creole

codebase=/data/leuven/351/vsc35188/machamp
loggingdir=/scratch/leuven/351/vsc35188/CreoleNLP-Baselines/creole-dro

cd $loggingdir

bert='xlmr'
algo='baseline'
lang='wikiann_tpi'
task='ner'

serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo

input_file='data/WikiAnn_data/tpi/tpi-test.txt'
output_file=$serialized_dir_a/test.pred.tsv

python $codebase/predict.py $serialized_dir_a/2022.12.16_14.40.17/model.pt $input_file $output_file --device 0 
