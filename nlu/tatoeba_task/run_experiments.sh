#!/bin/bash

: '
This script is used to run experiments on different models with the Tatoeba dataset.
Ensure to have an environment called tatoeba with dependencies installed as per requirements.txt
'

# models to use
MODELS=(
"bert-base-multilingual-cased"
"xlm-roberta-base"
"google/mt5-base"
"random"
)

# download tatoeba datasets
bash download_tatoeba.sh
echo ""

# preprocess files
for FOLDER in tatoeba/*
do
	python3 prepare_data.py $FOLDER
	echo "$FOLDER processed"
done

echo ""

# carry out experiments
for MODEL in "${MODELS[@]}"
do
	echo "$MODEL"
	echo ""
	for FILE in data/*
	do
		python3 run_tatoeba.py $FILE experiments/ $MODEL
		echo "$FILE processed"
		echo ""
	done
done

