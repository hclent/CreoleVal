import argparse
from pudb import set_trace
import os, csv, json
import random
import numpy as np
from models import MyBertForMultipleChoice
from transformers import AutoTokenizer
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

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-uncased")

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
    parser.add_argument("--parse_data_to_json", type=bool, default=False) #TODO: change the code to check for json, and if it doesnt exist, create it. 

    #Output & Logging
    parser.add_argument("--tb_dir",type=str, default="/home/cs.aau.dk/az01dn/mcdata/tensorboard")
    parser.add_argument("--output_dir", type=str, default="/home/cs.aau.dk/az01dn/mcdata/results_mctest_eng")

    #Model
    parser.add_argument("--tokenizer", type=str, default="bert-base-multilingual-cased")
    parser.add_argument("--from_pretrained", type=str, default="bert-base-multilingual-cased")
    parser.add_argument("--from_checkpoint", type=str, default="")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"])

    #Training
    parser.add_argument("--action", type=str, default="train", choices=["train", "evaluate"])
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--learning_rate", type=float, default=2e-5,
                        help="Former default was 5e-5")
    parser.add_argument("--weight_decay", type=float, default=0.01)


    # Evaluation
    parser.add_argument("--eval_batch_size", type=int, default=1)

    return parser.parse_args()
    

def write_to_json(path, split):
    """
    Input:
     path: str = the/path/to/your/data/dir
     split: str = mctest.train

    Output: 
     examples = list[dict] 
    """

    full_path = os.path.join(path, split)
    questions_path = f"{full_path}.tsv"
    answers_path = f"{full_path}.ans"

    q_dict = {}
     # q_dict: dict of dicts = 
     #    {id: 
     #        {'story': '...', 
     #         'questions': [[the question, a1, a2, a3, a4], [q2], [q3], [q4]],
     #         'answers': [A, B, C, A]
     #        } 

    examples = []

    with open(questions_path, newline='') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for i, row in enumerate(reader):
            q_id = row[0]
            story = row[2]
            questions = row[3:]
            organized_questions = []
            q_set = []
            for q in questions:
                if q.startswith('one:') or q.startswith('multiple:'):
                    q_set = [] # start of new question
                    q_set.append(q)
                else:
                    q_set.append(q)
                if len(q_set) == 5:
                    organized_questions.append(q_set)

            assert len(organized_questions) == 4 #every story has 4 questions

            for qa in organized_questions:
                assert len(qa) == 5 #question + 4 multiple choice

            q_dict[q_id] = {'story': story, 'questions': organized_questions}

    with open(answers_path, newline='') as ansfile:
        reader = csv.reader(ansfile, delimiter='\t')
        for i, row in enumerate(reader):
            q_id = f"{split}.{i}"
            q_dict[q_id].update({'answers': row})

    story_counter = 0
    question_counter = 0 

    for indx, mc_dict in q_dict.items():
        story_counter += 1
        story = mc_dict['story']
        j = 1
        for q, a in zip(mc_dict['questions'], mc_dict['answers']):
            lut = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            choices = q[1:]
            a_to_index = lut[a]
            text_answer = choices[a_to_index]

            question_text = q[0]
            if question_text.startswith("one: "):
                cleaned = (question_text).strip("one: ")#("one: ").strip(question_text)
                q_type = "one"
            else:
                cleaned = (question_text).strip("multiple: ")#("multiple: ").strip(question_text)
                q_type = "multiple"

            e_dict = {
                'story': story,
                'story_id': str(indx),
                'question_id': str(j), 
                'question': cleaned,
                'q_type': q_type,
                'choices': choices,
                'answer': a, #ABCD
                'text_answer': text_answer, #the text itself
                'label': str(a_to_index), #FIXME: i'm having to cast this to an int later
            }
            examples.append(e_dict) 
            j+=1
            question_counter +=1

    print(f"* {story_counter} stories ...")
    print(f"* {question_counter} questions ...")


    with open(f"{path}/as_json/{split}.json", "w") as out:
        for ex in examples:
            json.dump(ex, out)
            out.write('\n')




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
                trunc_token_type_ids = encoded_input['token_type_ids'][:self.max_len]
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

    #TODO: check if json exists, if not, create if, if so, pass. 
    #write_to_json(data_path, split)

    examples = load_dataset(f"{data_path}/as_json")
    print(f"****** EXAMPLES ******")
    print(examples)

    tokenized_mct = examples.map(preprocess_function, batched=True)
   
    data_collator = DataCollatorForMultipleChoice(tokenizer) #

    if args.action == "train":
        #model = AutoModelForMultipleChoice.from_pretrained(args.from_pretrained).to(device)
        model = MyBertForMultipleChoice.from_pretrained(args.from_pretrained).to(device)
        #init tensorboard for tracking
        experiment_sub_dir = f"lr{args.learning_rate}_wd{args.weight_decay}"
        writer = SummaryWriter(os.path.join(args.tb_dir, experiment_sub_dir))
        callback = TensorBoardCallback(writer)

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir), #f"./results_mctest_eng/no_story_with_answers_{experiment_sub_dir}", #TODO:also make output dir configurable.  
            save_steps=2500,
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
            callbacks=[callback]
        )
        print(f"DEVICE: {device}") 
        if device == "cuda":
            model.cuda()
        train_result = trainer.train()
        
        writer.close()

    elif args.action == "evaluate":

        #load trained model
        #model = AutoModelForMultipleChoice.from_pretrained(args.from_checkpoint).to(device) #TODO: lets make our own copy of this ...
        model = MyBertForMultipleChoice.from_pretrained(args.from_checkpoint).to(device)

        experiment_sub_dir = f"lr{args.learning_rate}_wd{args.weight_decay}"
        #writer = SummaryWriter(os.path.join(args.tb_dir, experiment_sub_dir))
        #callback = TensorBoardCallback(writer)

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir), #f"./results_mctest_eng/no_story_with_answers_{experiment_sub_dir}", #TODO:also make output dir configurable.  
            save_steps=5000,
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

        #dev_dataloader = trainer.get_eval_dataloader() #use the trainer to get the collated dev data
        dev_dataloader = trainer.get_train_dataloader()
        for batch in tqdm(dev_dataloader, desc="Evaluating"):
            batch = tuple(i.to(args.device) for t,i in batch.items())#put on device
            with torch.no_grad():
                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    # 'token_type_ids': None if args.model_type == 'xlm' else batch[2]  # XLM don't use segment_ids
                    "token_type_ids": batch[2],
                    "labels": batch[3],
                }

                # if args.model_type in ['xlnet', 'xlm']:
                #     inputs.update({'cls_index': batch[4],
                #                    'p_mask':    batch[5]})
                outputs = model(**inputs)
                tmp_eval_loss, logits = outputs[:2]
                eval_loss += tmp_eval_loss.mean().item()

            logits = logits.detach().cpu().numpy()
            #print(logits)
            preds = np.argmax(logits, axis=1)
            #print(preds)
            label_ids = inputs["labels"].to("cpu").numpy()
            #print(label_ids)
            tmp_eval_accuracy = (preds == label_ids).astype(np.float32).mean().item()
            if tmp_eval_accuracy != 1.0:
                #set_trace()
                #print(f"****** WRONG ********")
                #print(f"tmp_acc: {tmp_eval_accuracy}")
                #print(f"true: {label_ids}")
                #print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10]))
                #print(f"predicted: {preds}")
                #print(tokenizer.convert_ids_to_tokens(batch[0][0][int(preds)][:-10]))
            #else:
                #print(f"****** CORRECT ********")
                #print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10]))
                #print()
            #print(f"-----"*10)
            #print(tmp_eval_accuracy)
            #tmp_eval_accuracy = accuracy(logits, label_ids)
            eval_accuracy += tmp_eval_accuracy
            nb_eval_steps += 1
            nb_eval_examples += inputs["input_ids"].size(0)

        eval_loss = eval_loss / nb_eval_steps
        eval_accuracy = eval_accuracy / nb_eval_examples
        result = {"eval_loss": eval_loss, "eval_accuracy": eval_accuracy}
        print(result)
        """
        output_eval_file = os.path.join(f"./results_mctest_eng/story_with_answers_{experiment_sub_dir}", "eval_results_ON_TRAIN_DATA.txt")
        with open(output_eval_file, "w") as writer:
           writer.write(f"***** Eval results *****\n")
           for key in sorted(result.keys()):
               writer.write("%s = %s\n" % (key, str(result[key])))
        """
    
    else:
        print("* Supported actions are `train` or `evaluate` ")




main()
