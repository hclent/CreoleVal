#!/usr/bin/bash

: '
This script is used to run the full inference process for a set of models and 
sentence embedders on Creoles: bi, cbk-zam, jam, pih, tpi.

The script first creates the necessary directories if they do not exist.
Then it loops over each model and sentence embedder, and for each combination, it runs the inference process for each Creole language.
The results are logged in a log file specific to the model and sentence embedder combination.
'

mkdirs() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdirs "$(dirname "$dir")"
        mkdir "$dir"
    fi
}

HF_NAMESPACE=$1

model=('bert-base-multilingual-cased' 'xlm-roberta-base' 'xlm-roberta-large' 'bert-base-cased' 'bert-large-cased')
sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
Creole=('bi' 'cbk-zam' 'jam' 'pih' 'tpi')

# check if ZSBert_mBERT-finetuned exists
if [ ! -d pretrained_weights ]; then
    echo "Downloading pretrained weights, this may take ~10-20min"
    echo ""
    
    git lfs install
    git clone https://huggingface.co/$HF_NAMESPACE pretrained_weights
fi

# check if not unzipped, otherwise loop over sentence and unzip each model
if [ ! -d pretrained_weights/bert-base-multilingual-cased/bert-base-nli-mean-tokens ]; then
    for ss in "${sentence[@]}"; do
        echo "Unzipping $mm $ss"
        unzip pretrained_weights/$mm/$ss.zip -d pretrained_weights/$mm/$ss
    done
fi


log_dir="log_infer"
data_dir="data/relation_extraction"
proper_dir="data/relation_extraction/properties"
model_dir="pretrained_weights"
output_dir="output"
model_name="best_f1_0.7094704724243616_wiki_epoch_1_alpha_0.4_gamma_7.5"

mkdirs "$output_dir"
for mm in "${model[@]}"; do
    for ss in "${sentence[@]}"; do
        mkdirs "$log_dir"
        log_file="${log_dir}/${mm}_${ss}.log"
        > "$log_file"
        echo "$mm" | tee -a "$log_file"
        echo "$ss" | tee -a "$log_file"
        best_model="${model_dir}/${mm}/${ss}/${model_name}"
        for dd in "${Creole[@]}"; do
            data_file="${data_dir}/${dd}.json"
            proper_file="${proper_dir}/${dd}.json"
            CUDA_VISIBLE_DEVICES=0 python3 src/ZS_BERT/model/inference.py "$data_file" "$proper_file" "$output_dir" "$ss" "$mm" "$best_model" | tee -a "$log_file"
        done
    done
done