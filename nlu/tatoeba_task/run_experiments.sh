#!/bin/bash

# models to use
MODELS=(
"bert-base-multilingual-cased"
"xlm-roberta-base"
"google/mt5-base"
"random"
"lgrobol/xlm-r-CreoleEval_all"
)

# download tatoeba datasets
bash download_tatoeba.sh

# activate python environment
source activate tatoeba

echo ""

# preprocess files
echo "Preprocessing"
for FOLDER in tatoeba/*
do
	python prepare_data.py $FOLDER
	echo "$FOLDER preprocessed"
done

echo ""

# Ancestor-based models
echo "Using ancestor models"
for FILE in data/*
do
	NAME=$(basename $FILE)
	case ${NAME:0:3} in
		"cbk") ANCESTOR="spa";;
		"gcf") ANCESTOR="fra";;
		"hat") ANCESTOR="fra";;
		"jam") ANCESTOR="eng";;
		"pap") ANCESTOR="por";;
		"sag") ANCESTOR="ngb";;
		"tpi") ANCESTOR="eng";;
		*)
			echo "Skipping non-creole $FILE"
			continue
		;;
	esac
	echo "Processing $FILE using the $ANCESTOR ancestor model"
	python run_tatoeba.py $FILE experiments/ "lgrobol/xlm-r-CreoleEval_$ANCESTOR"
	echo "$FILE processed"
	echo ""
done

# carry out experiments
echo "Using multiling models"
for MODEL in ${MODELS[@]}
do
	echo "$MODEL"
	echo ""
	for FILE in data/*
	do
		python run_tatoeba.py $FILE experiments/ $MODEL
		echo "$FILE processed"
		echo ""
	done
done



