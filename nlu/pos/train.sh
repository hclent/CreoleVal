#!/usr/bin/env bash

set -Eeu

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MACHAMP_DIR="$SCRIPTDIR/../../submodules/machamp"

function script_usage() {
    cat << EOF
Usage: train.sh <TASK> <MODEL> <[SEED]>

Arguments:
    TASK                Task to train on; should be the name of a config file
                        (without the extension) in the configs/ folder, e.g.
                        'ner_naija' or 'senti_afri'.
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

if [[ $# -lt 2 || $# -gt 3 ]]; then
    msg "Error: Found $# positional arguments; expected 2 or 3\n"
    script_usage
    exit 1
fi

# TEST IF MACHAMP_DIR exists, if not then give message to pull submodules
if [ ! -d "$MACHAMP_DIR" ]; then
    msg "Error: MaChAmp not found, did you pull submodules? <git submodule update --init --recursive>"
    exit 1
fi

task="$1"
task_config="$SCRIPTDIR/configs/$task.json"
if [[ ! -f "$task_config" ]]; then
    msg "Error: Found no configuration file for task '$task'"
    msg "  expected: $task_config"
    exit 2
fi

model="$2"
model_config="$SCRIPTDIR/configs/params_$model.json"
if [[ ! -f "$model_config" ]]; then
    msg "Error: Found no configuration file for model '$model'"
    msg "  expected: $model_config"
    exit 2
fi

seed="${3-$RANDOM}"

# Important for relative path names in the config files
cd "$SCRIPTDIR"

python3 "$MACHAMP_DIR"/train.py \
       --parameters_config "$model_config" \
       --dataset_config "$task_config" \
       --name "${task}_${model}_baseline" \
       --seed $seed
