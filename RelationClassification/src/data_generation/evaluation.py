import json
import pandas as pd
import plac


def create_gold_dataset(lang):
    with open("ZS_BERT/data/m5/idx2property.json") as f:
        trained_properties = json.load(f)

    seen_properties = set([trained_properties[str(x)] for x in range(108)])

    print(len(seen_properties))
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
    print(seen_properties)
    print(properties)
    print(properties_lang)

    unseen = set(properties).difference(seen_properties)
    unseen_total = set(properties_lang).difference(seen_properties)

    df_gold = df.iloc[indices]

    print(
        f"original:{len(df)}, gold:{len(df_gold)}, #triples {len(set(triples_extracted))}, #properties {len(set(properties))} #total properties {len(properties_lang)}")
    print(f"unseen total proeprties {len(unseen_total)} , unseen properties {len(unseen)}")
    # df_gold.to_csv(f"data/gold/{lang}.csv", index=False, sep="\t")


if __name__ == '__main__':
    plac.call(create_gold_dataset)
