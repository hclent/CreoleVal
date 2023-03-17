import pandas as pd
from suffix_trees import STree
from sklearn.cluster import AffinityPropagation
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


def affinity_propagation_all(lang):
    inputfile = f"data/fuzzywuzzy/df_results/{lang}.csv"
    df = pd.read_csv(inputfile)
    # filter by the k value
    df = df[["text", "text_preprocessed"]]

    X_data = pd.crosstab([df.index, df.text_preprocessed], df.text_preprocessed).parallel_apply(
        lambda col: [len(STree.STree([col.name, x]).lcs()) for x in col.index.get_level_values(1)])

    clustering = AffinityPropagation(random_state=42).fit(X_data)
    df["label"] = clustering.predict(X_data)

    df.to_csv(f"data/affinityPropagation/results_all/{lang}.csv", index=False)


if __name__ == '__main__':
    import plac

    plac.call(affinity_propagation_all)
