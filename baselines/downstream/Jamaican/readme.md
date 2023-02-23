## Pipeline for running the Jamaican-NLI experiments:

Download the GLUE MNLI data here:

https://github.com/nyu-mll/GLUE-baselines/blob/master/download_glue_data.py

Ensure that the train and dev data filepaths in `configs/nli_glue.json` match the data filepaths in your system. 

Train the pretrained transformer model on the GLUE MNLI dataset:

```
sbatch jam_mnli_mbert.slurm
sbatch jam_mnli_mt5.slurm
sbatch jam_mnli_xlmr.slurm
```
The model.pt file will be stored in:

`baselines/logs/nli-jamaican-$bert-training/<date/time when you ran the experiment>`

Update the above path to the model.pt file in the `jam_nli_finetune_$bert.slurm` files on this line:

```
python $codebase/train.py --parameters_config $parameters_config --dataset_config $downstreamdir/configs/$task\_$finetune.json --retrain $loggingdir/logs/$finetune-$task-$bert-training/<path to model.pt>

```
The jamaican-nli finetuning dataset is available in `data/jam-nli-data`. Ensure that the data filepaths in `configs/nli_jamaican.json` and `jam_test_$bert.slurm` match the data filepaths on your system. 

Finetune the model:

```
sbatch jam_nli_finetune_mbert.slurm
sbatch jam_nli_finetune_mt5.slurm
sbatch jam_nli_finetune_xlmr.slurm
```
The finetuned model.pt will be stored in: 

`baselines/logs/nli-jamaican-$bert-finetune/<date/time when you ran the experiment>`

Update the path to the finetuned model.pt file in the `jam_test_$bert.slurm` files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 

```
Test the model:

```
sbatch jam_test_mbert.slurm
sbatch jam_test_mt5.slurm
sbatch jam_test_xlmr.slurm
```
