import os
import multiprocessing

from joblib import Parallel, delayed
import pandas as pd
from suffix_trees import STree
from sklearn.cluster import AffinityPropagation
import numpy as np
from tqdm import tqdm
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


def get_lcs(group):
    if len(group) > 1:
        lcs = STree.STree(group.text.tolist()).lcs()
        lcs_l = [lcs for _ in range(len(group))]
        group["LCS"] = lcs_l


def applyParallel(dfGrouped, func):
    retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(func)(group) for name, group in dfGrouped)
    return pd.concat(retLst)


def write_lcs_df(inputfile):
    basename = os.path.basename(inputfile)
    dirname = os.path.dirname(inputfile)
    lang, k = basename.replace(".csv", "").split("_")

    df = pd.read_csv(inputfile)
    # get the longest common substring
    df["LCS"] = [np.nan for _ in range(len(df))]
    # for idx, group in df.groupby(by=[f"k{k}_label"]):
    applyParallel(df.groupby(df[f"k{k}_label"]), get_lcs)

    df[f"k{k}_LCS"] = df["LCS"]

    df = df[["text", f"k{k}_label", f"k{k}_LCS"]]
    df.to_csv(os.path.join(dirname, "results", basename))


def affinity_propagation(lang, k):
    inputfile = f"data/fuzzywuzzy/df_results/{lang}.csv"
    df = pd.read_csv(inputfile)
    # filter by the k value
    df = df[["text", "text_preprocessed", f"k{k}"]]
    print(f"{inputfile} k {k} distribution:")
    print(df[f"k{k}"].value_counts())

    df_k_ls = []

    for k_idx, count in tqdm(df[f"k{k}"].value_counts().items()):
        # reset index necessary for the next step.
        df_i = df[df[f"k{k}"] == k_idx].reset_index(drop=True)

        print(f"{k_idx} -> {len(df_i)}")
        # generate x data by the LCS among texts.
        print("loading the data")
        X_data = pd.crosstab([df_i.index, df_i.text_preprocessed], df_i.text_preprocessed).parallel_apply(
            lambda col: [len(STree.STree([col.name, x]).lcs()) for x in col.index.get_level_values(1)])

        print("clustering...")
        # appply affinity propagation
        clusteing = AffinityPropagation(random_state=42).fit(X_data)

        df_i[f"k{k}_{k_idx}"] = clusteing.predict(X_data)
        df_i[f"k{k}_label"] = df_i[f"k{k}"].astype(str)+'_'+df_i[f"k{k}_{k_idx}"].astype(str)


        df_i = df_i[["text", "text_preprocessed", f"k{k}_label"]]

        df_k_ls.append(df_i)

    df_new = pd.concat(df_k_ls)
    df_new.to_csv(f"data/affinityPropagation/{lang}_{k}.csv", index=False)


if __name__ == '__main__':
    import plac
    plac.call(affinity_propagation)
