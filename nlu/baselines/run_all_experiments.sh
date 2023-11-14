#!/usr/bin/env bash

### This file serves as a reference for how to run all the baseline experiments.

export MACHAMP_DIR=./machamp  # replace with path to MaChAmp repo folder if necessary

models=(
    xlm-r+CreoleEval_all
    mbert
    mt5
    xlmr
    xlm-r+CreoleEval_eng
)

train_and_predict_all_models() {
    for model in ${models[@]}; do
        ./train.sh $task $model
        model_checkpoint=$(ls -td1 ./logs/${task}_${model}_baseline/*/ | head -1)
        ./predict.sh $model_checkpoint $testfile
    done
}

# AfriSenti
task=senti_afri
testfile='data/afrisenti/pcm_test.tsv'
./download_afrisenti.sh
train_and_predict_all_models

# Naija NER
task=ner_naija
testfile='data/naija/masakhane-ner-pcm/test.txt'
./download_masakhaner.sh
train_and_predict_all_models

# Naija UPOS
task=upos_naija
testfile='data/naija/naija-sud/pcm_nsc-ud-test.conllu'
./download_ud_naija.sh
train_and_predict_all_models

# Oyewusi
task=senti_oyewusi
testfile='data/Oyewusi/oyewusi_test.tsv'
train_and_predict_all_models

# Singlish UPOS
task=upos_singlish
testfile='data/singlish/test.conll'
./download_singlish_upos.sh
train_and_predict_all_models

# Jamaican NLI
testfile='data/jam-nli-data/jamnli-test.tsv'
wget -nc https://github.com/nyu-mll/GLUE-baselines/raw/master/download_glue_data.py
python download_glue_data.py --data_dir data/glue --tasks MNLI
bash recut_mnli.sh
for model in ${models[@]}; do
    ./train_and_finetune_jamnli.sh $model
    model_checkpoint=$(ls -td1 ./logs/nli_jamaican_${model}_finetune/*/ | head -1)
    ./predict.sh $model_checkpoint $testfile
done

# WikiAnn NER
languages=(bi ht pih tpi cbk_zam pap sg)
for lang in ${languages[@]}; do
    task=ner_wikiann_${lang}
    testfile="data/WikiAnn_data/${lang}/$(echo $lang | sed 's/_/-/')-test.txt"
    case $lang in
		"bi") ANCESTOR="eng";;
		"cbk-zam") ANCESTOR="spa";;
		"ht") ANCESTOR="fra";;
		"pap") ANCESTOR="por";;
		"pih") ANCESTOR="eng";;
		"sg") ANCESTOR="ngb";;
		"tpi") ANCESTOR="eng";;
		*)
			echo "Unknown language $lang"
			exit
		;;
	esac
	models=(
        xlm-r+CreoleEval_all
        mbert
        mt5
        xlmr
        xlm-r+CreoleEval_$ANCESTOR
    )
    echo "Using models ${models[@]}"
    train_and_predict_all_models
done
