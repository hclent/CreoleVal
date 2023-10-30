#!/usr/bin/env bash

set -Eeu

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

function script_usage() {
    cat << EOF
Usage: predict.sh MODELDIR INPUTFILE

Arguments:
    MODELDIR            Path to the trained model; usually of the form
                          ./logs/{task}-{model}-baseline/{date}/
    INPUTFILE           Input file for the model.

Predictions will be stored in MODELDIR/output.INPUTFILE

To point the script to the MaChAmp folder, either:
    - Set the environment variable MACHAMP_DIR
    - Create a symlink to the folder under
        $SCRIPTDIR/machamp
EOF
}

function msg() {
    echo >&2 -e "${1-}"
}

if [[ $# -ne 2 ]]; then
    msg "Error: Found $# positional arguments; expected 2\n"
    script_usage
    exit 1
fi

modeldir="$1"
if [[ ! -f "$modeldir/model.pt" ]]; then
    msg "Error: Trained model checkpoint not found"
    msg "  expected: $modeldir/model.pt"
    exit 2
fi

inputfile="$2"

if [[ ! -f "${MACHAMP_DIR:=$SCRIPTDIR/machamp}/predict.py" ]]; then
    msg "Error: predict.py not found -- did you make a symlink or set MACHAMP_DIR?"
    msg "  expected: $MACHAMP_DIR/predict.py"
    exit 1
fi

# Important for relative path names in the config files
cd "$SCRIPTDIR"

python "$MACHAMP_DIR"/predict.py \
       "$modeldir/model.pt" \
       "$inputfile" \
       "$modeldir"/output.$(basename "$inputfile")
