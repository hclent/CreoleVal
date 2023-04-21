import os
import glob
import nltk
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from transformers import AutoTokenizer, MT5Tokenizer


nltk.download("punkt")
plt.style.use("seaborn")

BINS = {1: [""],
        2: ["low", "high"],
        3: ["low", "moderate", "high"],
        4: ["very low", "medium low", "medium high", "very high"]
        }


def calculate_factors(df_path, bin_count=4, outpath=None):
    """
    Given a tsv with experimental outputs, it calculates source fertility
    and subword intersect ratio between source and target sentences.
    """
    if isinstance(df_path, str):
        df = pd.read_csv(df_path, sep="\t", index_col=0)
    else:
        df = df_path
    df.fillna("", inplace=True)
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
        intersect = len([subw for subw in src_sw if subw in gold_sw])
        intersects.append(intersect)

    df["subw_intersect_count"] = intersects
    df["subw_intersect_ratio"] = round(df["subw_intersect_count"] / df["src_subw_len"], 3)

    # # unk tokens
    # unks = []
    # for src_sw in src_subwords:
    #     unk = len([sw for sw in src_sw if sw in {"[UNK]", "<unk>"}])
    #     unks.append(unk)
    #
    # df["src_unks"] = unks

    # arrange factors into bins
    for factor_name in {"src_fertility", "subw_intersect_ratio"}:
        df[f"binned_{factor_name}"] = pd.qcut(df[factor_name], q=bin_count, duplicates="drop")

    if outpath:
        df.to_csv(outpath, sep="\t")
    return df


def return_bin_values(df, factor):
    """
    Given a dataframe and a factor,
    it returns a binned representation of the factor.
    """
    bin_dict = defaultdict(dict)
    binned_factor = f"binned_{factor}"

    df_filtered = df.filter(items=[binned_factor, "correct_pair"])
    grouped_df = df_filtered.groupby(binned_factor)

    for bin_group, group in grouped_df:
        correct_count = sum(group["correct_pair"])
        bin_size = len(group)
        accuracy = round(correct_count / bin_size * 100, 2)
        bin_dict[bin_group]["accuracy"] = accuracy
        bin_dict[bin_group]["size"] = bin_size

    return pd.DataFrame(bin_dict, index=None).T


def plot_binned_table(df, factor, output_path, **kwargs):
    """
    Provided an input dataframe, the function plots the bins on a bar chart.
    """
    if factor != "src_unks":
        bin_names = BINS[len(df)]
        index_dict = {k: i for k, i in zip(df.index, bin_names)}
        df.rename(index=index_dict, inplace=True)
    # else:

    ax = df.plot.bar(y="accuracy", rot=0, legend=False, **kwargs)

    # annotate bar chart for the size of the bins
    for p, s in zip(ax.patches, df["size"]):
        percentage = round(s / df["size"].sum() * 100)
        ax.annotate(f"{percentage}%",
                    (p.get_x() + p.get_width() / 2,  # x coordinate
                     p.get_height()),  # y coordinate
                    xytext=(0, 0),
                    textcoords="offset points",
                    ha="center",
                    va="bottom")

    if output_path:
        plt.savefig(output_path)
    # plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Arguments to plot fertility values.")
    parser.add_argument("input_folder", help="path to the folder containing all samples")
    parser.add_argument("-o", "--output_folder", help="path to the folder where the plots should be output")
    parser.add_argument("-b", "--bin_count", help="count of bins to assign data into")

    args = parser.parse_args()

    all_samples = os.path.join(args.input_folder, "**/**/**.tsv")

    full_df = None

    for tsv in sorted(glob.glob(all_samples)):

        dir_name = os.path.dirname(tsv)

        if dir_name.endswith("sample1"):
            dfs = []
            df_to_sample1 = pd.read_csv(tsv, sep="\t", index_col=0)
            dfs.append(df_to_sample1)
            continue
        elif dir_name.endswith("sample2"):
            df_to_sample2 = pd.read_csv(tsv, sep="\t", index_col=0)
            dfs.append(df_to_sample2)
            continue
        elif dir_name.endswith("sample3"):
            df_to_sample3 = pd.read_csv(tsv, sep="\t", index_col=0)
            dfs.append(df_to_sample3)
            full_df = pd.concat(dfs, ignore_index=True)

        lang_pair_full = os.path.dirname(tsv)  # full name of the language pair (including sample name)
        model_name = os.path.basename(os.path.dirname(lang_pair_full))  # model_name
        lang_pair = os.path.basename(lang_pair_full)

        if (lang_pair.endswith("sample1") or
                lang_pair.endswith("sample2") or
                lang_pair.endswith("sample3")):
            lang_pair = lang_pair[:-8]

        if model_name == "mt5-base":
            tokenizer = MT5Tokenizer.from_pretrained("google/mt5-base")
        elif model_name == "random":
            continue
        else:
            tokenizer = AutoTokenizer.from_pretrained(model_name)

        if full_df is not None:
            factor_df = calculate_factors(full_df)
        else:
            factor_df = calculate_factors(tsv)

        lg, eng = lang_pair.split("-")

        for factor in {"src_fertility", "subw_intersect_ratio"}:

            if factor == "subw_intersect_ratio":
                xlabel = f"Ratio of token overlap ({lg})"
                factor_name = "subword intersect ratio"
            elif factor == "src_fertility":
                xlabel = f"Tokenizer fertility ({lg})"
                factor_name = "sentence fertility"
            # elif factor == "src_unks":
            #     xlabel = f"Unknown token count ({lg})"
            #     factor_name = "unknown tokens"

            kwargs = {"xlabel": xlabel,
                      "ylabel": "Accuracy scores"
                      }

            bin_df = return_bin_values(factor_df, factor)

            if len(bin_df) > 0:

                output_dir = os.path.join(args.output_folder, "analysis", model_name, factor)

                os.makedirs(output_dir, exist_ok=True)

                output_path = os.path.join(output_dir, f"{lg}.pdf")

                plot_binned_table(bin_df, factor, output_path=output_path, **kwargs)

        full_df = None
