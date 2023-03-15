#!/bin/bash
#
#SBATCH --partition=prioritized
#SBATCH --job-name=clustering_ht
#SBATCH --output=%j-ht.out
#SBATCH --time=20:00:00
#SBATCH --mem=64GB

source $HOME/.bashrc
conda activate creole

cd $HOME/Creole-NLU-NLG-Suite/wikipedia



python src/RelationExtraction/clustering.py
