# CreoleM2M 

### Pre-requisites 


**We will update this section with a Google Form where you can request the data from us.**

**We do not own this data, and it his highly confidential due to copy-right, and must not be shared publically.**

Otherwise if you are looking for **Bible Data** in general, please reach out to [the authors of "Creating a massively parallel Bible corpus](https://aclanthology.org/L14-1215/). Again, because Bible data is copy-righted, we unfortunately cannot share it publically. 


**YANMTT**: You will need `YANMTT` to decode models we have trained.

If you dont use YANMTT, you can always use huggingface transformers to fine-tune and decode models yourself.

### Data preperation (UNDER CONSTRUCTION)

The Creole language codes are present in `creoles_list.txt`.

**GOOGLE FORM COMING SOON.**


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