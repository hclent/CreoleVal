# CreoleM2M 

### Pre-requisites 

**Bible Data**: Because Bible data is copy-righted, we unfortunately cannot share it. Please reach out to [the authors of "Creating a massively parallel Bible corpus](https://aclanthology.org/L14-1215/).

**YANMTT**: You will need `YANMTT` to decode models we have trained.

If you dont use YANMTT, you can always use huggingface transformers to fine-tune and decode models yourself.

### Data preperation (UNDER CONSTRUCTION)

The Creole language codes are present in `creoles_list.txt`.

**We will update this section with further details on how to reproduce our train-dev-test sets.**

Our data is in the following format: 
(a) `train.<creole code>-eng.<creole code>` and `train.<creole code>-eng.eng` are the training files,

(b) `train.<creole code>`, `train.eng` for the n-way parallel training segments of the aforementioned data, 

(c) `dev.<creole code>`, `dev.eng` for the n-way parallel development set segments of the aforementioned data,

(d) `test.<creole code>`, `test.eng` for the n-way parallel test set segments of the aforementioned data.

All results in the paper are calculated on the test set mentioned above.

### Experiments

#### Step 0: Acquire data and split into train-dev-test (more details coming soon!)

#### Step 1: Install [YANMTT](https://github.com/prajdabre/yanmtt)

#### Step 2: Train tokenizer 
(see `creole_mt_train_tokenizer.sh`)

#### Step 3: Train model 
(see `creole_mt_train.sh`)

#### Step 4: Decode and evaluate model 
(see `creole_mt_decode_eval.sh`)