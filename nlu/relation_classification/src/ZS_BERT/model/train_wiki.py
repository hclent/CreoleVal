import json
import random
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

import data_helper
from model import ZSBert
import torch
from torch.utils.data import DataLoader
from evaluation import extract_relation_emb, evaluate
from transformers import BertConfig
from tqdm import tqdm

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--seed", help="random seed", type=int, default=300, dest="seed")
# parser.add_argument("-m", "--n_unseen", help="number of unseen classes", type=int, default=10, dest="m")
parser.add_argument("-g", "--gamma", help="margin factor gamma", type=float, default=7.5, dest="gamma")
parser.add_argument("-a", "--alpha", help="balance coefficient alpha", type=float, default=0.4, dest="alpha")
parser.add_argument("-d", "--dist_func", help="distance computing function", type=str, default='inner',
                    dest="dist_func")
parser.add_argument("-b", "--batch_size", type=int, default=256, dest="batch_size")
parser.add_argument("-e", "--epochs", type=int, default=10, dest="epochs")
parser.add_argument("-t", "--transformer", type=str, default="bert-base-multilingual-cased", dest="t")
parser.add_argument("-se", "--sentence_embedder", type=str, default="bert-base-nli-mean-tokens", dest="se")
# parser.add_argument("-re", "--relation_emb", type=int, default=1024, dest="relation_emb")
# parser.add_argument("-cr", "--Creole", nargs="*", default=None, help="Creole list", dest="cr")
parser.add_argument("-w", "--wiki_zsl_data", type=str, default="ZS_BERT/Wiki-ZSL", help="Wiki-ZSL data file")
# parser.add_argument("--Creole_data", type=str, default=None, help="Creole RE data file")
parser.add_argument("-ms", "--model_saves", type=str, default="saved_models", help="model save dir")
parser.add_argument("-p", "--prop_list_path", type=str, default="ZS_BERT/resources/property_list.html", help="path to the property list")

args = parser.parse_args()
# set randam seed, this affects the data spliting.
random.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)

# add the directory to the ukp data
train_data_file = os.path.join(args.wiki_zsl_data, "train.json")
test_data_file = os.path.join(args.wiki_zsl_data, "test.json")
idx2property_file = os.path.join(args.wiki_zsl_data, "idx2property.json")

with open(train_data_file) as f:
    training_data = json.load(f)
with open(test_data_file) as f:
    test_data = json.load(f)
train_label = list(i['edgeSet'][0]['kbID'] for i in training_data)
test_label = list(i['edgeSet'][0]['kbID'] for i in test_data)

# set up sentence embedder
# prop_list_path = "../resources/property_list.html"
property2idx, idx2property, pid2vec = data_helper.get_pid2vec(args.se, idx2property_file,
                                                              prop_list_path=args.prop_list_path)

print('there are {} kinds of relation in train.'.format(len(set(train_label))))
print('there are {} kinds of relation in test.'.format(len(set(test_label))))
print('number of union of train and test: {}'.format(len(set(train_label) & set(test_label))))

print(len(training_data))
print(len(test_data))

bertconfig = BertConfig.from_pretrained(args.t,
                                        num_labels=len(set(train_label)),
                                        finetuning_task='wiki-zero-shot')
# bertconfig.relation_emb_dim = args.relation_emb
bertconfig.margin = args.gamma
bertconfig.alpha = args.alpha
bertconfig.dist_func = args.dist_func
# get relation embedding dimension directly
bertconfig.relation_emb_dim = list(pid2vec.values())[0].shape[0]
model = ZSBert.from_pretrained(args.t, config=bertconfig)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda:0" if torch.cuda.is_available() else "cpu")
if device == "cuda:0":
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

model.train()
optimizer = torch.optim.Adam(model.parameters(), lr=5e-6)

# prepare the model.


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

    if f1t > best_f1:
        best_p = pt
        best_r = rt
        best_f1 = f1t

        nn = args.t.split('/')[-1]

        model_save_dir = f"{args.model_saves}/{nn}/{args.se}"
        if not os.path.exists(model_save_dir):
            os.makedirs(model_save_dir)

        with open(os.path.join(model_save_dir, f"results_seed{args.seed}"), "w+") as f:
            result = {"preicison": pt, "recall":rt, "f1":f1t}
            json.dump(result,f)

        torch.save(model,
                   f'{args.model_saves}/{nn}/{args.se}/best_f1_{best_f1}_wiki_epoch_{epoch}_alpha_{args.alpha}_gamma_{args.gamma}_seed_{args.seed}')
    print(f'[best val] precision: {best_p:.4f}, recall: {best_r:.4f}, f1 score: {best_f1:.4f}')
