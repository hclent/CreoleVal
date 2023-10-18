mkdirs() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        mkdirs "$(dirname "$dir")"
        mkdir "$dir"
    fi
}



model=('bert-base-multilingual-cased' 'xlm-roberta-base' 'xlm-roberta-large' 'bert-base-cased' 'bert-large-cased')
sentence=('bert-base-nli-mean-tokens' 'bert-large-nli-mean-tokens' 'xlm-r-bert-base-nli-mean-tokens' 'xlm-r-100langs-bert-base-nli-mean-tokens')
Creole=('bi' 'cbk-zam' 'jam' 'pih' 'tpi')

log_dir="./relation_classification/log_infer"
data_dir="./relation_classification/data/relation_extraction"
proper_dir="./relation_classification//data/relation_extraction/properties/"
model_dir="./relation_classification/save_models/"
output_dir="./relation_classification/output"
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
            CUDA_VISIBLE_DEVICES=0 python ./relation_classification/ZS_BERT/model/inference.py "$data_file" "$proper_file" "$output_dir" "$ss" "$mm" "$best_model" | tee -a "$log_file"
        done
    done
done