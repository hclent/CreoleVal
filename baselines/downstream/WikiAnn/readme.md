## Pipeline for running the WikiAnn experiments:

Data is in the `data/Wikiann_data/$lang` folder. Ensure that the data filepaths in `configs/ner_wikiann_$lang.json` and `wikiann_$lang_test_$bert.slurm` match the data filepaths on your system. 

Train the model:

```
sbatch wikiann_$lang_ner_train_mbert.slurm
sbatch wikiann_$lang_ner_train_mt5.slurm
sbatch wikiann_$lang_ner_train_xlmr.slurm
```
The model.pt file will be stored in: 
`baselines/logs/wikiann_$lang-$bert-baseline/<date/time when you ran the experiment>`

Update the path to the respective model.pt files in the respective slurm test files on this line:

```
python $codebase/predict.py $serialized_dir_a/<path to model.pt> $input_file $output_file --device 0 
```
Test the model:

```
sbatch wikiann_$lang_ner_test_mbert.slurm
sbatch wikiann_$lang_ner_test_mt5.slurm
sbatch wikiann_$lang_ner_test_xlmr.slurm
```
