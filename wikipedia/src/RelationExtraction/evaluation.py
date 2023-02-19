import json
import pandas as pd
import plac


def create_gold_dataset(lang):
    datafile = f"data/post-processed/partial/{lang}.csv"
    df = pd.read_csv(datafile, sep="\t")
    with open(f"data/triples-wd/{lang}.json") as f:
        triples = json.load(f)

    with open(f"data/properties/{lang}.json") as f:
        properties_lang = json.load(f)

    indices = []
    triples_extracted = []
    properties = []
    for idx, item in df.iterrows():
        ent1 = item["Left_ID"]
        ent2 = item["Right_ID"]
        property = item["Property"]
        if [ent1, ent2, property] in triples or [ent2, ent1, property] in triples:
            properties.append(property)
            triples_extracted.append((ent1, ent2, property))

            indices.append(idx)

    df_gold = df.iloc[indices]

    print(
        f"original:{len(df)}, gold:{len(df_gold)}, #triples {len(set(triples_extracted))}, #properties {len(set(properties))} #total properties {len(properties_lang)}")
    df_gold.to_csv(f"data/gold/{lang}.csv", index=False, sep="\t")


if __name__ == '__main__':
    plac.call(create_gold_dataset)
