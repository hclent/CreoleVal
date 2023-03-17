import os
import pandas as pd


def combine_dfs(lang, folder="data/fuzzywuzzy/results/", outputfolder="data/fuzzywuzzy/df_results"):
    df = pd.DataFrame()
    for file in os.listdir(folder):
        if file.endswith(".csv") and file.startswith(lang):

            lang_, k = file.replace(".csv", "").split("_")
            assert lang_ == lang

            filepath = os.path.join(folder, file)
            print(f"loading file {filepath}")

            df_ = pd.read_csv(filepath, index_col=0)
            if df.empty:
                df = df_[["text", "text_preprocessed"]]

            assert len(df) == len(df_)

            df[k] = df_["fuzzy_cluster"]
            del df_
    df.to_csv(os.path.join(outputfolder, f"{lang}.csv"), index=False)


if __name__ == '__main__':
    import plac

    plac.call(combine_dfs)
