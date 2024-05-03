#!/usr/bin/env bash

set -Eeu

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
MACHAMP_DIR="$SCRIPTDIR/../../submodules/machamp"

function script_usage() {
    cat << EOF
Usage: predict.sh <MODELDIR> <INPUTFILE>

Positional Args:
    MODELDIR            Path to the trained model; usually of the form
                          ./logs/{task}-{model}-baseline/{date}/
    INPUTFILE           Input file for the model.

Predictions will be stored in MODELDIR/output.INPUTFILE
EOF
}

function msg() {
    echo >&2 -e "${1-}"
}

# TEST IF MACHAMP_DIR exists, if not then give message to pull submodules
if [ ! -d "$MACHAMP_DIR" ]; then
    msg "Error: MaChAmp not found, did you pull submodules? <git submodule update --init --recursive>"
    exit 1
fi

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

# Important for relative path names in the config files
cd "$SCRIPTDIR"

python3 ../../submodules/machamp/predict.py \
       "$modeldir/model.pt" \
       "$inputfile" \
       "$modeldir"/output.$(basename "$inputfile")
