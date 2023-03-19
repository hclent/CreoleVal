#!/bin/bash
#
#SBATCH --partition=prioritized
#SBATCH --job-name=affP
#SBATCH --output=%j.out
#SBATCH --time=30:00:00
#SBATCH --mem=512GB


lang=$1
algo=$2

source $HOME/.bashrc
conda activate creole

cd $HOME/Creole-NLU-NLG-Suite/wikipedia



python src/RelationExtraction/affinity_propagation.py "$lang" "$algo"