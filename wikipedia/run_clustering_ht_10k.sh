#!/bin/bash
#
#SBATCH --partition=prioritized
#SBATCH --job-name=clustering_ht
#SBATCH --output=%j-ht.out
#SBATCH --time=20:00:00
#SBATCH --mem=256GB

source $HOME/.bashrc
conda activate creole

cd $HOME/Creole-NLU-NLG-Suite/wikipedia



python src/RelationExtraction/clustering_ht_ent_10.py
