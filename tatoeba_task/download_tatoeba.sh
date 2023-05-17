#!/usr/bin/env bash

set -o errexit

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DATADIR="$SCRIPTDIR/tatoeba"

# urls to download from
URLS=(
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-hat.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/cbk-eng.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-gcf.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-jam.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-pap.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-sag.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/eng-tpi.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/fra-hat.tar
https://object.pouta.csc.fi/Tatoeba-Challenge-v2021-08-07/fra-gcf.tar
https://github.com/Helsinki-NLP/Tatoeba-Challenge/raw/master/data/devtest/deu-eng/test-v2021-03-10.txt
https://github.com/Helsinki-NLP/Tatoeba-Challenge/raw/master/data/devtest/eng-fra/test-v2021-07-22.txt
https://github.com/Helsinki-NLP/Tatoeba-Challenge/raw/master/data/devtest/eng-nor/test-v2020-05-31.txt
)

for URL in "${URLS[@]}"
do
        if [[ $URL == *.tar  ]]
        then
                LANGTAR=${URL:(-11)}
                LG=${LANGTAR:0:7}
                if
                        [ -d "tatoeba/$LG"  ]
                then
                        echo "$LG already exists"
                else
                        echo "downloading $LG"
                        wget -O "$LANGTAR" "$URL"
                        tar -xvf "$LANGTAR"
                        find data/release/ -name '*.gz' -exec gzip -dv {} \;
                        mkdir -p "$DATADIR/$LG"
                        find data/release/ -name '*.src' -o -name '*.trg' -exec mv {} "$DATADIR/$LG/" +
                        rm -rf data/release
                        rm -f "$LANGTAR"
                fi
        else
                IFS="/" read -ra ARRAY <<< "$URL"
                LG=${ARRAY[9]}
                FILENAME=${ARRAY[10]}
                if
                        [ -d "tatoeba/$LG" ]
                then
                        echo "$LG already exists"
                else
                        echo "downloading $LG"
                        wget -O "$FILENAME" "$URL"
                        mkdir -p "$DATADIR/$LG"
                        cut -f 3 "$FILENAME" > "$DATADIR/$LG/test.src"
                        cut -f 4 "$FILENAME" > "$DATADIR/$LG/test.trg"
                        rm -f "$FILENAME"
                fi
        fi
done

