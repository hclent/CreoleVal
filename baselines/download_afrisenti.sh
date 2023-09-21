#!/usr/bin/env bash

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/data/afrisenti"
FILELIST=("https://github.com/afrisenti-semeval/afrisent-semeval-2023/raw/main/SubtaskA/train/pcm_train.tsv"
          "https://github.com/afrisenti-semeval/afrisent-semeval-2023/raw/main/SubtaskA/dev/pcm_dev.tsv"
          "https://github.com/afrisenti-semeval/afrisent-semeval-2023/raw/main/SubtaskA/test/pcm_test.tsv")

mkdir -p "$DATADIR"
for file in ${FILELIST[@]}; do
    wget -nc --directory-prefix "$DATADIR" "$file"
done
