import os
import multiprocessing

import pandas as pd
from suffix_trees import STree
from sklearn.cluster import AffinityPropagation
from pandarallel import pandarallel
from thefuzz import fuzz, process

import numpy as np
from itertools import combinations
from sklearn.utils import shuffle
from tqdm import tqdm

pandarallel.initialize(progress_bar=True)


def run_aff_prop(inputfile):
    df = pd.read_csv(inputfile)
    df = df.drop_duplicates(subset=["text_preprocessed"]).drop_duplicates(subset=["text_preprocessed"]).reset_index(
        drop=True)
    df = shuffle(df)

    X_fuzz = pd.crosstab([df.index, df.text_preprocessed], df.text_preprocessed).parallel_apply(
        lambda col: [fuzz.partial_ratio(col.name, x) for x in col.index.get_level_values(1)])

    X_data = X_fuzz.to_numpy()

    clustering = AffinityPropagation(random_state=42).fit(X_data)
    df["label"] = clustering.predict(X_data)

    return X_fuzz, df


def ranking_clusters(X_fuzz, df):

    df["score"]= [np.nan for _ in range(len(df))]

    for label in set(df["label"].tolist()):
        indices_label = df[df.label==label].index.tolist()

        scores_label = []
        for pair in combinations(indices_label, 2):
            t1, t2 = pair
            score = X_fuzz.iloc[t1, t2]
            scores_label.append(score)

        mean_score = np.mean(scores_label)
        for indice in indices_label:
            df.loc[indice, "score"] = mean_score

    df.sort_values(by="score", ascending=False, inplace=True)

    return df



def lcs_aff_df(df, filename):


    df_lcs_ls = []
    for label_idx, count in tqdm(df["label"].value_counts().items()):
        df_i = df[df["label"]==label_idx].reset_index(drop=True)
        # X_data on lcs
        X_data = pd.crosstab([df_i.index, df_i.text_preprocessed], df_i.text_preprocessed).parallel_apply(
            lambda col: [len(STree.STree([col.name, x]).lcs()) for x in col.index.get_level_values(1)])
        clusteing = AffinityPropagation(random_state=42).fit(X_data)

        df_i[f"aff_lcs"] = clusteing.predict(X_data)
        df_i[f"aff_lcs_label"] = df_i["label"].astype(str)+ '-' +df_i[f"aff_lcs"].astype(str)

        df_lcs_ls.append(df_i)

    df_new = pd.concat(df_lcs_ls)
    df_new = df_new.sort_values(by='score', ascending=False)

    df_new.to_csv(f"data/affinityPropagation/results/{filename}")



if __name__ == '__main__':
    inputfolder = "data/clustering/dataframes/"

    for file in os.listdir(inputfolder):
        if file.endswith(".csv"):
            print(f"processing file {file}")
            filepath = os.path.join(inputfolder, file)

            X_fuzz, df = run_aff_prop(filepath)
            df = ranking_clusters(X_fuzz, df)
            lcs_aff_df(df, file)


