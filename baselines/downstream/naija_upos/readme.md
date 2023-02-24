## Pipeline for running the Naija UPOS experiments:

Download the data here:

https://github.com/UniversalDependencies/UD_Naija-NSC

Ensure that the data filepaths in `configs/upos_naija.json` and `naija_upos_test_$bert.slurm` match the data filepaths on your system.

Train the model:

```
sbatch naija_upos_train_mbert.slurm
sbatch naija_upos_train_mt5.slurm
sbatch naija_upos_train_xlmr.slurm
```
The model.pt file will be stored in: 

`baselines/logs/naija-upos-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch naija_upos_test_mbert.slurm
sbatch naija_upos_test_mt5.slurm
sbatch naija_upos_test_xlmr.slurm
```
