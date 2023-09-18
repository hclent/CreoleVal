import argparse
from pudb import set_trace
import os, csv, json
import random
import numpy as np
from models import MyBertForMultipleChoice
import transformers
from transformers import AutoTokenizer, EarlyStoppingCallback
from datasets import Dataset, DatasetDict, load_dataset
from dataclasses import dataclass
from transformers.tokenization_utils_base import PreTrainedTokenizerBase, PaddingStrategy
from typing import Optional, Union
import torch
from torch.utils.tensorboard import SummaryWriter
from transformers.integrations import TensorBoardCallback
from transformers import AutoModelForMultipleChoice, TrainingArguments, Trainer
from tqdm import tqdm, trange
import evaluate

accuracy = evaluate.load("accuracy")
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-uncased")

transformers.logging.set_verbosity_debug()

"""
Working from this/these tutorials

https://huggingface.co/docs/transformers/v4.22.0/en/tasks/multiple_choice#multiple-choice
https://huggingface.co/transformers/v3.3.1/model_doc/auto.html?highlight=automodelformultiplechoice#transformers.AutoModelForMultipleChoice

"""

def parse_args():
    parser = argparse.ArgumentParser()

    #Data
    parser.add_argument("--data_dir", type=str, default="", help="path to directory with mctest files")
    parser.add_argument("--split", type=str, default="mc500.train", help="path to specific dataset") #TODO: maybe by default dont need this, so it always loads training data, idk

    #Output & Logging
    parser.add_argument("--tb_dir",type=str, default="/home/cs.aau.dk/az01dn/mcdata/tensorboard")
    parser.add_argument("--output_dir", type=str, default="/home/cs.aau.dk/az01dn/mcdata/results_mctest_eng")

    #Model
    parser.add_argument("--tokenizer", type=str, default="bert-base-multilingual-uncased")
    parser.add_argument("--from_pretrained", type=str, default="bert-base-multilingual-uncased")
    parser.add_argument("--from_checkpoint", type=str, default="")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"])

    #Training
    parser.add_argument("--action", type=str, default="train", choices=["train", "evaluate", "test"])
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--learning_rate", type=float, default=2e-5,
                        help="Former default was 5e-5")
    parser.add_argument("--weight_decay", type=float, default=0.01)


    # Evaluation
    parser.add_argument("--eval_batch_size", type=int, default=1)

    return parser.parse_args()
    

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


def preprocess_function(examples):
    story = [[context] * 4 for context in examples["story"]] #real!
    story = sum(story, [])
    choices = []

    q2a_lut = {}
    for q, a in zip(examples["question"], examples["text_answer"]):
        q2a_lut[q] = a
    
    sep_tok = tokenizer.sep_token

    for q, candidates in zip(examples["question"], examples["choices"]):
        answer = q2a_lut[q]
        for option in candidates:
            choices.append(f"{q} {sep_tok} {option}") #real!
            #choices.append(f"{q} {sep_tok} {answer} {sep_tok} {option}") #This is for debugging only. We should get 100% Acc if we add the answer
    tokenized_examples = tokenizer(story, choices, truncation=False)
    bb = {k: [v[i : i + 4] for i in range(0, len(v), 4)] for k, v in tokenized_examples.items()}
    return bb

@dataclass
class DataCollatorForMultipleChoice:
    tokenizer: PreTrainedTokenizerBase
    max_len = 512

    def __call__(self, features):
        label_name = "label"
        labels = [feature.pop(label_name) for feature in features]
        batch_size = len(features)
        num_choices = 4
        flattened_features = [
            [{k: v[i] for k, v in feature.items()} for i in range(num_choices)] for feature in features]
        flattened_features = sum(flattened_features, []) #`encoded_inputs` for the batch [{'input_ids': [], 'token_type_ids': [], 'attention_mask': []}]

        # Truncate + Pad 

        #my own hacky truncation here 
        truncated_features = []

        for encoded_input in flattened_features:
            if len(encoded_input['input_ids']) < self.max_len:
                truncated_features.append(encoded_input)
            else:
                trunc_input_ids = encoded_input['input_ids'][:self.max_len]
                trunc_token_type_ids = encoded_input['token_type_ids'][:self.max_len] #TODO: COMMENT OUT FOR XLMR
                trunc_attention_mask = encoded_input['attention_mask'][:self.max_len]
                truncated_encoded_input = {'input_ids': trunc_input_ids, 'token_type_ids': trunc_token_type_ids , 'attention_mask': trunc_attention_mask}
                truncated_features.append(truncated_encoded_input)

        #Pad a single input/batch of inputs
        batch = self.tokenizer.pad(
            truncated_features,
            padding = True,
            max_length= self.max_len,
            return_tensors="pt",
            )

        batch = {k: v.view(batch_size, num_choices, -1) for k, v in batch.items()}
        labels_as_ints = [int(l) for l in labels] #make sure these are numbers
        batch["labels"] = torch.tensor(labels_as_ints, dtype=torch.int64)
        input_ids = batch["input_ids"] 
        return batch 


def main():
    args = parse_args()

    seed = args.seed

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    device = torch.device(args.device)
    if args.device == "cuda":
        torch.cuda.manual_seed_all(seed)
        print('There are %d GPU(s) available.' % torch.cuda.device_count())
        print('We will use the GPU:', torch.cuda.get_device_name(0))
    else:
        print('Running on cpu.')
        print('Killing this job then!')
        exit(333)

    data_path = args.data_dir
    split = args.split

    examples = load_dataset(f"{data_path}")
    print(f"****** EXAMPLES ******")
    print(examples)

    tokenized_mct = examples.map(preprocess_function, batched=True)
   
    data_collator = DataCollatorForMultipleChoice(tokenizer) #

    if args.action == "train":
        model = AutoModelForMultipleChoice.from_pretrained(args.from_pretrained).to(device)
        #######model = MyBertForMultipleChoice.from_pretrained(args.from_pretrained).to(device) #for debugging wooooo

        #init tensorboard for tracking
        experiment_sub_dir = f"mbert_lr{args.learning_rate}_wd{args.weight_decay}"
        writer = SummaryWriter(os.path.join(args.tb_dir, experiment_sub_dir))
        callback = TensorBoardCallback(writer)
        
        early_stopping = EarlyStoppingCallback(early_stopping_patience=10, early_stopping_threshold = 0.001)

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir),   
            save_strategy= "epoch",
            evaluation_strategy="epoch",
            learning_rate=args.learning_rate,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.batch_size,
            num_train_epochs=args.num_epochs,
            weight_decay=args.weight_decay,
            load_best_model_at_end = True,
            logging_steps=100,
            #logging_dir=f"dummy/{experiment_sub_dir}",
            logging_first_step = True
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_mct["train"],
            eval_dataset=tokenized_mct["validation"],
            tokenizer=tokenizer,
            data_collator=DataCollatorForMultipleChoice(tokenizer=tokenizer),
            callbacks=[callback, early_stopping],
            compute_metrics=compute_metrics,
            #logging_steps=100,
            #tb_writer=writer, 
        )
        print(f"DEVICE: {device}") 
        if device == "cuda":
            model.cuda()
        
        train_result = trainer.train()
        
        writer.close()

    elif args.action == "evaluate":

        #load trained model
        model = AutoModelForMultipleChoice.from_pretrained(args.from_checkpoint).to(device) 
        #####model = MyBertForMultipleChoice.from_pretrained(args.from_checkpoint).to(device)

        experiment_sub_dir = f"mbert_lr{args.learning_rate}_wd{args.weight_decay}"
        #writer = SummaryWriter(os.path.join(args.tb_dir, experiment_sub_dir))
        #callback = TensorBoardCallback(writer)

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir),   
            save_strategy="epoch",
            evaluation_strategy="epoch",
            learning_rate=args.learning_rate,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.batch_size,
            num_train_epochs=args.num_epochs,
            weight_decay=args.weight_decay,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_mct["train"],
            eval_dataset=tokenized_mct["validation"],
            tokenizer=tokenizer,
            data_collator=DataCollatorForMultipleChoice(tokenizer=tokenizer),
            #callbacks=[callback]
        )

        if device == "cuda":
            model.cuda()

        # Eval!
        model.eval()

        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0
        nb_eval_batches = 0 

        preds_list = []
        true_list = []

        dev_dataloader = trainer.get_eval_dataloader() #use the trainer to get the collated dev data
        for batch in tqdm(dev_dataloader, desc="Evaluating"):
            with torch.no_grad():

                inputs = {
                    "input_ids": batch["input_ids"].to(args.device),
                    "attention_mask": batch["attention_mask"].to(args.device),
                    "token_type_ids": batch["token_type_ids"].to(args.device),
                    "labels": batch["labels"].to(args.device),
                }

                outputs = model(**inputs)
                tmp_eval_loss, logits = outputs[:2]
                eval_loss += tmp_eval_loss.mean().item()

            logits = logits.detach().cpu().numpy()
            preds = np.argmax(logits, axis=1)
            print(f"[eval] predictions: {preds}")
            [preds_list.append(p) for p in preds]
            label_ids = inputs["labels"].to("cpu").numpy()
            print(f"[eval] labels: {label_ids}")
            [true_list.append(l) for l in label_ids]

            
            tmp_eval_accuracy = (preds == label_ids).astype(np.float32).mean().item() #BATCH-wise accuracy
            """
            ##########3 DEBUGGING #########
            if tmp_eval_accuracy != 1.0:
                #set_trace()
                print(f"****** WRONG ********")
                print(f"tmp_acc: {tmp_eval_accuracy}")
                print(f"true: {label_ids}")
                print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10].tolist()))
                print(logits)
                print(f"predicted: {preds}")
                print(tokenizer.convert_ids_to_tokens(batch[0][0][int(preds)][:-10].tolist()))
            else:
                print(f"****** CORRECT ********")
                print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10].tolist()))
                print()
            print(f"-----"*10)
            print(tmp_eval_accuracy)
            print(f"idk somethingggggg ... {accuracy(logits, label_ids)}")
            ##############
            """
            eval_accuracy += tmp_eval_accuracy
            nb_eval_steps += 1
            nb_eval_examples += inputs["input_ids"].size(0)
            nb_eval_batches += 1 
        eval_loss = eval_loss / nb_eval_steps
        eval_accuracy = eval_accuracy / nb_eval_batches 
        #over_all = accuracy.compute(predictions=preds_list, references=true_list) #compute_metrics((preds_list, true_list))
        result = {"eval_loss": eval_loss, "eval_accuracy": eval_accuracy}
        print(result)
    
    elif args.action == "test":

        model = AutoModelForMultipleChoice.from_pretrained(args.from_checkpoint).to(device) 
        experiment_sub_dir = f"mbert_lr{args.learning_rate}_wd{args.weight_decay}"

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir),   
            save_strategy="epoch",
            evaluation_strategy="epoch",
            learning_rate=args.learning_rate,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.batch_size,
            num_train_epochs=args.num_epochs,
            weight_decay=args.weight_decay,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_mct["train"],
            eval_dataset=tokenized_mct["test"],
            #test_dataset=tokenized_mct["test"],
            tokenizer=tokenizer,
            data_collator=DataCollatorForMultipleChoice(tokenizer=tokenizer),
        )

        if device == "cuda":
            model.cuda()

        # Eval!
        model.eval()

        test_loss, test_accuracy = 0, 0
        nb_test_steps, nb_test_examples = 0, 0
        nb_test_batches = 0 

        preds_list = []
        true_list = []

        test_dataloader = trainer.get_eval_dataloader() 
        for batch in tqdm(test_dataloader, desc="Evaluating TEST data"):
            with torch.no_grad():

                inputs = {
                    "input_ids": batch["input_ids"].to(args.device),
                    "attention_mask": batch["attention_mask"].to(args.device),
                    "token_type_ids": batch["token_type_ids"].to(args.device),
                    "labels": batch["labels"].to(args.device),
                }

                outputs = model(**inputs)
                tmp_test_loss, logits = outputs[:2]
                test_loss += tmp_test_loss.mean().item()

            logits = logits.detach().cpu().numpy()
            preds = np.argmax(logits, axis=1)
            print(f"[test] predictions: {preds}")
            [preds_list.append(p) for p in preds]
            label_ids = inputs["labels"].to("cpu").numpy()
            print(f"[test] labels: {label_ids}")
            [true_list.append(l) for l in label_ids]

            
            tmp_test_accuracy = (preds == label_ids).astype(np.float32).mean().item() #BATCH-wise accuracy
            test_accuracy += tmp_test_accuracy
            nb_test_steps += 1
            nb_test_examples += inputs["input_ids"].size(0)
            nb_test_batches += 1 
        test_loss = test_loss / nb_test_steps
        test_accuracy = test_accuracy / nb_test_batches 
        result = {"test_loss": test_loss, "test_accuracy": test_accuracy}
        print(result)
    


    else:
        print("* Supported actions are `train` or `evaluate` or `test` ")




main()
