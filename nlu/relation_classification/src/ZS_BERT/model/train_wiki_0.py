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
from tqdm import tqdm
from sklearn.metrics import precision_recall_fscore_support
from transformers import AutoTokenizer, AutoModelForMaskedLM, AutoConfig

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--seed", help="random seed", type=int, default=300, dest="seed")
# parser.add_argument("-m", "--n_unseen", help="number of unseen classes", type=int, default=10, dest="m")
parser.add_argument("-g", "--gamma", help="margin factor gamma", type=float, default=7.5, dest="gamma")
parser.add_argument("-a", "--alpha", help="balance coefficient alpha", type=float, default=0.4, dest="alpha")
parser.add_argument("-d", "--dist_func", help="distance computing function", type=str, default='inner',
    dest="dist_func")
parser.add_argument("-b", "--batch_size", type=int, default=4, dest="batch_size")
parser.add_argument("-e", "--epochs", type=int, default=10, dest="epochs")
parser.add_argument("-t", "--transformer", type=str, default="bert-base-multilingual-cased", dest="t")
parser.add_argument("-se", "--sentence_embedder", type=str, default="bert-base-nli-mean-tokens", dest="se")
parser.add_argument("-re", "--relation_emb", type=int, default=1024, dest="relation_emb")
parser.add_argument("-cr", "--Creole", nargs="*", default=None, help="Creole list", dest="cr")
parser.add_argument("--Wiki_ZSL_data", type=str, default=None, help="Wiki-ZSL data file")
parser.add_argument("--Creole_data", type=str, default=None, help="Creole RE data file")
parser.add_argument("--model_saves", type=str, default=None, help="model save dir")
parser.add_argument("--prop_list_path", type=str, default=None, help="model save dir")

args = parser.parse_args()
# set randam seed, this affects the data spliting.
random.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)

train_data_file = os.path.join(args.Wiki_ZSL_data, "train.json")
test_data_file = os.path.join(args.Wiki_ZSL_data, "test.json")
idx2property_file = os.path.join(args.Wiki_ZSL_data, "idx2property.json")

with open(train_data_file) as f:
    training_data = json.load(f)
    # training_data = training_data[:2000]
with open(test_data_file) as f:
    test_data = json.load(f)
train_label = list(i['edgeSet'][0]['kbID'] for i in training_data)
test_label = list(i['edgeSet'][0]['kbID'] for i in test_data)

property2idx, idx2property, pid2vec = data_helper.get_pid2vec(args.se, idx2property_file,
    prop_list_path=args.prop_list_path)

print('there are {} kinds of relation in train.'.format(len(set(train_label))))
print('there are {} kinds of relation in test.'.format(len(set(test_label))))
print('number of union of train and test: {}'.format(len(set(train_label) & set(test_label))))

print(len(training_data))
print(len(test_data))

# Creole data
Creole_data = {}
Creole_label = {}
root_dir = args.Creole_data
for c in args.cr:
    filepath = root_dir + '/' + c + '.json'
    with open(filepath) as f:
        data = json.load(f)  #
    for d in data:
        d['edgeSet']['kbID'] = d['edgeSet']['triple'][-1]
    Creole_data[c] = data
    Creole_data_label = list(i['edgeSet']['kbID'] for i in data)
    Creole_label[c] = Creole_data_label
    output_info = 'There are {} kinds of relation in Creole '.format(len(set(Creole_data_label))) + c
    print(output_info)
    output_info = 'number of union of train and Creole' + c + ': {}'.format(
        len(set(train_label) & set(Creole_data_label)))
    print(output_info)

print('\n')

property2idx, idx2property, pid2vec = data_helper.generate_attribute(train_label=train_label,
    test_label=test_label,
    Creole_label=Creole_label,
    sentence_embedder=args.se,
    att_dim=args.relation_emb,
    prop_list_path=args.prop_list_path)

bertconfig = BertConfig.from_pretrained(args.t,
    num_labels=len(set(train_label)),
    finetuning_task='wiki-zero-shot')
bertconfig.relation_emb_dim = args.relation_emb
bertconfig.margin = args.gamma
bertconfig.alpha = args.alpha
bertconfig.dist_func = args.dist_func
bertconfig.relation_emb_dim = list(pid2vec.values())[0].shape[0]
model = ZSBert.from_pretrained(args.t, config=bertconfig)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
if device == "cuda":
    torch.cuda.manual_seed_all(args.seed)

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print("device:", device)
model = model.to(device)

trainset = data_helper.WikiDataset('train', training_data, pid2vec, property2idx, args.t)
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

testset = data_helper.WikiDataset('test', test_data, pid2vec, property2idx, args.t)
testloader = DataLoader(testset, batch_size=256,
    collate_fn=data_helper.create_mini_batch)

#
# Creole_y_attr, Creole_y = {}, {}# 获取test_y,以及test中label的相关attribute
# Creole_idxmap = {}
#
# for c, c_data in Creole_data.items():
#     c_y_attr, c_y = [], []# 获取test_y,以及test中label的相关attribute
#     c_idxmap = {}
#     for i, cc_data in enumerate(c_data):
#         property_kbid = cc_data['edgeSet']['kbID']
#         label = int(property2idx[property_kbid])
#         c_y.append(label)
#         c_idxmap[i] = label
#     c_y_attr = list(pid2vec[i] for i in set(Creole_label[c]))
#     c_y_attr = np.array(c_y_attr)#10，,1024
#     c_y = np.array(c_y)
#     Creole_y_attr[c] = c_y_attr
#     Creole_y[c] = c_y
#     Creole_idxmap[c] = c_idxmap
#     print(c)
#     print("Creole_y_attr.shape {}. ".format(c_y_attr.shape))
#     print("Creole_y.shape {}.".format(c_y.shape))
#
# Creole_set = {}
# Creole_loader = {}
# for c in args.cr:
#     Creole_set[c] = data_helper.WikiDataset('dev', Creole_data[c], pid2vec, property2idx, args.t)
#     Creole_loader[c] = DataLoader(Creole_set[c], batch_size=256,
#                         collate_fn=data_helper.create_mini_batch)


model.train()
optimizer = torch.optim.Adam(model.parameters(), lr=5e-6)

best_p = 0.0
best_r = 0.0
best_f1 = 0.0
for epoch in range(args.epochs):
    print(f'============== TRAIN ON THE {epoch + 1}-th EPOCH ==============')
    running_loss = 0.0
    correct = 0
    total = 0
    for step, data in enumerate(tqdm(trainloader)):

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

    print('============== EVALUATION ON TEST DATA ==============')
    preds = extract_relation_emb(model, testloader).cpu().numpy()
    pt, rt, f1t = evaluate(preds, test_y_attr, test_y, test_idxmap, len(set(train_label)), args.dist_func)
    print(f'[test] precision: {pt:.4f}, recall: {rt:.4f}, f1 score: {f1t:.4f}')

    # Creole_predictions = {}
    # Creole_pre = []
    # Creole_re = []
    # Creole_F1 = []
    # for c in args.cr:
    #     c_preds = extract_relation_emb(model, Creole_loader[c]).cpu().numpy()
    #     # c_pt, c_rt, c_f1t, predictions = evaluate(c_preds, Creole_y_attr[c], Creole_y[c], Creole_idxmap[c], len(set(Creole_label[c])), args.dist_func)
    #     c_pt, c_rt, c_f1t = evaluate(c_preds, Creole_y_attr[c], Creole_y[c], Creole_idxmap[c], len(set(Creole_label[c])), args.dist_func)
    #     # Creole_predictions[c] = predictions
    #     print(f'{c} precision: {c_pt:.4f}, recall: {c_rt:.4f}, f1 score: {c_f1t:.4f}')
    #     Creole_F1.append(c_f1t)
    #     Creole_pre.append(c_pt)
    #     Creole_re.append(c_rt)

    if f1t > best_f1:
        best_p = pt
        best_r = rt
        best_f1 = f1t

        nn = args.t.split('/')[-1]
        torch.save(model,
            f'{args.model_saves}/{nn}/{args.se}/best_f1_{best_f1}_wiki_epoch_{epoch}_alpha_{args.alpha}_gamma_{args.gamma}')
    print(f'[best val] precision: {best_p:.4f}, recall: {best_r:.4f}, f1 score: {best_f1:.4f}')
