import json
import os.path
from collections import defaultdict
from itertools import islice

import plac
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from sentence_transformers import SentenceTransformer
from transformers import AutoModel, AutoTokenizer

from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import f1_score, precision_score, recall_score

prop_list_path = './ZS_BERT/resources/property_list.html'


def mark_wiki_entity(edge, sent_len):
    e1 = edge['left']
    e2 = edge['right']
    marked_e1 = np.array([0] * sent_len)
    marked_e2 = np.array([0] * sent_len)
    marked_e1[e1] += 1
    marked_e2[e2] += 1
    return torch.tensor(marked_e1, dtype=torch.long), torch.tensor(marked_e2, dtype=torch.long)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


class WikiDataset(Dataset):
    def __init__(self, data, tokenizer):
        self.data = data
        self.len = len(self.data)
        # self.tokenizer = BertTokenizer.from_pretrained(
        #     tokenizer, do_lower_case=False)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer, do_lower_case=False)
        self.tokenizer_name = tokenizer

    def __getitem__(self, idx):
        g = self.data[idx]
        sentence = " ".join(g["tokens"])
        tokens = self.tokenizer.tokenize(sentence)
        if "bert" in self.tokenizer_name:
            tokens_ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + tokens + ["[SEP]"])
        if "xlm" in self.tokenizer_name:
            tokens_ids = self.tokenizer.convert_tokens_to_ids(["<s>"] + tokens + ["</s>"])

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


def get_model_dict(model_folder):
    """
    Get the best model for each seed.
    """
    file_list = os.listdir(model_folder)

    seed2file = defaultdict(dict)
    for filepath in file_list:
        seed = filepath.split("_")[-1]
        f1_score = round(float(filepath.split("_")[2]), 4)*100
        seed2file[seed][f1_score] = filepath

    sorted_seed2file = {seed: dict(islice(dict(sorted(d.items(), reverse=True)).items(), 1)) for seed, d in
        seed2file.items()}
    # {seed: f1: model_path}
    return sorted_seed2file


def prediction_per_model(tokenizer, sentence_embedder, seed, batch_size=16):
    # {seed: f1: model_path}
    model_folder = f"saved_models/{tokenizer}/{sentence_embedder}"
    seed2model = get_model_dict(model_folder)
    # load sentence embedder
    print(f"the best models... {seed2model}")
    encoder = SentenceTransformer(sentence_embedder)
    # load model

    creole_data_path = "../data/relation_extraction"
    creoles = ["bi", "cbk-zam", "jam", "tpi"]

    results_dict = defaultdict(dict)
    results_dict["model"]["sentence_embedder"] = sentence_embedder
    results_dict["model"]["transformer"] = tokenizer

    outputfolder = os.path.join("output", tokenizer, sentence_embedder, seed)
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)

    seed = str(seed)
    if seed in seed2model:
        f1TOmodel = seed2model[seed]
        for f1, model_path in f1TOmodel.items():
            model_path = os.path.join(model_folder, model_path)
            print(f"loading model from {model_path}")
            results_dict["model"]["dev"] = f1
            results_dict["model"]["seed"] = seed
            results_dict["model"]["model_path"] = model_path

            model = torch.load(model_path, map_location=torch.device('cpu'))
            model.eval()
            # run predictions
            for creole in creoles:
                filepath = os.path.join(creole_data_path, f"{creole}.json")
                property_file = os.path.join(creole_data_path, f"properties/{creole}.json")

                creole_result = predictions(filepath, property_file, encoder, tokenizer, model, outputfolder,
                    batch_size)
                results_dict["creoles"][creole] = round(creole_result,4)*100

    result_filename = os.path.join("output", f"{tokenizer}_{sentence_embedder}_{seed}.json")
    if not os.path.exists("output"):
        os.makedirs("output")

    print(f"writing result to {result_filename}")
    with open(result_filename, "w") as f:
        json.dump(results_dict, f)

    print(f"results {results_dict}")


def predictions(filepath, property_file, encoder, tokenizer, model, outputfolder, batch_size):
    # from json file ../data/ent_extraction/..json
    with open(filepath) as f:
        data = json.load(f)  #

    with open(property_file) as f:
        properties = json.load(f)
    # encoder = AutoModel.from_pretrained(sentence_embedder)
    # tokenizer = AutoTokenizer.from_pretrained(sentence_embedder)

    # load property list
    prop_list = pd.read_html(prop_list_path, flavor="html5lib")[0]
    prop_list = prop_list[prop_list["ID"].isin(properties)]
    print(len(prop_list))
    print(prop_list.head(2))

    prop_list.dropna(subset=["description"], inplace=True)
    print("length of property list :", len(prop_list))

    id2property = {idx: prop for idx, prop in enumerate(prop_list["ID"].tolist())}
    property2id = {prop: idx for idx, prop in id2property.items()}

    golden_rel = [property2id[d["edgeSet"]["triple"][-1]] for d in data]
    # get the sentence embeddings from encoder
    sentence_embeddings = encoder.encode(prop_list.description.to_list())

    pid2vec = {}
    for pid, embedding in zip(prop_list.ID, sentence_embeddings):
        pid2vec[pid] = embedding.astype('float32')
        # pid2vec[pid] = embedding.numpy().astype('float32')

    print(f"loading wiki dataset...")
    dataset = WikiDataset(data, tokenizer=tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, collate_fn=create_mini_batch)

    # model = torch.load(model_path, map_location=torch.device('cpu'))
    # model.eval()

    attr = list(pid2vec.values())
    attr = np.array(attr)
    # golden_rel =[]
    pred_rel = []

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
                pred_rel.extend(predictions)
        except Exception:
            preds_property += [None for _ in range(batch_size)]

    filename = os.path.basename(filepath)
    assert len(data) == len(preds_property)
    new_data = []
    for idx, line in enumerate(data):
        tokens = line["tokens"]
        edgeSet = line["edgeSet"]
        triple = line["edgeSet"]["triple"]
        prop = triple[-1]
        # prediction0 = line["edgeSet"]["prediction"]
        if preds_property[idx] != None:
            new_data.append({
                "tokens": tokens,
                "edgeSet": {
                    "left": edgeSet["left"],
                    "right": edgeSet["right"],
                    "property": preds_property[idx],
                    "triple": triple,
                    "prediction": prop == preds_property[idx],
                }
            })

    outputfile = os.path.join(outputfolder, filename)
    precision = precision_score(golden_rel, pred_rel, average='macro')
    recall = recall_score(golden_rel, pred_rel, average='macro')
    f1 = f1_score(golden_rel, pred_rel, average='macro')
    print(f"pre: {precision}, recall: {recall}, f1: {f1}")

    # record the results.
    with open(outputfile, "w") as f:
        json.dump(new_data, f)

    return f1


if __name__ == '__main__':
    # tokenizer, sentence_transformer, seed, batch_size
    plac.call(prediction_per_model)
