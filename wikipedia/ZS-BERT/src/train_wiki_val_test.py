import json
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from termcolor import cprint
from torch.utils.data import DataLoader
from transformers import BertModel, BertConfig, BertPreTrainedModel, BertTokenizer
from argparse import ArgumentParser

from src.evaluation import extract_relation_emb, evaluate
from src import data_helper
from src.model import ZSBert

parser = ArgumentParser()
parser.add_argument("-s", "--seed", help="random seed", type=int, default=300, dest="seed")
parser.add_argument("-m", "--n_unseen", help="number of unseen classes", type=int, default=10, dest="m")
parser.add_argument("-g", "--gamma", help="margin factor gamma", type=float, default=7.5, dest="gamma")
parser.add_argument("-a", "--alpha", help="balance coefficient alpha", type=float, default=0.4, dest="alpha")
parser.add_argument("-d", "--dist_func", help="distance computing function", type=str, default='inner',
                    dest="dist_func")
parser.add_argument("-b", "--batch_size", type=int, default=2, dest="batch_size")
parser.add_argument("-e", "--epochs", type=int, default=10, dest="epochs")
parser.add_argument("-p", "--datapath", type=str, default="data/", dest="p")
parser.add_argument("-se", "--sentence_embedder", type=str, default="bert-large-nli-mean-tokens",
                    dest="se")
parser.add_argument("-t", "--transformer", type=str, default="bert-base-multilingual-cased", dest="t")
parser.add_argument("-r", "--relation_dim", type=int, default=1024, dest="r")
parser.add_argument("-to", "--tokenizer", type=str, default="bert-base-multilingual-cased", dest="to")
parser.add_argument("-out", "--output", type=str, default="output/", dest="out")

args = parser.parse_args()
# set randam seed, this affects the data spliting.
random.seed(args.seed)

# setup environment in m1

cprint(f"torch backends cuda available: {torch.cuda.is_available()}", "red")
cprint(f"torch backends mps available: {torch.backends.mps.is_available()}", "green")

cprint(f"loading data...", "magenta")
train_data, val_data, test_data = data_helper.load_datasets(args.p, args.m)
cprint(f"train {len(train_data)} val {len(val_data)} test {len(test_data)}", "magenta")

train_label = list(i['edgeSet'][0]['kbID'] for i in train_data)
val_label = list(i['edgeSet'][0]['kbID'] for i in val_data)
# test_label = list(i['edgeSet'][0]['kbID'] for i in test_data)
cprint(f"there are {len(set(train_label))} kinds of relations in train data.", "blue")
# cprint(f"there are {len(set(test_label))} kinds of relations in test data.", "blue")
cprint(f"there are {len(set(val_label))} kinds of relations in val data.", "blue")
cprint(f'number of union of train and val: {len(set(train_label) & set(val_label))}', "blue")
# cprint(f'number of union of train and test: {len(set(train_label) & set(test_label))}', "blue")
# cprint(f'number of union of test and val: {len(set(val_label) & set(test_label))}', "blue")

property2idx, idx2property, pid2vec = data_helper.generate_attribute(train_label, val_label,
                                                                     sentence_embedder=args.se, att_dim=args.r)

bert_model_name = args.t

# bert_model_name = "bert-large-cased"

bertconfig = BertConfig.from_pretrained(bert_model_name,
                                        num_labels=len(set(train_label)),
                                        finetuning_task='wiki-zero-shot')

bertconfig.relation_emb_dim = args.r  # 1024
bertconfig.margin = args.gamma
bertconfig.alpha = args.alpha
bertconfig.dist_func = args.dist_func

cprint(f"Loading the ZSBERT model from {bert_model_name}", "red")
model = ZSBert.from_pretrained(bert_model_name, config=bertconfig)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cprint(f"device: {device}", "red")
cprint(f"loading model to {device}", "red")
model = model.to(device)


trainset = data_helper.WikiDataset('train', train_data, pid2vec, property2idx, args.to)
trainloader = DataLoader(trainset, batch_size=args.batch_size, collate_fn=data_helper.create_mini_batch, shuffle=True)

valset = data_helper.WikiDataset('dev', val_data, pid2vec, property2idx, args.to)
valloader = DataLoader(valset, batch_size=256, collate_fn=data_helper.create_mini_batch)

testset = data_helper.WikiDataset('test', test_data, pid2vec, property2idx, args.to)
testloader = DataLoader(testset, batch_size=256,
                        collate_fn=data_helper.create_mini_batch)


# test_y_attr, test_y = [], []
# test_idxmap = {}
#
# for i, test in enumerate(test_data):
#     property_kbid = test['edgeSet'][0]['kbID']
#     label = int(property2idx[property_kbid])
#     test_y.append(label)
#     test_idxmap[i] = label
#
# test_y_attr = list(pid2vec[i] for i in set(test_label))
# test_y_attr = np.array(test_y_attr)
# test_y = np.array(test_y)
#
# print(test_y_attr.shape)
# print(test_y.shape)

#### convert val data
val_y_attr, val_y = [], []
val_idxmap = {}

for i, val in enumerate(val_data):
    property_kbid = val['edgeSet'][0]['kbID']
    label = int(property2idx[property_kbid])
    val_y.append(label)
    val_idxmap[i] = label

val_y_attr = list(pid2vec[i] for i in set(val_label))
val_y_attr = np.array(val_y_attr)
val_y = np.array(val_y)

print(val_y_attr.shape)
print(val_y.shape)


model.train()
print("model is training..")
optimizer = torch.optim.Adam(model.parameters(), lr=5e-6)

model_output_dir = os.path.join(args.out, f"m{args.m}")
if not os.path.exists(model_output_dir):
    os.mkdir(model_output_dir)
    bertconfig.to_json_file(os.path.join(model_output_dir, "bertconfig.json"))


best_p_val = 0.0
best_r_val = 0.0
best_f1_val = 0.0
for epoch in range(args.epochs):
    cprint(f'============== TRAIN ON THE {epoch + 1}-th EPOCH ==============', 'red')
    running_loss = 0.0
    correct = 0
    total = 0
    for step, data in tqdm(enumerate(trainloader)):

        tokens_tensors, segments_tensors, marked_e1, marked_e2, \
        masks_tensors, relation_emb, labels = [t.to(device) for t in data]
        optimizer.zero_grad()

        outputs, out_relation_emb = model(input_ids=tokens_tensors,
                                          token_type_ids=segments_tensors,
                                          e1_mask=marked_e1,
                                          e2_mask=marked_e2,
                                          attention_mask=masks_tensors,
                                          input_relation_emb=relation_emb,
                                          labels=labels)

        loss = outputs[0]
        logits = outputs[1]
        total += labels.size(0)
        _, pred = torch.max(logits, 1)
        correct += (pred == labels).sum().item()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if step % 1000 == 0:
            print(f'[step {step}]' + '=' * (step // 1000))
    print(f'train acc: {correct / total}')

    cprint("============== EVALUATION ON VAL DATA ==============", "red")
    val_preds = extract_relation_emb(model, valloader).cpu().numpy()
    val_pt, val_rt, val_f1t = evaluate(val_preds, val_y_attr, val_y, val_idxmap, len(set(val_label)), args.dist_func)
    print(f'[val] precision: {val_pt:.4f}, recall: {val_rt:.4f}, f1 score: {val_f1t:.4f}')

    if val_f1t > best_f1_val:
        best_p = val_pt
        best_r = val_rt
        best_f1 = val_f1t
        torch.save(model,os.path.join(model_output_dir, f'best_f1_{best_f1}_wiki_epoch_{epoch}_m_{args.m}_alpha_{args.alpha}_gamma_{args.gamma}'))
    print(f'[best val] precision: {best_p_val:.4f}, recall: {best_r_val:.4f}, f1 score: {best_f1_val:.4f}')

    # cprint('============== EVALUATION ON TEST DATA ==============', "red")
    # preds_test = extract_relation_emb(model, testloader).cpu().numpy()
    # pt, rt, f1t = evaluate(preds_test, test_y_attr, test_y, test_idxmap, len(set(train_label)), args.dist_func)
    # print(f'[test] precision: {pt:.4f}, recall: {rt:.4f}, f1 score: {f1t:.4f}')

