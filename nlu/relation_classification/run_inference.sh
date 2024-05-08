#!/bin/bash -e

function script_usage() {
    cat << EOF
Usage: run_full_inference.sh <MODEL> <SENTENCE_TRANSFORMER> <WEIGHTS_FOLDER> <BATCH_SIZE> <SEED>

Arguments:
    MODEL                   Model to use for inference
    SENTENCE_TRANSFORMER    Sentence transformer to use for inference
    WEIGHTS_FOLDER          Parent folder containing the model weights (e.g. pretrained_weights/, saved_models/, or any other custom name)
    BATCH_SIZE              Batch size for the inference process
    SEED                    Seed for the random number generator
EOF
}

# running with args
echo "Running with parameters; Seed: $1; Batch Size: $2; Weights Folder: $3"

if [[ $# -ne 5 ]]; then
    echo "Error: Found $# positional arguments; expected 3"
    script_usage
    exit 1
fi

TRANSFORMER=$1
SENTENCE_TRANSFORMER=$2
WEIGHTS_FOLDER=$3
BATCH_SIZE=$4
SEED=$5

echo "Running inference on Creoles"
echo "seed ${SEED}"

# sentence_embedder, tokenizer, seed, batch_size
python3 src/ZS_BERT/model/inference_batch.py ${TRANSFORMER} ${SENTENCE_TRANSFORMER} ${WEIGHTS_FOLDER} ${SEED} ${BATCH_SIZE}
