# Baselines



## Download and install machamp:

```
git clone https://github.com/machamp-nlp/machamp.git
pip install -r requirements.txt #do this in a conda env called 'creole'
```
PS. There might be issues with the jsonnet installation - in which case just run the command `conda install -c conda-forge jsonnet` in the creole env.

Experiments run with commit `c1bde68e` of machamp.

## Steps for running individual experiments

### AfriSenti

- **Data**: [AfriSenti-SemEval Shared Task 12](https://github.com/afrisenti-semeval/afrisent-semeval-2023)
  - Download script: `download_afrisenti.sh`
- **Dataset Config**: `downstream/configs/senti_afri.json`
- **Model Config**:
  - `params_mbert.json`
  - `params_mt5.json`
  - `params_xlmr.json`

### Jamaican

- **Data**: [GLUE MNLI](https://github.com/nyu-mll/GLUE-baselines) + fine-tuning data in `data/jam-nli-data`
  - Download: From `/baselines` folder, run:
    ```bash
    $ wget https://github.com/nyu-mll/GLUE-baselines/raw/master/download_glue_data.py
    $ python download_glue_data.py --data_dir data/glue --tasks MNLI
    ```
- **Dataset Config**: `downstream/configs/nli_glue.json`

TODO

### Oyewusi

- **Data**: `data/Oyewusi` (in this repo)
- **Dataset Config**: `downstream/configs/senti_oyewusi.json`
- **Model Config**:
  - `params_mbert.json`
  - `params_mt5.json`
  - `params_xlmr.json`

### Naija NER

- **Data**: [MasakhaNER 2.0](https://github.com/masakhane-io/masakhane-ner/tree/main/MasakhaNER2.0/data/pcm/)
  - Download script: `download_masakhaner.sh`
- **Dataset Config**: `downstream/configs/ner_naija.json`
- **Model Config**:
  - `params_mbert.json`
  - `params_mt5.json`
  - `params_xlmr.json`

### Naija UPOS

- **Data**: [UD Naija-NSC](https://github.com/UniversalDependencies/UD_Naija-NSC)
  - Download script: `download_ud_naija.sh`
- **Dataset Config**: `downstream/configs/upos_naija.json`
- **Model Config**:
  - `params_mbert.json`
  - `params_mt5.json`
  - `params_xlmr.json`

### Singlish UPOS

- **Data**: [Singlish STB-ACL](https://github.com/wanghm92/Sing_Par/tree/master/ACL17_dataset/treebank/gold_pos)
  - Download script: `download_singlish_upos.sh`
- **Dataset Config**: `downstream/configs/upos_naija.json`
- **Model Config**:
  - `params_mbert.json`
  - `params_mt5.json`
  - `params_xlmr.json`




## Points to remember while running the experiments:
- The `downstream/configs` folder contains all the configuration files for the model hyperparameters and datasets.
- Filenames beginning with `params_` contain model hyperparameters where the pretrained transformer models can be changed by changing the following line to any huggingface transformer model:
```
{
  "transformer_model": "bert-base-multilingual-cased",
```
- Filenames beginning with `ner`, `senti`, `nli` and `upos` contain the data filepaths and configurations. Ensure that filepath mentioned in these files are same as the filepaths to the data files on your system.
- Update slurm gpu info if needed as well as `$codebase` and `$loggingdir` variables in the train and test slurm files. Example job (presuming it is submitted from inside the folder where the slurm file is located):
```
sbatch naija_ner_train_mbert.slurm
```
And then to test:
```
sbatch naija_ner_test_mbert.slurm
```
- Running a train file will create a `baselines/logs` dir where all your models, metrics, scores and test files will be stored.
