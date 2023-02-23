## Pipeline for running the AfriSenti experiments:

Download the data here:
- Train: https://github.com/afrisenti-semeval/afrisent-semeval-2023/blob/main/SubtaskA/train/pcm_train.tsv
- Dev: https://github.com/afrisenti-semeval/afrisent-semeval-2023/blob/main/SubtaskA/dev/pcm_dev.tsv
- Test: https://github.com/afrisenti-semeval/afrisent-semeval-2023/blob/main/SubtaskA/test/pcm_test.tsv

Ensure that the data filepaths in `configs/senti_afri.json` and `afri_senti_test_$bert.slurm` match the data filepaths on your system.

Train the model:

```
sbatch afri_senti_train_mbert.slurm
sbatch afri_senti_train_mt5.slurm
sbatch afri_senti_train_xlmr.slurm
```
The model.pt file will be stored in: 
`baselines/logs/afri-senti-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch afri_senti_test_mbert.slurm
sbatch afri_senti_test_mt5.slurm
sbatch afri_senti_test_xlmr.slurm
```
