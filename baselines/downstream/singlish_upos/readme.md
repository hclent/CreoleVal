## Pipeline for running the Singlish UPOS experiments:

Download the data here:

https://github.com/wanghm92/Sing_Par/tree/master/ACL17_dataset/treebank/gold_pos

Ensure that the data filepaths in `configs/upos_singlish.json` and `singlish_upos_test_$bert.slurm` match the data filepaths on your system.

Train the model:

```
sbatch singlish_upos_train_mbert.slurm
sbatch singlish_upos_train_mt5.slurm
sbatch singlish_upos_train_xlmr.slurm
```
The model.pt file will be stored in: 
`baselines/logs/singlish-upos-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch singlish_upos_test_mbert.slurm
sbatch singlish_upos_test_mt5.slurm
sbatch singlish_upos_test_xlmr.slurm
```
