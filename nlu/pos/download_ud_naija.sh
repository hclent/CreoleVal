#!/usr/bin/env bash

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/data/naija/naija-sud"
FILELIST=("https://github.com/UniversalDependencies/UD_Naija-NSC/raw/master/pcm_nsc-ud-train.conllu"
          "https://github.com/UniversalDependencies/UD_Naija-NSC/raw/master/pcm_nsc-ud-dev.conllu"
          "https://github.com/UniversalDependencies/UD_Naija-NSC/raw/master/pcm_nsc-ud-test.conllu")

mkdir -p "$DATADIR"
for file in ${FILELIST[@]}; do
    wget -nc --directory-prefix "$DATADIR" "$file"
done
