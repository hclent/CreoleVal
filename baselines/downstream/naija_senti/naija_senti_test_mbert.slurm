#!/bin/bash
#SBATCH --cluster=wice
#SBATCH -A intro_vsc35188
#SBATCH -N 1
#SBATCH --ntasks=18
#SBATCH --gpus-per-node=1
#SBATCH --partition=gpu
#SBATCH --mem-per-cpu=5G
#SBATCH --time=1:00:00
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=kushaljayesh.tatariya@kuleuven.be
#SBATCH --job-name=naija_senti_test_mbert

source activate creole

codebase=/data/leuven/351/vsc35188/machamp
loggingdir=/scratch/leuven/351/vsc35188/CreoleNLP-Baselines/creole-dro

cd $loggingdir

bert='mbert'
algo='baseline'
lang='naija'
task='senti'

serialized_dir_a=$loggingdir/logs/$lang-$task-$bert-$algo

input_file='data/naijasenti-data/pcm_test.tsv'
output_file=$serialized_dir_a/test.pred.tsv

python $codebase/predict.py $serialized_dir_a/2023.01.23_14.59.47/model.pt $input_file $output_file --device 0 
