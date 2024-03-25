import json
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
from transformers import BertTokenizer
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForMaskedLM


def load_datas(json_files, val_portion=0.0, load_vertices=True):
    """
    Load semantic graphs from multiple json files and if specified reserve a portion of the data for validation.

    :param json_files: list of input json files
    :param val_portion: a portion of the data to reserve for validation
    :return: a tuple of the data and validation data
    """
    data = []
    for json_file in json_files:
        with open(json_file) as f:
            if load_vertices:
                data = data + json.load(f)
            else:
                data = data + json.load(f, object_hook=dict_to_graph_with_no_vertices)
    print("Loaded data size:", len(data))

    val_data = []
    if val_portion > 0.0:
        val_size = int(len(data) * val_portion)
        rest_size = len(data) - val_size
        val_data = data[rest_size:]
        data = data[:rest_size]
        print("Training and dev set sizes:", (len(data), len(val_data)))
    return data, val_data


def load_data(json_file, val_portion=0.0, load_vertices=True):
    return load_datas([json_file], val_portion, load_vertices)


def split_wiki_data(data, test_relation):
    train_data, test_data = [], []
    for i in data:
        kbID = i['edgeSet'][0]['kbID']
        if kbID not in test_relation:
            train_data.append(i)
        elif kbID in test_relation:
            test_data.append(i)
    return train_data, test_data


def get_pid2vec(sentence_embedder, idx2property_file, prop_list_path):
    with open(idx2property_file) as f:
        idx2property = json.load(f)
    property2idx = {prop: idx for idx, prop in idx2property.items()}
    prop_list = pd.read_html(prop_list_path, flavor="html5lib")[0]
    prop_list = prop_list.loc[prop_list.ID.isin(property2idx.keys())]

    encoder = SentenceTransformer(sentence_embedder)
    sentence_embeddings = encoder.encode(prop_list.description.to_list())
    pid2vec = {}
    for pid, embedding in zip(prop_list.ID, sentence_embeddings):
        pid2vec[pid] = embedding.astype('float32')
    return property2idx, idx2property, pid2vec


def generate_attribute(train_label, test_label, Creole_label,
    sentence_embedder='bert-large-nli-mean-tokens', att_dim=1024,
    prop_list_path='/home/nlp/ZL/TEST/Creole-NLU-NLG-Suite-wiki/wikipedia/ZS_BERT/resources/property_list.html'):
    # from sentence_transformers import SentenceTransformer
    property2idx = {}
    idx2property = {}
    idx = 0
    for i in set(train_label):
        property2idx[i] = idx
        idx2property[idx] = i
        idx += 1
    for i in set(test_label):
        property2idx[i] = idx
        idx2property[idx] = i
        idx += 1
    for cl in Creole_label.values():
        cl = set(cl)
        for l in cl:
            if l not in property2idx.keys():
                property2idx[l] = idx
                idx2property[idx] = l
                idx += 1

    prop_list = pd.read_html(prop_list_path, flavor="html5lib")[0]
    prop_list = prop_list.loc[prop_list.ID.isin(property2idx.keys())]
    encoder = SentenceTransformer(sentence_embedder)
    sentence_embeddings = encoder.encode(prop_list.description.to_list())

    # if att_dim < 768:
    #     from sklearn.decomposition import TruncatedSVD
    #     print(f'att_dim={att_dim}')
    #     svd = TruncatedSVD(n_components=att_dim, n_iter=10, random_state=42)
    #     sentence_embeddings = svd.fit_transform(sentence_embeddings)
    #     print(f'size of sentence_embeddings: {sentence_embeddings.shape}')

    print(f'size of sentence_embeddings: {sentence_embeddings.shape}')
    pid2vec = {}
    for pid, embedding in zip(prop_list.ID, sentence_embeddings):
        pid2vec[pid] = embedding.astype('float32')
    return property2idx, idx2property, pid2vec


def mark_wiki_entity(edge, sent_len):
    e1 = edge['left']
    e2 = edge['right']
    marked_e1 = np.array([0] * sent_len)
    marked_e2 = np.array([0] * sent_len)
    marked_e1[e1] += 1
    marked_e2[e2] += 1
    return torch.tensor(marked_e1, dtype=torch.long), torch.tensor(marked_e2, dtype=torch.long)


def mark_fewrel_entity(edge, sent_len):
    e1 = np.array(edge['h'][2][0]) + 1
    e2 = np.array(edge['t'][2][0]) + 1
    marked_e1 = np.array([0] * sent_len)
    marked_e2 = np.array([0] * sent_len)
    marked_e1[e1] += 1
    marked_e2[e2] += 1
    return torch.tensor(marked_e1, dtype=torch.long), torch.tensor(marked_e2, dtype=torch.long)


def create_mini_batch(samples):
    tokens_tensors = [s[0] for s in samples]
    segments_tensors = [s[1] for s in samples]
    marked_e1 = [s[2] for s in samples]
    marked_e2 = [s[3] for s in samples]
    relation_emb = [s[4] for s in samples]
    if samples[0][5] is not None:
        label_ids = torch.stack([s[5] for s in samples])
    else:
        label_ids = None

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
    relation_emb = np.array(relation_emb)  # make the list into an array first before converting to tensor
    relation_emb = torch.tensor(relation_emb)
    return tokens_tensors, segments_tensors, marked_e1, marked_e2, masks_tensors, relation_emb, label_ids


class WikiDataset(Dataset):
    def __init__(self, mode, data, pid2vec, property2idx, model):
        assert mode in ['train', 'dev', 'test']
        self.mode = mode
        self.data = data
        self.pid2vec = pid2vec
        self.property2idx = property2idx
        self.len = len(self.data)
        self.tokenizer = AutoTokenizer.from_pretrained(model, do_lower_case=False)
        # print('a')

    #     self.tokenizer = BertTokenizer.from_pretrained(
    # model, do_lower_case=False)

    def __getitem__(self, idx):
        g = self.data[idx]

        # tokens_final = ["[CLS]"]
        #
        # edge_new = {}
        # for i, t in enumerate(g["tokens"]):
        #     new_token = self.tokenizer.tokenize(t)
        #     if len(edge['left']) > 0:
        #         if i == edge['left'][0]:  # left_start
        #             left_start = len(tokens_final)
        #         if i == edge['left'][-1]:  # left_end
        #             left_end = len(tokens_final) + len(new_token)
        #     if len(edge['right']) > 0:
        #         if i == edge['right'][0]:  # right_start
        #             right_start = len(tokens_final)
        #         if i == edge['right'][-1]:  # right_end
        #             right_end = len(tokens_final) + len(new_token)
        #     tokens_final.extend(new_token)
        # if len(edge['left']) > 0:
        #     edge_new['left'] = list(range(left_start, left_end))
        # else:
        #     edge_new['left'] = edge['left']
        # if len(edge['right']) > 0:
        #     edge_new['right'] = list(range(right_start, right_end))
        # else:
        #     edge_new['right'] = edge['right']
        # # print('a')
        # tokens_final = tokens_final + ['[SEP]']

        sentence = " ".join(g["tokens"])  # old
        tokens = self.tokenizer.tokenize(sentence)  # old
        # tokens_ids = self.tokenizer.convert_tokens_to_ids(tokens_final)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + tokens + ["[SEP]"])  # old

        tokens_tensor = torch.tensor(tokens_ids)
        segments_tensor = torch.tensor([0] * len(tokens_ids),
            dtype=torch.long)

        if self.mode == 'dev':
            edge = g["edgeSet"]
        else:
            edge = g["edgeSet"][0]

        # edge = g["edgeSet"][0]
        # marked_e1, marked_e2 = mark_wiki_entity(edge_new, len(tokens_ids))  # mark有错误

        marked_e1, marked_e2 = mark_wiki_entity(edge, len(tokens_ids))  # mark有错误

        if self.mode == 'dev':
            property_kbid = g['edgeSet']['kbID']
        else:
            property_kbid = g['edgeSet'][0]['kbID']

        relation_emb = self.pid2vec[property_kbid]

        if self.mode == 'train':
            label = int(self.property2idx[property_kbid])
            label_tensor = torch.tensor(label)
        elif self.mode == 'test' or self.mode == 'dev':
            label_tensor = None

        return (tokens_tensor, segments_tensor, marked_e1, marked_e2, relation_emb, label_tensor)

    def __len__(self):
        return self.len


class FewRelDataset(Dataset):
    def __init__(self, mode, data, pid2vec, property2idx):
        assert mode in ['train', 'dev', 'test']
        self.mode = mode
        self.data = data
        self.pid2vec = pid2vec
        self.property2idx = property2idx
        self.len = len(data)
        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-base-cased', do_lower_case=False)

    def __getitem__(self, idx):
        g = self.data[idx]
        sentence = " ".join(g["tokens"])
        tokens = self.tokenizer.tokenize(sentence)
        tokens_ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + tokens + ["[SEP]"])
        tokens_tensor = torch.tensor(tokens_ids)
        segments_tensor = torch.tensor([0] * len(tokens_ids),
            dtype=torch.long)
        marked_e1, marked_e2 = mark_fewrel_entity(g, len(tokens_ids))
        relation_emb = self.pid2vec[g['relation']]

        if self.mode == 'train':
            label = int(self.property2idx[g['relation']])
            label_tensor = torch.tensor(label)
        elif self.mode == 'test' or self.mode == 'dev':
            label_tensor = None

        return (tokens_tensor, segments_tensor, marked_e1, marked_e2, relation_emb, label_tensor)

    def __len__(self):
        return self.len
