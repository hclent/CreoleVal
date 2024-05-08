#!/usr/bin/bash

: '
This script is used to run the full inference process for a set of models and 
sentence embedders on Creoles: bi, cbk-zam, jam, pih, tpi.

The script first creates the necessary directories if they do not exist.
Then it loops over each model and sentence embedder, and for each combination, it runs the inference process for each Creole language.
The results are logged in a log file specific to the model and sentence embedder combination.
'

HF_NAMESPACES=("ZSBert_xlmr" "ZSBert_mBERT")
MODEL_NAMES=("xlm-roberta-base" "bert-base-multilingual-cased")
SENT_EMBEDDERS=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')


for ((i=0;i<${#MODELS[@]};++i)); do
    echo "Model: ${MODELS[i]}, Name: ${MODEL_NAMES[i]}"
done

# check if ZSBert_mBERT-finetuned exists
if [ ! -d pretrained_weights ]; then
    mkdir pretrained_weights
    echo "Downloading pretrained weights, this may take ~10-20min"
    echo ""
    
    git lfs install
    # loop over HF_NAMESPACES and clone
    for ((i=0;i<${#MODEL_NAMES[@]};++i)); do
        # Split the tuple into HF namespace and model dir
        HF_NAMESPACE=${HF_NAMESPACES[i]}
        MODEL_DIR=${MODEL_NAMES[i]}
        git clone https://huggingface.co/yiyic/$HF_NAMESPACE-finetuned pretrained_weights/$MODEL_DIR --depth 1
    done
fi

# check if not unzipped, otherwise loop over pretrained_weights $MODEL directory and unzip each model
for MODEL in "${MODEL_NAMES[@]}"; do
    if [ -d "pretrained_weights/$MODEL/" ]; then
        for s in "${SENT_EMBEDDERS[@]}"; do
            echo "Unzipping $MODEL $s"
            unzip pretrained_weights/$MODEL/$s.zip -d pretrained_weights/$MODEL
            rm pretrained_weights/$MODEL/$s.zip
        done
    fi
done

echo "Done!"
