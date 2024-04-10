#!/usr/bin/env bash

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
