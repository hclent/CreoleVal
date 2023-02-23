Pipeline for running the Jamaican-NLI experiments:

1) Training the model on the GLUE MNLI dataset. Run the jam_mnli_<bert>.slurm file - which will create a folder named jamaican_nli_$bert-training in the logs dir with the model.pt file.

2) Finetune the model on the jamaican-nli dataset. Update the path to the model.pt file in the jam_nli_finetune_$bert.slurm file. 
