## Download and install machamp

```
git clone https://github.com/machamp-nlp/machamp.git
pip install -r requirements.txt #do this in a conda env called 'creole'
```
PS. There might be issues with the jsonnet installation - in which case just run the command `conda install -c conda-forge jsonnet` in the creole env.

## Steps for running individual experiments are in the respective folders.

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
