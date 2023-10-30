#!/usr/bin/env bash

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/data/singlish"
FILELIST=("https://github.com/wanghm92/Sing_Par/raw/master/ACL17_dataset/treebank/gold_pos/train.conll"
          "https://github.com/wanghm92/Sing_Par/raw/master/ACL17_dataset/treebank/gold_pos/dev.conll"
          "https://github.com/wanghm92/Sing_Par/raw/master/ACL17_dataset/treebank/gold_pos/test.conll")

mkdir -p "$DATADIR"
for file in ${FILELIST[@]}; do
    wget -nc --directory-prefix "$DATADIR" "$file"
done
