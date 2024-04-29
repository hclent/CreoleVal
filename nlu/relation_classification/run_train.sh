cd ./CreoleRE
source activate RE



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
        python3 ./relation_classification/ZS_BERT/model/train_wiki.py -se "$ss" -t "$mm" -cr bi cbk-zam jam pih tpi --model_saves ./relation_classification/save_models --Wiki_ZSL_data ./relation_classification/data/Wiki-ZSL --Creole_data ./relation_classification/data/relation_extraction --prop_list_path ./relation_classification/ZS_BERT/resources/property_list.html  | tee -a "$log_file"
    done
done
