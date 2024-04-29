#!/usr//bin/bash

# Usage
usage() {
cat << EOF
Usage:
    bash run_inference.sh <LANG> <MODEL_PATH>
    LANG: language code (e.g. bi, cbk-zam, jam, pih, tpi)
    MODEL_PATH: path to the model checkpoint

    Note: Calls Python3 by default. If you're using a virtual environment, make sure to activate it before running this script.
EOF
}
if [ "$#" -ne 2 ]; then
    usage
    exit 1
fi


# Main script
LANG=$1
MODEL_PATH=$2
# "../../../model/best_f1_0.7081677743338072_wiki_epoch_4_m_5_alpha_0.4_gamma_7.5"

echo "Redirect to the ZS_BERT directory ..."
cd src/ZS_BERT/model
python3 inference.py ../../../data/relation_extraction/"$LANG".json ../../../data/relation_extraction/properties/"$LANG".json $MODEL_PATH

