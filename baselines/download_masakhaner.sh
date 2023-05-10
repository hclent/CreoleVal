#!/usr/bin/env bash

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/data/naija/masakhane-ner-pcm"
FILELIST=("https://github.com/masakhane-io/masakhane-ner/raw/main/MasakhaNER2.0/data/pcm/train.txt"
          "https://github.com/masakhane-io/masakhane-ner/raw/main/MasakhaNER2.0/data/pcm/dev.txt"
          "https://github.com/masakhane-io/masakhane-ner/raw/main/MasakhaNER2.0/data/pcm/test.txt")

mkdir -p "$DATADIR"
for file in ${FILELIST[@]}; do
    wget -nc --directory-prefix "$DATADIR" "$file"
done

# Format conversion (change spaces to tabs)
set -i 's/\s/\t/g' "$DATADIR"/*.txt
