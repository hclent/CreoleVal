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


def preprocessing_text(sentences):
    l = []
    for sentence in sentences:
        puncts = '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~–'
        sentence = sentence.translate(str.maketrans('', '', puncts)).translate(str.maketrans('', '', string.digits))
        tokens = word_tokenize(sentence)
        sent = " ".join(tokens)
        l.append(sent)
    return l


def load_json_data(filepath):
    # regex
    pattern = r"\[\[(.*?)\]\]"
    p = regex.compile(pattern)

    texts = []
    data = []
    data_ents = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        for line in f.readlines():
            line = json.loads(line)
            text = line["linked_text"]

            text_clean = text.replace("[[", "").replace("]]", "")

            if len(text_clean) > 0:
                # tokenize a document into sentences.
                sentences = sent_tokenize(text)
                texts += sentences
                # 1 -> clean sentences

                text_clean_processed = preprocessing_text(sentences)
                # data with clean sentences.
                data += text_clean_processed

                # process the entities in text
                sentences_ = []
                for sentence in sentences:
                    for m in p.finditer(sentence):
                        ent = m.group()
                        ent_preprocessed = "_".join(ent.replace("[[", "").replace("]]", "").split(" "))
                        sentence = sentence.replace(ent, ent_preprocessed).replace("[[", "").replace("]]", "")
                    # append.
                    sentences_.append(sentence)

                sentences_processed = preprocessing_text(sentences_)
                data_ents += sentences_processed
    assert len(texts) == len(data) == len(data_ents)
    df = pd.DataFrame.from_dict({"text": texts, "text_clean": data, "text_ents": data_ents}).dropna()

    df = df.drop_duplicates(subset="text_clean").reset_index(drop=True)
    return df


def visualize_elbow(df, col_name, outputfile, k_low=1, k_high=40, interval=2):
    # count vectorization
    df = df.dropna()
    vectorizer_cv = CountVectorizer(analyzer="word", ngram_range=(2, 2))
    X_data = df[col_name].tolist()
    X_data = vectorizer_cv.fit_transform(X_data)

    sns.set_style("whitegrid")
    sse = {}
    for k in np.arange(k_low, k_high, interval):
        kmeans = KMeans(n_clusters=k, max_iter=1000).fit(X_data)
        sse[k] = kmeans.inertia_
    plt.plot(list(sse.keys()), list(sse.values()))
    plt.xlabel('Values for K')
    plt.ylabel('SSE')
    plt.savefig(outputfile)
    plt.clf()


def clustering_kmeans(df, col_name, n_clusters, outputfile):
    # count vectorization
    vectorizer_cv = CountVectorizer(analyzer="word", ngram_range=(2, 2))
    X_data = df[col_name].tolist()
    X_data = vectorizer_cv.fit_transform(X_data)

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X_data)
    df_ = pd.DataFrame(X_data.toarray(), columns=vectorizer_cv.get_feature_names_out())
    df_result = pd.concat([df, df_], axis=1)
    df_result[f"{col_name}_cluster"] = kmeans.predict(X_data)
    print(df_result[f"{col_name}_cluster"].value_counts())
    df_result.to_csv(outputfile, index=False)
    # return df_result


def save_clustering():
    
    filepath = f"data/clustering/dfs/ht.csv"
    df = pd.read_csv(filepath).dropna().reset_index(drop=True)
        
    print(f"language ht ents k10")
    clustering_kmeans(df, "text_ents", 10, f"data/clustering/results/ht_text_ents_k10_01.csv")

    del df


def save_dfs():
    langs = ["cbk-zam", "sg", "pih", "bi", "tpi", "jam", "pap", "gcr", "ht"]
    for lang in langs:
        filepath = f"data/annotated_wikidumps/{lang}.jsonl"
        df = load_json_data(filepath)
        df.to_csv(f"data/clustering/dfs/{lang}.csv", index=False)


def save_elbow_plots():
    langs = ["cbk-zam", "sg", "pih", "bi", "tpi", "jam", "pap", "gcr", "ht"]
    for lang in tqdm(langs):
        filepath = f"data/dfs/{lang}.csv"
        df = pd.read_csv(filepath)
        visualize_elbow(df, "text_clean", f"data/plots_elbow/{lang}_text_clean.png")
        visualize_elbow(df, "text_ents", f"data/plots_elbow/{lang}_text_ents.png")


if __name__ == '__main__':
    save_clustering()
