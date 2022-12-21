#!/bin/bash
# Purpose: Read Comma Separated CSV File
# Author: Vivek Gite under GPL v2.0+
# ------------------------------------------
INPUT=/Users/yiyichen/Documents/experiments/datasets/wikidumps/full_wikipages_qcodes_only.csv
COUNTER=0
cat $INPUT | tr -d '\r' | while read qcode
do
  let COUNTER++
  wdtaxonomy $qcode -P P31 -f json -o output/document_classification/$qcode.json
  printf "The value of the counter is COUNTER=%d\n" $COUNTER
done

