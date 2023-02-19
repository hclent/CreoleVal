#!/bin/bash

python src/RelationExtraction/stretch_data.py ZS_BERT/output/bi.json data/annotated_wikidumps/bi_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/cbk-zam.json data/annotated_wikidumps/cbk-zam_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/gcr.json data/annotated_wikidumps/gcr_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/jam.json data/annotated_wikidumps/jam_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/pap.json data/annotated_wikidumps/pap_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/pih.json data/annotated_wikidumps/pih_anno.csv
python src/RelationExtraction/stretch_data.py ZS_BERT/output/sg.json data/annotated_wikidumps/sg_anno.csv

python src/RelationExtraction/stretch_data.py ZS_BERT/output/tpi.json data/annotated_wikidumps/tpi_anno.csv
