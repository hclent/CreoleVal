import json
import os.path

import pandas as pd
import spacy
from more_itertools import consecutive_groups

nlp = spacy.load("xx_ent_wiki_sm")
nlp.add_pipe("sentencizer")
tokenizer = nlp.tokenizer


def find_all_ids_for_ent(ent, doc):
    """
    Find all the ids for one entity in the re. sentence
    """
    # tokenization
    el = tokenizer(ent)
    el_ids = []  # get all the ids of el elements in the sentence.
    for t in doc:
        # print(t.text, t.i, )
        for e in el:
            # print(e)
            if e.text == t.text:
                el_ids.append(t.i)
    # one entity can have multiple groups of ids.
    el_ids = sorted(list(set(el_ids)))  # in order to avoid multiple ids.
    LEN = len(el)
    ent2ids = []
    for g in consecutive_groups(el_ids):
        g_l = list(g)
        if len(g_l) == LEN:
            ent2ids.append(g_l)
    return ent2ids


def processing_one_row(sentence, ent1, ent2, ent1_qcode, ent2_qcode, p):
    """
    Processing one row.
    sentence, ent1, ent2, ent1_qcode, ent2_qcode, property
    example: Liu Yifei (bon 1987) hem i wan akta blong Jaena .	Liu Yifei	akta	Q242676	Q33999	P106
    """
    instance = dict()
    doc = nlp(sentence)
    tokens = [t.text for t in doc]
    instance["tokens"] = tokens
    ent1_ids = find_all_ids_for_ent(ent1, doc)
    ent2_ids = find_all_ids_for_ent(ent2, doc)
    edgesets = {}
    if len(ent1_ids) == 1 and len(ent2_ids) == 1:
        ent1_start = ent1_ids[0][0]
        ent2_start = ent2_ids[0][0]
        if ent1_start < ent2_start:
            edgesets["left"] = ent1_ids[0]
            edgesets["right"] = ent2_ids[0]
            edgesets["triple"] = (ent1_qcode, ent2_qcode, p)
        else:
            edgesets["right"] = ent1_ids[0]
            edgesets["left"] = ent2_ids[0]
            edgesets["triple"] = (ent2_qcode, ent1_qcode, p)
    else:
        print(f"alert: {sentence}, {ent1}, {ent2} ")
        print(ent1_ids,ent2_ids)

    edgesets["property"] = p
    instance["edgeSet"] = edgesets
    return instance


def processing_one_file(filepath):
    """
    Processing one file to render form csv to json for training and evaluating
    using ZSBert.
    """
    print(f"open file {filepath}")
    save2filepath = filepath.replace(".csv", ".json")
    df = pd.read_csv(filepath)

    df_list = []

    print("processing ....")
    for row in df.itertuples():
        sentence, ent1, ent2, ent1_qcode, ent2_qcode, p = row[1], row[2], row[3], row[4], row[5], row[6]
        instance = processing_one_row(sentence, ent1, ent2, ent1_qcode, ent2_qcode, p)

        df_list.append(instance)

    print(f"Saving the file to {save2filepath}")
    with open(save2filepath, "w") as f:
        json.dump(df_list, f)


if __name__ == '__main__':
    import plac

    plac.call(processing_one_file)

