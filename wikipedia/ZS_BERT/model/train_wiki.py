import json
import random
import data_helper
import numpy as np
import pandas as pd
import os

from model import ZSBert
from tqdm import tqdm
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from evaluation import extract_relation_emb, evaluate
from transformers import BertModel, BertConfig, BertPreTrainedModel, BertTokenizer
from termcolor import cprint

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-s", "--seed", help="random seed", type=int, default=300, dest="seed")
parser.add_argument("-m", "--n_unseen", help="number of unseen classes", type=int, default=10, dest="m")
parser.add_argument("-g", "--gamma", help="margin factor gamma", type=float, default=7.5, dest="gamma")
parser.add_argument("-a", "--alpha", help="balance coefficient alpha", type=float, default=0.4, dest="alpha")
parser.add_argument("-d", "--dist_func", help="distance computing function", type=str, default='inner', dest="dist_func")
parser.add_argument("-b", "--batch_size", type=int, default=4, dest="batch_size")
parser.add_argument("-e", "--epochs", type=int, default=10, dest="epochs")
parser.add_argument("-t", "--transformer", type=str, default="bert-base-multilingual-cased", dest="transformer")
parser.add_argument("-se", "--sentence_embedder", type=str, default="bert-base-nli-mean-tokens", dest="se")
parser.add_argument("-re", "--relation_emb", type=int, default=1024, dest="relation_emb")

args = parser.parse_args()
# set randam seed, this affects the data spliting.
random.seed(args.seed) 

train_set = '../data/wiki_1k.json'

m_data_folder = os.path.join("../data", f"m{args.m}")
train_data_file = os.path.join(m_data_folder, "train.json")
test_data_file = os.path.join(m_data_folder, "test.json")
idx2property_file = os.path.join(m_data_folder, "idx2property.json")

if not os.path.exists(train_data_file):
    cprint(f"creating data from {train_set}", "red")
    training_data, _ = data_helper.load_data(train_set, load_vertices=True)
    train_label = list(i['edgeSet'][0]['kbID'] for i in training_data)

    pid, count = np.unique(train_label, return_counts=True)
    pid2cnt = dict(zip(pid, count))

    test_relation = random.sample(list(pid2cnt), k=args.m)
    training_data, test_data = data_helper.split_wiki_data(training_data, test_relation)
    print('train size: {}, test size: {}'.format(len(training_data), len(test_data)))

    train_label = list(i['edgeSet'][0]['kbID'] for i in training_data)
    test_label = list(i['edgeSet'][0]['kbID'] for i in test_data)
    property2idx, idx2property, pid2vec = data_helper.generate_attribute(train_label, test_label, args.se, args.relation_emb)

else:
    cprint(f"loading from folder {m_data_folder}", "red")
    with open(train_data_file) as f:
        training_data = json.load(f)
    with open(test_data_file) as f:
        test_data = json.load(f)
    train_label = list(i['edgeSet'][0]['kbID'] for i in training_data)
    test_label = list(i['edgeSet'][0]['kbID'] for i in test_data)

    property2idx, idx2property, pid2vec = data_helper.get_pid2vec(args.se,idx2property_file)


print('there are {} kinds of relation in train.'.format(len(set(train_label))))
print('there are {} kinds of relation in test.'.format(len(set(test_label))))
print('number of union of train and test: {}'.format(len(set(train_label) & set(test_label))))


print(len(training_data))
print(len(test_data))

bertconfig = BertConfig.from_pretrained(args.transformer,
                                        num_labels=len(set(train_label)),
                                        finetuning_task='wiki-zero-shot')
bertconfig.relation_emb_dim = args.relation_emb
bertconfig.margin = args.gamma
bertconfig.alpha = args.alpha
bertconfig.dist_func = args.dist_func

model = ZSBert.from_pretrained(args.transformer, config=bertconfig)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device:", device)
model = model.to(device)

trainset = data_helper.WikiDataset('train', training_data, pid2vec, property2idx, args.transformer)
trainloader = DataLoader(trainset, batch_size=args.batch_size, collate_fn=data_helper.create_mini_batch, shuffle=True)

test_y_attr, test_y = [], []
test_idxmap = {}
    
for i, test in enumerate(test_data):
    property_kbid = test['edgeSet'][0]['kbID']
    label = int(property2idx[property_kbid])
    test_y.append(label)
    test_idxmap[i] = label

test_y_attr = list(pid2vec[i] for i in set(test_label))    
test_y_attr = np.array(test_y_attr)
test_y = np.array(test_y)

print(test_y_attr.shape)
print(test_y.shape)

testset = data_helper.WikiDataset('test', test_data, pid2vec, property2idx, args.transformer)
testloader = DataLoader(testset, batch_size=256,
                        collate_fn=data_helper.create_mini_batch)


data_folder = f"../data/m{args.m}"
if not os.path.exists(data_folder):
    os.mkdir(data_folder)
with open(os.path.join(data_folder, "train.json"), "w") as f:
    json.dump(training_data, f)

with open(os.path.join(data_folder, "test.json"), "w") as f:
    json.dump(test_data, f)

with open(os.path.join(data_folder, "idx2property.json"), "w") as f:
    json.dump(idx2property, f)

model.train()
optimizer = torch.optim.Adam(model.parameters(), lr=5e-6)

best_p = 0.0
best_r = 0.0
best_f1 = 0.0
for epoch in range(args.epochs):
    print(f'============== TRAIN ON THE {epoch+1}-th EPOCH ==============')
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
            print(f'[step {step}]' + '=' * (step//1000))
    print(f'train acc: {correct/total}')

    print('============== EVALUATION ON TEST DATA ==============')
    preds = extract_relation_emb(model, testloader).cpu().numpy()
    pt, rt, f1t = evaluate(preds, test_y_attr, test_y, test_idxmap, len(set(train_label)), args.dist_func)
    print(f'[test] precision: {pt:.4f}, recall: {rt:.4f}, f1 score: {f1t:.4f}')

    if f1t > best_f1:
        best_p = pt
        best_r = rt
        best_f1 = f1t
        torch.save(model, f'best_f1_{best_f1}_wiki_epoch_{epoch}_m_{args.m}_alpha_{args.alpha}_gamma_{args.gamma}')
    print(f'[best val] precision: {best_p:.4f}, recall: {best_r:.4f}, f1 score: {best_f1:.4f}')
