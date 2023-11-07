# CreoleM2M 

### Pre-requisite Bible data

We do not own this data, and it his highly confidential due to copy-right, and must not be shared publically.

If you are looking for **Bible Data** in general, please reach out to [the authors of "Creating a massively parallel Bible corpus](https://aclanthology.org/L14-1215/). Again, because Bible data is copy-righted, we unfortunately cannot share it publically. 

**If you have specific questions about the CreoleM2M data, please reach out to the authors.**


### Data preperation 

The Creole language codes are present in `creoles_list.txt`, and the dataset sizes are in `corpora_stats.txt`.

Our data is in the following format: 

(a) `train.<creole code>-eng.<creole code>` and `train.<creole code>-eng.eng` are the training files,

(b) `train.<creole code>`, `train.eng` for the n-way parallel training segments of the aforementioned data, 

(c) `dev.<creole code>`, `dev.eng` for the n-way parallel development set segments of the aforementioned data,

(d) `test.<creole code>`, `test.eng` for the n-way parallel test set segments of the aforementioned data.

All results in the paper are calculated on the test set mentioned above.

### Experiments

#### Step 0: Acquire Bible data and create train-dev-test splits. 

#### Step 1: Install [YANMTT](https://github.com/prajdabre/yanmtt)

You will need `YANMTT` to decode models we have trained. If you dont use `YANMTT`, you can always use huggingface transformers to fine-tune and decode models yourself.

#### Step 2: Train tokenizer 
(see `creole_mt_train_tokenizer.sh`)

#### Step 3: Train model 
(see `creole_mt_train.sh`)

#### Step 4: Decode and evaluate model 
(see `creole_mt_decode_eval.sh`)