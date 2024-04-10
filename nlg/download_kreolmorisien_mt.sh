#!/bin/bash
: '
This script downloads the KreolMorisien MT dataset and extracts them in a designated kreolmorisien_mt/ folder.

Variables:
FILE_NAMES: An array of file names to be downloaded.
FILE_LOCATION: The URL where the files are located.
LOCATION: The directory where the files will be stored.
'

FILE_NAMES=("cr" "fr-cr" "en-cr")
FILE_LOCATION="https://huggingface.co/datasets/prajdabre/KreolMorisienMT/resolve/main/data/"
LOCATION="kreolmorisien_mt"

# Create the directory if it doesn't exist
mkdir -p $LOCATION

# Download the files
for file_name in "${FILE_NAMES[@]}"
do
    wget "$FILE_LOCATION$file_name.zip"

    # create a subdirectory for each file, unzip and cleanup
    mkdir -p "$LOCATION/$file_name"
    unzip $file_name.zip -d "$LOCATION/$file_name"
    rm $file_name.zip
done