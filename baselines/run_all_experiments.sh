#!/usr/bin/env bash

### This file serves as a reference for how to run all the baseline experiments.

export MACHAMP_DIR=./machamp  # replace with path to MaChAmp repo folder if necessary

models=(mbert mt5 xlmr)

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
train_and_predict_all_models

# Naija NER
task=ner_naija
testfile='data/naija/masakhane-ner-pcm/test.txt'
train_and_predict_all_models

# Naija UPOS
task=upos_naija
testfile='data/naija/naija-sud/pcm_nsc-ud-test.conllu'
train_and_predict_all_models

# Oyewusi
task=senti_oyewusi
testfile='data/Oyewusi/oyewusi_test.tsv'
train_and_predict_all_models

# Singlish UPOS
task=upos_singlish
testfile='data/singlish/test.conll'
train_and_predict_all_models

# WikiAnn NER
languages=(bi ht pih tpi cbk_zam pap sg)
for lang in $languages; do
    task=ner_wikiann_${lang}
    testfile="data/WikiAnn_data/${lang}/$(echo $lang | sed 's/_/-/')-test.txt"
    train_and_predict_all_models
done

# Jamaican NLI
testfile='data/jam-nli-data/jamnli-test.tsv'
for model in ${models[@]}; do
    ./train_and_finetune.sh $model
    model_checkpoint=$(ls -td1 ./logs/nli_jamaican_${model}_finetune/*/ | head -1)
    ./predict.sh $model_checkpoint $testfile
done
