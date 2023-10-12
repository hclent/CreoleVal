#!/usr/bin/env bash

# Adds keys that are expected by MaChAmp v0.4.2
# Needs:
# - jq
# - moreutils (for `sponge`)
# - `npm install --global strip-json-comments-cli`

for paramfile in params_*.json ; do
    echo "Updating $paramfile"
    strip-json-comments $paramfile |
        jq '. + {"reset_transformer_model": false} | .batching.shuffle = true | .batching.diverse = false' |
        sponge $paramfile
done
