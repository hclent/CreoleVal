import os
import glob
import nltk
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from transformers import AutoTokenizer, MT5Tokenizer


nltk.download("punkt")


def calculate_factors(df_path, bin_count=4, outpath=None):
    """
    pass
    """
    df = pd.read_csv(df_path, sep="\t", index_col=0)
    df.fillna("", inplace=True)
    # print(df.tail())
    # exit(1)
    df = df.filter(items=["source_sent", "gold_sent", "correct_pair", "predicted_sent"])

    # source sentence length
    df["src_len"] = df["source_sent"].apply(lambda x: len(nltk.word_tokenize(x)))

    # source sentence subwords
    src_subwords = [subwords for subwords in df["source_sent"].apply(lambda x: tokenizer.tokenize(x))]
    # gold sentence subwords
    gold_subwords = [subwords for subwords in df["gold_sent"].apply(lambda x: tokenizer.tokenize(x))]

    # source fertility
    df["src_subw_len"] = [len(sw) for sw in src_subwords]
    df["src_fertility"] = round(df["src_subw_len"] / df["src_len"], 3)

    # intersection
    intersects = []

    for src_sw, gold_sw in zip(src_subwords, gold_subwords):
        src_set, gold_set = set(src_sw), set(gold_sw)
        matched = src_set.intersection(gold_set)
        intersect = len(matched)
        intersects.append(intersect)

    df["subw_intersect_count"] = intersects
    df["subw_intersect_ratio"] = round(df["subw_intersect_count"] / df["src_subw_len"], 3)

    print(df)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Arguments to plot fertility values.")
    parser.add_argument("input_folder", help="path to the folder containing all samples")
    parser.add_argument("-o", "--output_folder", help="path to the folder where the plots should be output")

    args = parser.parse_args()

    all_samples = os.path.join(args.input_folder, "**/**/**.tsv")

    for tsv in sorted(glob.glob(all_samples)):

        print(tsv)

        lang_pair_full = os.path.dirname(tsv)  # full name of the language pair (including sample name)
        model_name = os.path.basename(os.path.dirname(lang_pair_full))  # model_name

        if model_name == "mt5-base":
            tokenizer = MT5Tokenizer.from_pretrained("google/mt5-base")
        elif model_name == "random":
            pass
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_name)

        calculate_factors(tsv)
        break
