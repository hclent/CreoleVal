## Pipeline for running the Jamaican-NLI experiments:

1) Training the model on the GLUE MNLI dataset. Run the jam_mnli_<bert>.slurm file - which will create a folder named jamaican_nli_$bert_training in the logs dir with the model.pt file.

2) Finetune the model on the jamaican-nli dataset. Update the path to the model.pt file in the jam_nli_finetune_$bert.slurm file on this line and run the file:

```
python $codebase/train.py --parameters_config $parameters_config --dataset_config $downstreamdir/configs/$task\_$finetune.json --retrain $loggingdir/logs/$finetune-$task-$bert-training/<path to model.pt>

```

3) To test the model, update the path to the finetuned model.pt file in the logs dir in the jam_test_$bert.slurm file on this line and run the file:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 

```
