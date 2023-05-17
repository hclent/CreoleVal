#!/bin/bash

# models to use
MODELS=(
"bert-base-multilingual-cased"
"xlm-roberta-base"
"google/mt5-base"
"random"
)

# download tatoeba datasets
bash download_tatoeba.sh

# activate python environment
source activate tatoeba

echo ""

# preprocess files
for FOLDER in tatoeba/*
do
	python prepare_data.py $FOLDER
	echo "$FOLDER processed"
done

echo ""

# carry out experiments
for MODEL in ${MODELS[@]}
do
	echo "$MODEL"
	echo ""
	for FILE in tatoeba/*
	do
		python run_tatoeba.py $FILE experiments/ $MODEL
		echo "$FILE processed"
		echo ""
	done
done
