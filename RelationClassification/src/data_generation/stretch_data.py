import json
from itertools import chain
from ast import literal_eval
import pandas as pd
import plac
import os


# def streching(datafile, outputfolder):
#     # data/ent_extraction -> data.entExt
#     with open(datafile) as f:
#         data = json.load(f)
#     print("original:", len(data))
#     new_data = []
#
#     for line in data:
#         tokens = line["tokens"]
#         for edge in line['edgeSet']:
#             new_data.append({
#                 "tokens": tokens,
#                 "edgeSet": [edge]
#             })
#
#     print("new:", len(new_data))
#     basename = os.path.basename(datafile)
#     with open(os.path.join(outputfolder, basename), "w") as f:
#         json.dump(new_data, f)


def post_processing(datafile, anno_file, outputfolder="data/post-processed/partial"):
    #  ZS_BERT/output/ht.json data/processed_wikidumps/ht_anno.csv
    annos = pd.read_csv(anno_file)
    with open(datafile, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    basename = os.path.basename(datafile)

    writer = open(os.path.join(outputfolder, basename.replace(".json", ".csv")), "w")
    writer.write("Tokens\tLeft_Offset\tLeft\tLeft_ID\tRight_Offset\tRight\tRight_ID\tProperty\n")

    text2id = dict(zip(annos["Text"], annos["Wikidata_ID"]))
    counter = 0
    for line in data:
        try:
            tokens = line["tokens"]
            edgeset = line["edgeSet"]
            left_offsets = edgeset["left"]
            right_offsets = edgeset["right"]
            left_ent = " ".join([tokens[idx] for idx in edgeset["left"]]).replace(" ,", ",").replace(" '", "'").replace(
                " (", "(").replace(" )", ")")
            right_ent = " ".join([tokens[idx] for idx in edgeset["right"]]).replace(" ,", ",").replace(" '",
                                                                                                       "'").replace(
                " (", "(").replace(" )", ")")
            left_q = text2id[left_ent]
            right_q = text2id[right_ent]
            property = edgeset["property"]
            writer.write(f"{tokens}\t{left_offsets}\t{left_ent}\t{left_q}\t{right_offsets}\t{right_ent}\t{right_q}\t{property}\n")
        except Exception:
            counter += 1
            print(line)
    writer.close()
    print(counter)


def get_properties_for_each_lang(lang):
    # from triples-wd, using only these properties for ZS_BERT
    datafile = f"data/triples-wd/{lang}.csv"
    basename = os.path.basename(datafile).replace(".csv", ".json")
    df = pd.read_csv(datafile,converters={"Properties": literal_eval}, sep="\t")
    properties = list(set(list(chain.from_iterable(df["Properties"].tolist()))))
    print(len(properties))
    with open(os.path.join("data/properties", basename), "w") as f:
        json.dump(properties, f)


def stretching_triples(lang):
    datafile = f"data/triples-wd/{lang}.csv"
    df = pd.read_csv(datafile, converters={"Properties": literal_eval}, sep="\t")
    triples = list()
    for idx, item in df.iterrows():
        ent1 = item["ENT1"]
        ent2 = item["ENT2"]
        properties = item["Properties"]
        for property in properties:
            triples.append((ent1, ent2, property))
    filename = datafile.replace(".csv", ".json")
    with open(filename, "w") as f:
        json.dump(triples, f)


if __name__ == '__main__':
    # plac.call(get_properties_for_each_lang)
    # plac.call(stretching_triples)
    plac.call(post_processing)
