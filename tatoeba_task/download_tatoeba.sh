#!/bin/bash

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

# variables for extracting src and trg files
SOURCE="data/release/*/*/*.src"
TARGET="data/release/*/*/*.trg"
ARCHIVED="data/release/*/*/*.gz"

mkdir tatoeba

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
                        wget "$URL"
                        tar -xvf "$LANGTAR"
                        gzip -dv "$ARCHIVED"
                        mdkir "tatoeba/$LG"
                        mv "$TARGET" "tatoeba/$LG/"
                        mv "$SOURCE" "tatoeba/$LG/"
                        rm -r data
                        rm -r "$LANGTAR"
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
                        wget "$URL"
                        mkdir "tatoeba/$LG"
                        cut -f 3 "$FILENAME" > "tatoeba/$LG/test.src"
                        cut -f 4 "$FILENAME" > "tatoeba/$LG/test.trg"
                        rm "$FILENAME"
                fi
        fi
done

