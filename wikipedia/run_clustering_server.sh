#!/bin/bash
#
#SBATCH --partition=prioritized
#SBATCH --job-name=fuzzy
#SBATCH --output=%j.out
#SBATCH --time=30:00:00
#SBATCH --mem=64GB


lang=$1

source $HOME/.bashrc
conda activate creole

cd $HOME/Creole-NLU-NLG-Suite/wikipedia



python src/RelationExtraction/fuzzywuzzy.py "$lang"