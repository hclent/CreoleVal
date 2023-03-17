#!/bin/bash
#
#SBATCH --partition=prioritized
#SBATCH --job-name=affP
#SBATCH --output=%j.out
#SBATCH --time=30:00:00
#SBATCH --mem=256GB


lang=$1


source $HOME/.bashrc
conda activate creole

cd $HOME/Creole-NLU-NLG-Suite/wikipedia



python src/RelationExtraction/affinity_propagation.py "$lang"