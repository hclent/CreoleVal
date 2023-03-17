import pandas as pd
from suffix_trees import STree
from sklearn.cluster import AffinityPropagation
import numpy as np
from tqdm import tqdm

from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


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

        # get the longest common substring
        # l_group_ls = []
        # for idx, group in df_i.groupby(by=[f"k{k}_label"]):
        #     if len(group) > 1:
        #         lcs = STree.STree(group.text_preprocessed.tolist()).lcs()
        #         lcs_l = [lcs for _ in range(len(group))]
        #         l_group_ls += lcs_l
        #     else:
        #         l_group_ls += [np.nan]
        #
        # assert len(df_i) == len(l_group_ls)
        #
        # df_i[f"k{k}_LCS"] = l_group_ls

        # df_i = df_i[["text", "text", f"k{k}_label", f"k{k}_LCS"]]
        df_i = df_i[["text", "text", f"k{k}_label"]]

        df_k_ls.append(df_i)

    df_new = pd.concat(df_k_ls)
    df_new.to_csv(f"data/affinityPropagation/{lang}_{k}.csv", index=False)


if __name__ == '__main__':
    import plac
    plac.call(affinity_propagation)
