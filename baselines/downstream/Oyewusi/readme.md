## Pipeline for running the Nigerian Pidgin Sentiment (Oyewusi) experiments:

Data is in the `data/Oyewusi` folder. Ensure that the data filepaths in `configs/senti_oyewusi.json` and `oyewusi_senti_test_$bert.slurm` match the data filepaths on your system. 

Train the model:

```
sbatch oyewusi_senti_train_mbert.slurm
sbatch oyewusi_senti_train_mt5.slurm
sbatch oyewusi_senti_train_xlmr.slurm
```
The model.pt file will be stored in: 
`baselines/logs/oyewusi-senti-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch oyewusi_senti_test_mbert.slurm
sbatch oyewusi_senti_test_mt5.slurm
sbatch oyewusi_senti_test_xlmr.slurm
```
