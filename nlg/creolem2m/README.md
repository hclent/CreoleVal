# Creole MT README.

### Note 1: You will need YANMTT to decode models we have trained.
### Note 2: If you dont use YANMTT, you can always use huggingface transformers to fine-tune and decode models yourself.
### Note 3: The creole language codes are present in creoles_list.txt
### Note 4: The datasets folder contains all the training data: (a) train.<creole code>-eng.<creole code> and train.<creole code>-eng.eng are the training files (b) train.<creole code>, train.eng for the n-way parallel training segments of the aforementioned data, (c) dev.<creole code>, dev.eng for the n-way parallel development set segments of the aforementioned data, (d) test.<creole code>, test.eng for the n-way parallel test set segments of the aforementioned data.
### Note 5: All results in the paper are calculated on the test set mentioned in note 4.


## Step 1: Install YANMTT (https://github.com/prajdabre/yanmtt)

## Step 2: Train tokenizer (see creole_mt_train_tokenizer.sh)

## Step 3: Train model (see creole_mt_train.sh)

## Step 4: Decode and evaluate model (see creole_mt_decode_eval.sh)