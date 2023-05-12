#!/usr/bin/env bash

set -Eeu

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function script_usage() {
    cat << EOF
Usage: train_and_finetune_jamnli.sh MODEL [SEED]

Arguments:
    MODEL               Model type to use; one of: mbert, mt5, xlmr
    SEED                (optional) Random seed to pass to MaChAmp.

To point the script to the MaChAmp folder, either:
    - Set the environment variable MACHAMP_DIR
    - Create a symlink to the folder under
        $SCRIPTDIR/machamp
EOF
}

function msg() {
    echo >&2 -e "${1-}"
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    msg "Error: Found $# positional arguments; expected 1 or 2\n"
    script_usage
    exit 1
fi

model="$1"
model_pretrain_config="$SCRIPTDIR/configs/params_nli_$model.json"
model_finetune_config="$SCRIPTDIR/configs/params_jamnli_$model.json"
if [[ ! -f "$model_pretrain_config" || ! -f "$model_finetune_config" ]]; then
    msg "Error: Found no configuration file for model '$model'"
    msg "  expected: $model_pretrain_config"
    msg "            $model_finetune_config"
    exit 2
fi

seed="${2-$RANDOM}"
task_pretrain_config="$SCRIPTDIR/configs/nli_glue.json"
task_finetune_config="$SCRIPTDIR/configs/nli_jamaican.json"

if [[ ! -f "${MACHAMP_DIR:=$SCRIPTDIR/machamp}/train.py" ]]; then
    msg "Error: train.py not found -- did you make a symlink or set MACHAMP_DIR?"
    msg "  expected: $MACHAMP_DIR/train.py"
    exit 1
fi

# Important for relative path names in the config files
cd "$SCRIPTDIR"

# Pre-training
python "$MACHAMP_DIR"/train.py \
       --parameters_config "$model_pretrain_config" \
       --dataset_config "$task_pretrain_config" \
       --name "nli_jamaican_${model}_pretrain" \
       --seed $seed

# Find the trained pre-trained model
# !! ASSUMES THAT NO OTHER PROCESS HAS TRAINED A MODEL !!
# !! WITH THE SAME NAME IN THE MEANTIME                !!
model_pretrained=$(ls -td1 "$SCRIPTDIR/logs/nli_jamaican_${model}_pretrain"/*/ | head -1)

if [[ ! -f "$model_pretrained/model.pt" ]]; then
    msg "Error: Pre-trained model file does not exist"
    msg "  expected: $model_pretrained/model.pt"
    return 1
fi

python "$MACHAMP_DIR"/train.py \
       --parameters_config "$model_finetune_config" \
       --dataset_config "$task_finetune_config" \
       --retrain "$model_pretrained/model.pt" \
       --name "nli_jamaican_${model}_finetune" \
       --seed $SEED
