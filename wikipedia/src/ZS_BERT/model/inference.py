import json

import json
import os.path

import plac
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import classification_report

sentence_embedder = 'bert-base-nli-mean-tokens'
prop_list_path = '../resources/property_list.html'

torch.manual_seed(42)

def mark_wiki_entity(edge, sent_len):
    e1 = edge['left']
    e2 = edge['right']
    marked_e1 = np.array([0] * sent_len)
    marked_e2 = np.array([0] * sent_len)
    marked_e1[e1] += 1
    marked_e2[e2] += 1
    return torch.tensor(marked_e1, dtype=torch.long), torch.tensor(marked_e2, dtype=torch.long)


class WikiDataset(Dataset):
    def __init__(self, data, tokenizer="bert-base-multilingual-cased"):
        self.data = data
        self.len = len(self.data)
        self.tokenizer = BertTokenizer.from_pretrained(
            tokenizer, do_lower_case=False)

    def __getitem__(self, idx):
        g = self.data[idx]
        sentence = " ".join(g["tokens"])
        tokens = self.tokenizer.tokenize(sentence)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + tokens + ["[SEP]"])
        tokens_tensor = torch.tensor(tokens_ids)
        segments_tensor = torch.tensor([0] * len(tokens_ids),
                                       dtype=torch.long)
        edge = g["edgeSet"]
        marked_e1, marked_e2 = mark_wiki_entity(edge, len(tokens_ids))

        return (tokens_tensor, segments_tensor, marked_e1, marked_e2)

    def __len__(self):
        return self.len


def create_mini_batch(samples):
    tokens_tensors = [s[0] for s in samples]
    segments_tensors = [s[1] for s in samples]
    marked_e1 = [s[2] for s in samples]
    marked_e2 = [s[3] for s in samples]

    tokens_tensors = pad_sequence(tokens_tensors,
                                  batch_first=True)
    segments_tensors = pad_sequence(segments_tensors,
                                    batch_first=True)
    marked_e1 = pad_sequence(marked_e1,
                             batch_first=True)
    marked_e2 = pad_sequence(marked_e2,
                             batch_first=True)
    masks_tensors = torch.zeros(tokens_tensors.shape,
                                dtype=torch.long)
    masks_tensors = masks_tensors.masked_fill(
        tokens_tensors != 0, 1)

    return tokens_tensors, segments_tensors, marked_e1, marked_e2, masks_tensors


def predictions(filepath, property_file, model_path="../../../model/best_f1_0.7081677743338072_wiki_epoch_4_m_5_alpha_0.4_gamma_7.5",
                outputfolder="../../../output", batch_size=16,
                ):
    # from json file ../data/ent_extraction/..json
    with open(filepath) as f:
        data = json.load(f)

    with open(property_file) as f:
        properties = json.load(f)

    # load property list
    prop_list = pd.read_html(prop_list_path, flavor="html5lib")[0]
    prop_list = prop_list[prop_list["ID"].isin(properties)]
    print(len(prop_list))
    print(prop_list.head(2))

    prop_list.dropna(subset="description", inplace=True)
    print("length of property list :", len(prop_list))

    encoder = SentenceTransformer(sentence_embedder)
    id2property = {idx: prop for idx, prop in enumerate(prop_list["ID"].tolist())}

    sentence_embeddings = encoder.encode(prop_list.description.to_list())

    pid2vec = {}
    for pid, embedding in zip(prop_list.ID, sentence_embeddings):
        pid2vec[pid] = embedding.astype('float32')

    print(f"loading wikidataset...")
    dataset = WikiDataset(data)
    dataloader = DataLoader(dataset, batch_size=batch_size, collate_fn=create_mini_batch)

    print(f"loading model from {model_path}")

    model = torch.load(model_path, map_location=torch.device('cpu'))
    model.eval()

    attr = list(pid2vec.values())
    attr = np.array(attr)

    preds_property = []
    for sample in dataloader:
        tokens_tensors, segments_tensors, marked_e1, marked_e2, masks_tensors = [t for t in sample if t is not None]

        try:
            with torch.no_grad():
                _, out_relation_emb = model(input_ids=tokens_tensors,
                                            token_type_ids=segments_tensors,
                                            e1_mask=marked_e1,
                                            e2_mask=marked_e2,
                                            attention_mask=masks_tensors)

                tree = NearestNeighbors(n_neighbors=1, algorithm='ball_tree', metric=lambda a, b: -(a @ b))
                tree.fit(attr)
                predictions = tree.kneighbors(out_relation_emb, 1, return_distance=False).flatten()
                print(predictions)
                preds_property += [id2property[i] for i in predictions]
        except Exception:
            preds_property += [None for _ in range(batch_size)]

    filename = os.path.basename(filepath)
    assert len(data) == len(preds_property)
    new_data = []
    golds = []
    preds = []
    for idx, line in enumerate(data):
        tokens = line["tokens"]
        edgeSet = line["edgeSet"]
        triple = line["edgeSet"]["triple"]
        prop = triple[-1]
        if preds_property[idx] != None:
            new_data.append({
                "tokens": tokens,
                "edgeSet": {
                    "left": edgeSet["left"],
                    "right": edgeSet["right"],
                    "property": preds_property[idx],
                    "triple": triple,
                    "prediction": prop == preds_property[idx]
                }
            })
            golds.append(prop)
            preds.append(preds_property[idx])

    outputfile = os.path.join(outputfolder, filename)
    print(f"writing the predictions to file {outputfile}")
    # record the results.
    with open(outputfile, "w") as f:
        json.dump(new_data, f)

    # show the evaluation.
    results = classification_report(golds, preds)
    print(results)

if __name__ == '__main__':
    plac.call(predictions)
