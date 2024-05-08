#!/bin/bash

echo "Remember:
  - Create and activate your corresponding Conda environment before running this script;
  - This script calls Python3 by default;
"

# Download data
UKP="data/ukp/wiki_all.json"
FILE_ID="1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK"
if test -f $UKP;
  then
    echo "UKP file exists ..."
  else
    echo "downloading UKP English data... to data/ukp/wiki_all.json"
    wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ELFGUIYDClmh9GrEHjFYoE_VI1t2a5nK' -O $UKP
fi

# test if relation_classification/src/ZS_BERT/Wiki-ZSL/train.json exists
if [ ! -f src/ZS_BERT/Wiki-ZSL/train.json ]; 
  then
    wget https://huggingface.co/datasets/yiyic/ukp_m5/resolve/main/train.json -O src/ZS_BERT/Wiki-ZSL/train.json
  else
    echo "Found src/ZS_BERT/Wiki-ZSL/test.json ..."
fi

if [ ! -f src/ZS_BERT/Wiki-ZSL/test.json ]; 
  then
    wget https://huggingface.co/datasets/yiyic/ukp_m5/resolve/main/test.json -O src/ZS_BERT/Wiki-ZSL/test.json
  else
    echo "Found src/ZS_BERT/Wiki-ZSL/test.json ..."
fi

mkdirs() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdirs "$(dirname "$dir")"
        mkdir "$dir"
    fi
}


model=('bert-base-multilingual-cased' 'xlm-roberta-base' 'xlm-roberta-large' 'bert-base-cased')
sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
log_dir="./relation_classification/log"

for mm in "${model[@]}"; do
    for ss in "${sentence[@]}"; do
        mkdirs "$log_dir"
        log_file="${log_dir}/${mm}_${ss}.log"
        > "$log_file"
        echo "$mm" | tee -a "$log_file"
        echo "$ss" | tee -a "$log_file"
        python3 src/ZS_BERT/model/train_wiki.py -se "$ss" -t "$mm" -cr bi cbk-zam jam tpi --model_saves saved_models --Wiki_ZSL_data src/ZS_BERT/Wiki-ZSL --Creole_data data/relation_extraction --prop_list_path src/ZS_BERT/resources/property_list.html  | tee -a "$log_file"
    done
done