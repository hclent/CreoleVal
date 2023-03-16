import json
import string

import pandas as pd
import numpy as np
import regex
from tqdm import tqdm
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

from thefuzz import fuzz, process


def run_fuzzy_wuzzy_clustering(lang, k=10):
    df = pd.read_csv(f"data/fuzzywuzzy/dfs/{lang}.csv")
    df = df.drop_duplicates(subset=["text_preprocessed"]).reset_index(drop=True)
    print(f"loading {lang}, len {len(df)}")

    X_fuzz = pd.crosstab([df.index, df.text_preprocessed], df.text_preprocessed).apply(
        lambda col: [fuzz.partial_ratio(col.name, x)
                     for x in col.index.get_level_values(1)])

    X_fuzz = X_fuzz.to_numpy()

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X_fuzz)

    df["fuzzy_cluster"] = kmeans.predict(X_fuzz)

    print(df["fuzzy_cluster"].value_counts())
    df.to_csv(f"data/fuzzywuzzy/results/{lang}_{k}.csv")


def main(lang):
    if lang == "ht":
        for k in range(10, 110, 10):
            run_fuzzy_wuzzy_clustering(lang, k)
    elif lang in ["cbk-zam", "gcr", "pap", "sg"]:
        for k in range(10, 60, 10):
            run_fuzzy_wuzzy_clustering(lang, k)
    else:
        for k in range(5, 25, 5):
            run_fuzzy_wuzzy_clustering(lang, k)


if __name__ == '__main__':
    import plac

    plac.call(main)
