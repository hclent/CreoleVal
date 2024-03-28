import pandas as pd
import json
from collections import defaultdict

transformers = ['bert-base-multilingual-cased', 'xlm-roberta-base']
encoders = ['bert-base-nli-mean-tokens',
    'bert-large-nli-mean-tokens',
    'xlm-r-100langs-bert-base-nli-mean-tokens',
    'xlm-r-bert-base-nli-mean-tokens']

for m in transformers:
    for encoder in encoders:
        print(f"model-encoder: {m}_{encoder}")
        record_dict = defaultdict(dict)
        if "bert" in m:
            seeds = [300, 563, 757, 991 ]
        else:
            seeds = [563, 757, 991]

        for seed in seeds:
            filepath = f"output/{m}_{encoder}_{seed}.json"
            print(f"loading {filepath}")
            with open(filepath) as f:
                data = json.load(f)
            assert data["model"]["seed"] == str(seed)
            # bi, cbk-zam, jam, tpi
            record_dict["Dev(en)"][seed] = data["model"]["dev"]
            for creole in ["bi", "cbk-zam", "jam", "tpi"]:
                record_dict[creole][seed] = data["creoles"][creole]

        df = pd.DataFrame.from_dict(record_dict, orient="index")
        df.to_csv(f"output/{m}_{encoder}_results.csv")
        print(df)
