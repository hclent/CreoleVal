#!/usr//bin/bash

# Usage
usage() {
cat << EOF
Usage:
    bash run_inference.sh <LANG> <MODEL_PATH> <MODEL_NAME> <SENTENCE_EMBEDDER>

Positional Args:
    LANG: Language code (e.g. bi, cbk-zam, jam, pih, tpi)
    MODEL_PATH: Path to the model checkpoint
    MODEL_NAME: Name of the model (e.g. bert-base-multilingual-cased; xlm-roberta-base; xlm-roberta-large; bert-base-cased; bert-large-cased')
    SENTENCE_EMBEDDER: Sentence embedder (e.g. bert-base-nli-mean-tokens; bert-large-nli-mean-tokens; xlm-r-bert-base-nli-mean-tokens; xlm-r-100langs-bert-base-nli-mean-tokens)

Note: 
    Calls Python3 by default. If you're using a virtual environment, make sure to activate it before running this script.
EOF
}
if [ "$#" -ne 4 ]; then
    usage
    exit 1
fi


# Main script
LANG=$1
MODEL_PATH=$2
MODEL_NAME=$3
SENTENCE_EMBEDDER=$4

log_dir="log_infer"
data_dir="data/relation_extraction"
proper_dir="data/relation_extraction/properties"
model_dir="save_models"
output_dir="output"

property_file="${proper_dir}/${LANG}.json"

mkdirs "$output_dir"
mkdirs "$log_dir"

# Log time
log_file="${log_dir}/${mm}_${ss}.log"
> "$log_file"
echo "$mm" | tee -a "$log_file"
echo "$ss" | tee -a "$log_file"

echo "Redirect to the ZS_BERT directory ..."
python3 src/ZS_BERT/model/inference.py data/relation_extraction/"$LANG".json "$property_file" "$output_dir" "$SENTENCE_EMBEDDER" "$MODEL_NAME" "$MODEL_PATH" | tee -a "$log_file"