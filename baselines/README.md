## Step 1: download and install machamp

```
git clone https://github.com/machamp-nlp/machamp.git
pip install requirements.txt #do this in the conda env
```

## Step 2: clean the data files that we need

``` 
python machamp/scripts/misc/cleanconl.py *.conllu
sed -i 's/\s/\t/g' data/eval/naija/masakhane-ner-pcm/*.txt
```

## Step 3:
Update data paths in `configs/ner_naija.json` and `configs/upos_singlish` unless they are in a folder called data in the directory in which you are running the code.
Update slurm gpu info if needed as well as `$codebase` and `$loggingdir` variables in `train_downstream.sh` and `predict_test.sh`
run jobs, example:
```
sbatch downstream/train_downstream.sh mbert baseline naija creoleonly
```

when it's done:
```
sbatch downstream/predict_test.sh mbert baseline naija creoleonly
```

Voila! The results are in the directory in which you run everything, you have a logs dir with subdirs with models and test sets.
