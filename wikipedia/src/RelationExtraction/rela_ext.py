import pickle
import json
import re
from itertools import tee

# import spacy
import jsonlines
# from SPARQLWrapper import SPARQLWrapper, JSON
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from termcolor import cprint, colored

from utils import retrieve_relation_type

# https://github.com/migrationsKB/MGKB/blob/master/entity_linking/wiki2wikidata.py

# TODO
# restrcuture the entity pairs, get statistics (1,2,3) entities in one sentence
# write sparql query
# query the relation types between entities /
# TODO: whether they exist in the wikidata triples.
# how many valid triples we have for each languages. -> test data for relation extraction
# english data from ukp as training data for model, then do zero-shot

# wikidata should consistently say the same things for all the languages.

# using english to try out first. -> gold dataset.
#


### load spacy pipeline.
# https://spacy.io/usage/models#multi-language
# nlp = spacy.load("en_core_web_md")

# def load_graph_embeddings(transe_file = "data/wikiata5m/transe_wikidata5m.pkl"):
transe_file = "../../data/wikiata5m/transe_wikidata5m.pkl"
with open(transe_file, "rb") as fin:
    model = pickle.load(fin)

entity2id = model.graph.entity2id
relation2id = model.graph.relation2id
id2relation = model.graph.id2relation
entity_embeddings = model.solver.entity_embeddings
relation_embeddings = model.solver.relation_embeddings


# should we consider the syntax of the sentence when doing relation extraction?
def pairwise(iterable):
    # in python ab 3.10
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def relation_extraction_document_level(jsonfile, annofile):
    # spacy sentence tokenizer with en_core_web_md didn't work well.
    df_anno = pd.read_csv(annofile, sep="\t")
    # get the q_id
    alisa2qcode = dict(zip(df_anno["Text"], df_anno["Wikidata_ID"]))
    # print(alisa2id)

    # find the annotated phrases in the jsonfile.
    expr = r"\[\[(.*?)\]\]"

    counter = 0
    with jsonlines.open(jsonfile) as f:
        while counter < 10:
            for obj in f:
                # ata = json.load(obj)
                title = obj["title"]
                text = obj["linked_text"]
                groups = re.findall(expr, text)

                if groups is not None:
                    pairwised_list = [(x, y) for (x, y) in list(pairwise(groups)) if x != y]
                    if len(pairwised_list) > 1:
                        print(title)
                        print(text)
                        for e1, e2 in pairwised_list:
                            if e1 in alisa2qcode and e2 in alisa2qcode:
                                e1_qcodes = alisa2qcode[e1]
                                e2_qcodes = alisa2qcode[e2]

                                if e1_qcodes in entity2id and e2_qcodes in entity2id:
                                    cprint(f"{e1}, {e2}", "blue")
                                    predict_relations(e1_qcodes, e2_qcodes)
                        print("*" * 50)
                counter += 1


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


if __name__ == '__main__':
    # sample
    sentence = "[[Pedro Fernández de Quirós]] i bin kamtru long [[Vanuatu]] long 1606."
    # Q313633, Q686
    # predict_relations("Q313633","Q686",3) # P27, country of citizenship
    test_file = "../../output/bi.jsonl"
    annos_file = "../../output/bi_annos.csv"
    relation_extraction_document_level(test_file, annos_file)


