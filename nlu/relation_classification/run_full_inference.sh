#!/usr/bin/bash

: '
This script is used to run the full inference process for a set of models and 
sentence embedders on Creoles: bi, cbk-zam, jam, pih, tpi.

The script first creates the necessary directories if they do not exist.
Then it loops over each model and sentence embedder, and for each combination, it runs the inference process for each Creole language.
The results are logged in a log file specific to the model and sentence embedder combination.
'

# add usage

function script_usage() {
    cat << EOF
Usage: run_full_inference.sh <SEED> <BATCH_SIZE> <WEIGHTS_FOLDER>

Arguments:
    SEED            Seed for the random number generator
    BATCH_SIZE      Batch size for the inference process
    WEIGHTS_FOLDER  Parent folder containing the model weights (e.g. pretrained_weights/, saved_models/, or any other custom name)
EOF
}

# running with args
echo "Running with parameters; Seed: $1; Batch Size: $2; Weights Folder: $3"

if [[ $# -ne 3 ]]; then
    echo "Error: Found $# positional arguments; expected 3"
    script_usage
    exit 1
fi

mkdirs() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdirs "$(dirname "$dir")"
        mkdir "$dir"
    fi
}

SEED=$1
BATCH_SIZE=$2
WEIGHTS_FOLDER=$3
model=('bert-base-multilingual-cased' 'xlm-roberta-base')
sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
Creole=('bi' 'cbk-zam' 'jam' 'tpi')

# Necessary for relative paths

log_dir="log_infer"
output_dir="output"

mkdirs "$output_dir"

for mm in "${model[@]}"; do
    for ss in "${sentence[@]}"; do
        mkdirs "$log_dir"
        log_file="${log_dir}/${mm}_${ss}.log"
        > "$log_file"
        echo "$mm" | tee -a "$log_file"
        echo "$ss" | tee -a "$log_file"
        
        echo "Running with parameters; Model: $mm; Sentence Embedder: $ss; Weights Folder: $WEIGHTS_FOLDER; Seed: $SEED; Batch Size: $BATCH_SIZE"
        bash run_inference.sh "$mm" "$ss" "$WEIGHTS_FOLDER" "$SEED" "$BATCH_SIZE" | tee -a "$log_file"
    
    done
done