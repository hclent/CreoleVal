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
)

# variables for extracting src and trg files
SOURCE="data/release/*/*/*.src"
TARGET="data/release/*/*/*.trg"
ARCHIVED="data/release/*/*/*.gz"

mkdir tatoeba

for URL in ${URLS[@]}
do
	LANGTAR=${URL:(-11)}
	LANG=${LANGTAR:0:7}
	if
		[ -d tatoeba/$LANG ]
	then
		echo "$LANG already exists"
	else
		echo "downloading $LANG"
		wget $URL
		tar -xvf $LANGTAR
		gzip -dv $ARCHIVED
		mkdir tatoeba/$LANG
		mv $TARGET tatoeba/$LANG/
		mv $SOURCE tatoeba/$LANG/
		rm -r data
		rm -r $LANGTAR
	fi
done

