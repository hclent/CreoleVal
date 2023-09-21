import pandas as pd
from suffix_trees import STree
from sklearn.cluster import AffinityPropagation
from pandarallel import pandarallel
from thefuzz import fuzz, process

pandarallel.initialize(progress_bar=True)


def affinity_propagation_stree(lang):
    inputfile = f"data/fuzzywuzzy/dfs/{lang}.csv"
    df = pd.read_csv(inputfile)
    # filter by the k value
    df = df[["text", "text_preprocessed"]].drop_duplicates(subset=["text_preprocessed"]).reset_index(
        drop=True)
    print(f"loading {lang}, len {len(df)}")

    X_data = pd.crosstab([df.index, df.text_preprocessed], df.text_preprocessed).parallel_apply(
        lambda col: [len(STree.STree([col.name, x]).lcs()) for x in col.index.get_level_values(1)])

    clustering = AffinityPropagation(random_state=42).fit(X_data)
    df["label"] = clustering.predict(X_data)

    df.to_csv(f"data/affinityPropagation/stree+aff/{lang}.csv", index=False)


def affinity_propagtion_on_fuzzywuzzy(lang):
    inputfile = f"data/fuzzywuzzy/dfs/{lang}.csv"
    df = pd.read_csv(inputfile)
    df = df.drop_duplicates(subset=["text_preprocessed"]).drop_duplicates(subset=["text_preprocessed"]).reset_index(
        drop=True)
    print(f"loading {lang}, len {len(df)}")

    X_fuzz = pd.crosstab([df.index, df.text_preprocessed], df.text_preprocessed).parallel_apply(
        lambda col: [fuzz.partial_ratio(col.name, x)
                     for x in col.index.get_level_values(1)])

    X_data = X_fuzz.to_numpy()
    clustering = AffinityPropagation(random_state=42).fit(X_data)
    df["label"] = clustering.predict(X_data)

    df.to_csv(f"data/affinityPropagation/fuzzy+aff/{lang}.csv", index=False)


def main(lang, data_alg):
    if data_alg == "fuzzy":
        print(f"language {lang} -> {data_alg}")
        affinity_propagtion_on_fuzzywuzzy(lang)
    if data_alg == "stree":
        affinity_propagation_stree(lang)


if __name__ == '__main__':
    import plac

    plac.call(main)
