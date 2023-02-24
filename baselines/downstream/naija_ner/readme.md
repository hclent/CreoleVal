## Pipeline for running the Naija MasakhaNER experiments:

Download the data here:

https://github.com/masakhane-io/masakhane-ner/tree/main/MasakhaNER2.0/data/pcm

Ensure that the data filepaths in `configs/ner_naija.json` and `naija_ner_test_$bert.slurm` match the data filepaths on your system.

Train the model:

```
sbatch naija_ner_train_mbert.slurm
sbatch naija_ner_train_mt5.slurm
sbatch naija_ner_train_xlmr.slurm
```
The model.pt file will be stored in: 
`baselines/logs/naija-ner-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch naija_ner_test_mbert.slurm
sbatch naija_ner_test_mt5.slurm
sbatch naija_ner_test_xlmr.slurm
```
