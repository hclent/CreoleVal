#!/usr/bin/env bash

# Download pretraining MNLI Glue data (as per JamPatois paper)
wget https://github.com/nyu-mll/GLUE-baselines/raw/master/download_glue_data.py
python3 download_glue_data.py --data_dir data/glue --tasks MNLI

# Download Fine-tuning Jamaican data
SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/data/jam-nli-data"
FILELIST=(
    "https://github.com/ruth-ann/jampatoisnli/raw/main/datasets/patoisnli/jampatoisnli-train.csv"
    "https://github.com/ruth-ann/jampatoisnli/raw/main/datasets/patoisnli/jampatoisnli-val.csv"
    "https://github.com/ruth-ann/jampatoisnli/raw/main/datasets/patoisnli/jampatoisnli-test.csv"
)

mkdir -p "$DATADIR"
for file in ${FILELIST[@]}; do
    wget -nc --directory-prefix "$DATADIR" "$file"
done
