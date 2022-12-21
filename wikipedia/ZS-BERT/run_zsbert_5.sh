#!/bin/bash
#
#SBATCH --partition=batch
#SBATCH --gres=gpu:titanrtx:1
#SBATCH --job-name=wiki-train
#SBATCH --output=wiki-train-m5.txt
#SBATCh --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=8:00:00

source $HOME/.bashrc
conda activate creole #activate your environment
cd $HOME/ZS-BERT #run from a specific directory
python -m src.train_wiki_val_test -m 5