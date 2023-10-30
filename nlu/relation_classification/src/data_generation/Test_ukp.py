import os
import json
import pickle

import pandas as pd
import numpy as np

from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import f1_score, precision_score, recall_score


transe_file = "../../data/wikiata5m/transe_wikidata5m.pkl"
with open(transe_file, "rb") as fin:
    model = pickle.load(fin)

entity2id = model.graph.entity2id
relation2id = model.graph.relation2id
id2relation = model.graph.id2relation
entity_embeddings = model.solver.entity_embeddings
relation_embeddings = model.solver.relation_embeddings


def predict_relations(ent1, ent2, top_n=3):
    """
    ent1, ent2: Wikidata qcodes of the entities
    model: pretrained Wikidata5m graph embeddings
    """

    # subtract entity1 from entity2 to get the supposed relation embeddings
    e1_id = entity2id[ent1]
    e2_id = entity2id[ent2]
    e1 = entity_embeddings[e1_id]
    e2 = entity_embeddings[e2_id]
    rel = e2 - e1
    rel = rel.reshape(1, -1)  # reshape 1D to 2D array

    scores = []
    for _, idx in relation2id.items():
        relation_emb = relation_embeddings[idx].reshape(1, -1)
        scores.append(cosine_similarity(relation_emb, rel))

    scores_arr = np.array(scores).flatten()

    sorted_indices = np.argsort(scores_arr)[::-1]

    for indice in sorted_indices[:top_n]:
        relation_qcode = id2relation[indice]
        print(relation_qcode)


def test_ukp_datasets(
        testfile="../../data/WikipediaWikidataDistantSupervisionAnnotations.v1.0/enwiki-20160501/semantic-graphs-filtered-held-out.02_06.json"):
    with open(testfile) as f:
        test_data = json.load(f)

    gold = []
    preds = []
    for sample in tqdm.tqdm(test_data[:1000]):
        vertexSet = sample["vertexSet"]
        if len(vertexSet) == 2:
            e1 = vertexSet[0]["kbID"]
            e2 = vertexSet[1]["kbID"]
        edgeSet = sample["edgeSet"]

        r = edgeSet[0]["kbID"]
        print(e1, e2, r)
        print(" ".join(sample["tokens"]))

        if e1.startswith("Q") and e2.startswith("Q"):
            try:
                pred_rs = predict_relations(e1, e2, top_n=5)[0]
                gold.append(r)
                preds.append(pred_rs)
            except Exception as msg:
                print(msg)


