import argparse
import os
import random
from typing import Any, Mapping, Sequence, TypedDict
import numpy as np
from transformers import (
    AutoTokenizer,
    PreTrainedTokenizerBase,
    EarlyStoppingCallback,
)
from datasets import load_dataset
from dataclasses import dataclass
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
import torch
from torch.utils.tensorboard import SummaryWriter
from transformers.integrations import TensorBoardCallback
from transformers import AutoModelForMultipleChoice, TrainingArguments, Trainer
from tqdm import tqdm
import evaluate

accuracy = evaluate.load("accuracy")

"""
Working from this/these tutorials

https://huggingface.co/docs/transformers/v4.22.0/en/tasks/multiple_choice#multiple-choice
https://huggingface.co/transformers/v3.3.1/model_doc/auto.html?highlight=automodelformultiplechoice#transformers.AutoModelForMultipleChoice

"""


def parse_args():
    parser = argparse.ArgumentParser()

    # Data
    parser.add_argument(
        "--data_dir", type=str, default="", help="path to directory with mctest files"
    )

    # Output & Logging
    parser.add_argument(
        "--tb_dir", type=str, default="/home/cs.aau.dk/az01dn/mcdata/tensorboard"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/home/cs.aau.dk/az01dn/mcdata/results_mctest_eng",
    )

    # Model
    parser.add_argument("--tokenizer", type=str, default="xlm-roberta-base")
    parser.add_argument("--from_pretrained", type=str, default="xlm-roberta-base")
    parser.add_argument("--from_checkpoint", type=str, default="")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"])
    parser.add_argument(
        "--max_length",
        type=int,
        default=512,
    )

    # Training
    parser.add_argument(
        "--action", type=str, default="train", choices=["train", "evaluate", "test"]
    )
    parser.add_argument("--seed", type=int, default=12)
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument(
        "--learning_rate", type=float, default=2e-5, help="Former default was 5e-5"
    )
    parser.add_argument("--weight_decay", type=float, default=0.01)

    # Evaluation
    parser.add_argument("--eval_batch_size", type=int, default=8)

    return parser.parse_args()


def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


class RawBatch(TypedDict):
    choices: Sequence[Sequence[str]]
    label: Sequence[str]
    question: Sequence[str]
    story: Sequence[str]
    text_answer: Sequence[str]


def preprocess_function(
    tokenizer: PreTrainedTokenizerBase,
    examples: RawBatch,
    max_length: int,
) -> Mapping[str, Any]:
    choices = []
    stories = []
    labels = []

    bos_token = tokenizer.bos_token
    eos_token = tokenizer.eos_token

    for story, question, candidates, lbl in zip(
        examples["story"],
        examples["question"],
        examples["choices"],
        examples["label"],
        strict=True,
    ):
        for i, option in enumerate(candidates):
            choices.append(f"{question} {eos_token} {bos_token} {option}")  # real!
            # This is for debugging only. We should get 100% Acc if we add the answer
            # choices.append(f"{question} {sep_tok} {label==str(i)} {sep_tok} {option}")
            stories.append(story)
        labels.append(int(lbl))
    tokenized_examples = tokenizer(
        stories,
        choices,
        truncation=True,
        max_length=max_length,
    )
    bb = {
        k: [v[i : i + 4] for i in range(0, len(v), 4)]
        for k, v in tokenized_examples.items()
    }
    return {**bb, "label": labels}


@dataclass
class DataCollatorForMultipleChoice:
    tokenizer: PreTrainedTokenizerBase
    max_length: int

    def __call__(self, features):
        batch_size = len(features)
        num_choices = 4
        flattened_features = [
            {k: f[k][i] for k in ("input_ids", "attention_mask")}
            for f in features
            for i in range(num_choices)
        ]

        batch = self.tokenizer.pad(
            flattened_features,
            padding=True,
            return_tensors="pt",
        )

        batch = {k: v.view(batch_size, num_choices, -1) for k, v in batch.items()}
        batch["labels"] = torch.tensor(
            [f["label"] for f in features], dtype=torch.int64
        )
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
        print(f"There are {torch.cuda.device_count()} GPU(s) available.")
        print("We will use the GPU:", torch.cuda.get_device_name(0))
    else:
        print("Running on cpu.")

    data_path = args.data_dir

    examples = load_dataset(f"{data_path}/")
    print("****** EXAMPLES ******")
    print(examples)

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    tokenized_mct = examples.map(
        (lambda x: preprocess_function(tokenizer, x, args.max_length)),
        batched=True,
        desc="Tokenizing",
    )

    if args.action == "train":
        model = AutoModelForMultipleChoice.from_pretrained(args.from_pretrained).to(
            device
        )
        # init tensorboard for tracking
        experiment_sub_dir = f"{args.from_pretrained.replace('/', '|')}_lr{args.learning_rate}_wd{args.weight_decay}"
        writer = SummaryWriter(os.path.join(args.tb_dir, experiment_sub_dir))
        tensorboard_callback = TensorBoardCallback(writer)

        # early_stopping = EarlyStoppingCallback(
        #     early_stopping_patience=5, early_stopping_threshold=0.001
        # )

        training_args = TrainingArguments(
            output_dir=os.path.join(args.output_dir, experiment_sub_dir),
            save_strategy="epoch",
            evaluation_strategy="epoch",
            learning_rate=args.learning_rate,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.eval_batch_size,
            num_train_epochs=args.num_epochs,
            weight_decay=args.weight_decay,
            load_best_model_at_end=True,
            logging_steps=100,
            logging_first_step=True,
            bf16=True,
            report_to="none",
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_mct["train"],
            eval_dataset=tokenized_mct["validation"],
            tokenizer=tokenizer,
            data_collator=DataCollatorForMultipleChoice(
                tokenizer=tokenizer, max_length=args.max_length
            ),
            callbacks=[tensorboard_callback],  # , early_stopping],
            compute_metrics=compute_metrics,
        )
        print(f"DEVICE: {device}")
        if device == "cuda":
            model.cuda()
        train_result = trainer.train()

        writer.close()

    elif args.action == "evaluate":
        # load trained model
        model = AutoModelForMultipleChoice.from_pretrained(args.from_checkpoint).to(
            device
        )

        experiment_sub_dir = f"{args.from_pretrained.replace('/', '|')}_lr{args.learning_rate}_wd{args.weight_decay}"

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
            data_collator=DataCollatorForMultipleChoice(
                tokenizer=tokenizer, max_length=args.max_length
            ),
            callbacks=[tensorboard_callback],
        )

        if device == "cuda":
            model.cuda()

        # Eval!
        model.eval()

        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0

        dev_dataloader = (
            trainer.get_eval_dataloader()
        )  # use the trainer to get the collated dev data
        for batch in tqdm(dev_dataloader, desc="Evaluating"):
            # set_trace()
            # batch = tuple(i.to(args.device) for t,i in batch.items())#put on device
            with torch.no_grad():
                inputs = {
                    "input_ids": batch["input_ids"].to(args.device),
                    "attention_mask": batch["attention_mask"].to(args.device),
                    "labels": batch["labels"].to(args.device),
                }

                outputs = model(**inputs)
                tmp_eval_loss, logits = outputs[:2]
                eval_loss += tmp_eval_loss.mean().item()

            logits = logits.detach().cpu().numpy()
            # print(logits)
            preds = np.argmax(logits, axis=1)
            print(f"[eval] predictions: {preds}")
            # print(preds)
            label_ids = inputs["labels"].to("cpu").numpy()
            print(f"[eval] labels: {label_ids}")
            # print(label_ids)
            tmp_eval_accuracy = (preds == label_ids).astype(np.float32).mean().item()
            # if tmp_eval_accuracy != 1.0:
            # set_trace()
            # print(f"****** WRONG ********")
            # print(f"tmp_acc: {tmp_eval_accuracy}")
            # print(f"true: {label_ids}")
            # print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10]))
            # print(f"predicted: {preds}")
            # print(tokenizer.convert_ids_to_tokens(batch[0][0][int(preds)][:-10]))
            # else:
            # print(f"****** CORRECT ********")
            # print(tokenizer.convert_ids_to_tokens(batch[0][0][int(label_ids)][:-10]))
            # print()
            # print(f"-----"*10)
            # print(tmp_eval_accuracy)
            # tmp_eval_accuracy = accuracy(logits, label_ids)
            eval_accuracy += tmp_eval_accuracy
            nb_eval_steps += 1  # number of batches
            nb_eval_examples += inputs["input_ids"].size(0)

        eval_loss = eval_loss / nb_eval_steps
        eval_accuracy = eval_accuracy / nb_eval_steps
        result = {"eval_loss": eval_loss, "eval_accuracy": eval_accuracy}
        print(result)

    elif args.action == "test":
        model = AutoModelForMultipleChoice.from_pretrained(args.from_checkpoint).to(
            device
        )

        experiment_sub_dir = f"{args.from_pretrained.replace('/', '|')}_lr{args.learning_rate}_wd{args.weight_decay}"

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
            tokenizer=tokenizer,
            data_collator=DataCollatorForMultipleChoice(
                tokenizer=tokenizer, max_length=args.max_length
            ),
            # callbacks=[callback]
        )

        if device == "cuda":
            model.cuda()

        # Eval!
        model.eval()

        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0

        dev_dataloader = (
            trainer.get_eval_dataloader()
        )  # use the trainer to get the collated dev data
        for batch in tqdm(dev_dataloader, desc="Evaluating"):
            # set_trace()
            # batch = tuple(i.to(args.device) for t,i in batch.items())#put on device
            with torch.no_grad():
                inputs = {
                    "input_ids": batch["input_ids"].to(args.device),
                    "attention_mask": batch["attention_mask"].to(args.device),
                    "labels": batch["labels"].to(args.device),
                }

                outputs = model(**inputs)
                tmp_eval_loss, logits = outputs[:2]
                eval_loss += tmp_eval_loss.mean().item()

            logits = logits.detach().cpu().numpy()
            # print(logits)
            preds = np.argmax(logits, axis=1)
            print(f"[test] predictions: {preds}")
            # print(preds)
            label_ids = inputs["labels"].to("cpu").numpy()
            print(f"[test] labels: {label_ids}")
            # print(label_ids)
            tmp_eval_accuracy = (preds == label_ids).astype(np.float32).mean().item()

            eval_accuracy += tmp_eval_accuracy
            nb_eval_steps += 1  # number of batches
            nb_eval_examples += inputs["input_ids"].size(0)

        eval_loss = eval_loss / nb_eval_steps
        eval_accuracy = eval_accuracy / nb_eval_steps
        result = {"test data loss": eval_loss, "test data accuracy": eval_accuracy}
        print(result)
    else:
        print("* Supported actions are `train` or `evaluate` ")


main()
