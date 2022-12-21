import json
import csv
import os
import pandas as pd
from ast import literal_eval
from itertools import chain
from collections import Counter
from termcolor import cprint, colored
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

output_file = "output/summary.csv"

INPUT_FOLDER = "output/document_classification"


# Top 20 classes
def read_one_file(filepath):
    with open(filepath) as reader:
        data = json.load(reader)

        concepts = data["concepts"][0]
        qcode = concepts["notation"][0]  # Q1000065
        count = concepts["occurrences"][0]["count"]  # how many languages?
        try:
            label = concepts["prefLabel"]["en"]  # english label

            broader = concepts["broader"]
            qcodes_broader = []
            for item in broader:
                qcode_ = item["uri"].split("/")[-1]
                qcodes_broader.append(qcode_)

            return qcode, count, label, qcodes_broader
        except Exception:
            print(qcode, "exception")


def process_all_files():
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["qcode", "count", "label", "qcodes_broader"])

        for filepath in os.listdir(INPUT_FOLDER):

            filepath = os.path.join(INPUT_FOLDER, filepath)
            print(filepath)
            try:
                qcode, count, label, qcodes_broader = read_one_file(filepath)
                writer.writerow([qcode, count, label, qcodes_broader])
            except Exception:
                print("Exception")


def get_statistics(file=output_file, count_most_common=20):
    cprint("Statistics of the Wikidata instances and sup-classes ...", "blue", attrs=["bold"])
    df = pd.read_csv(output_file, sep="\t", index_col=0)
    df.dropna(subset=["qcodes_broader"], inplace=True)
    print("entities in total:", len(df))
    # df["qcodes_broader"] = df["qcodes_broader"]
    qcodes_broader = df["qcodes_broader"].apply(literal_eval).tolist()
    qcodes_broader_list = list(chain.from_iterable(qcodes_broader))

    print("qcodes in sup-class in total: ", len(qcodes_broader_list), "unique classes: ",
          len(list(set(qcodes_broader_list))))  # 70290, 3463
    # most common sup-classes
    most_commons = Counter(qcodes_broader_list).most_common(count_most_common)

    print("Most common sup-classes ....")
    for qcode_, freq in most_commons:
        # cprint("*" * 20, "grey")
        cprint(f"{qcode_}, counts {freq}", "green", attrs=["bold", "underline"])
        instances = df[df["qcodes_broader"].str.contains(qcode_)].index.tolist()[:10]

        # for instance in instances:
        #     label = df.at[instance, "label"]
        #     cprint(f"{instance} => {label}", "magenta")
        # print(instance,)


def get_occurrence_matrix(output_file):
    # get occurrence matrix of the super-classes from wikipedia pages.
    cprint("Co-occurrence statistics of the sup-classes", "blue", attrs=["bold"])
    df = pd.read_csv(output_file, sep="\t", index_col=0)
    df["qcodes_broader"] = df["qcodes_broader"].apply(literal_eval)
    df["qcodes_broader"] = df["qcodes_broader"].apply(" ".join)
    cprint(f"The length of the dataframe {len(df)}", "green")
    l = df["qcodes_broader"].tolist()
    # constructing co-occur matrix from the codes.
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    arr = vectorizer.fit_transform(l)
    arr_coocur = (arr.T * arr)
    arr_coocur.setdiag(0)  # set the diagonals to be zeroes as it's pointless to be 1
    # get the vocabulary/code names
    names = vectorizer.get_feature_names()
    cprint(f"The size of the codes {len(names)}", "red")
    df_coocur = pd.DataFrame(data=arr_coocur.toarray(), columns=names, index=names)
    print(df_coocur.head(5))
    df_coocur.to_csv("output/stats/cooccurrence_super_classes.csv", sep=",")


def get_stats(file, top_n=20):
    cprint("rank coocurences matrix by descending order...", "blue", attrs=["bold"])
    df = pd.read_csv(file, index_col=0)
    df["A"] = df.index
    df_ = df.melt(id_vars=["A"], value_vars=df.columns)  # melt the pandas dataframe to rank the matrix by values.
    cprint(df_.nlargest(top_n, "value"), "magenta")


if __name__ == '__main__':
    # get_statistics(output_file, 10)
    # get_occurrence_matrix(output_file)
    get_stats("output/stats/cooccurrence_super_classes.csv", 20)
