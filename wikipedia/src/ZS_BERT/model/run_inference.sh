#!/bin/bash

python inference.py ../../data/entExt/pap.json ../../data/properties/pap.json ../output

python inference.py ../../data/entExt/pih.json ../../data/properties/pih.json ../output

python inference.py ../../data/entExt/sg.json ../../data/properties/sg.json ../output

python inference.py ../../data/entExt/tpi.json ../../data/properties/tpi.json ../output


python inference.py ../../data/relation_extraction/post-processed/bi.json ../../data/relation_extraction/properties/bi.json ../output
