import os
import csv
import glob
import nltk
import argparse
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


nltk.download("punkt")
sns.set_color_codes("muted")


def plot_distribution(sentences, lang, output_folder):
    sentence_lengths = [len(nltk.word_tokenize(sent)) for sent in sentences]
    frequency_dict = Counter(sentence_lengths)
    lengths = [length for length, frequency in frequency_dict.items()]
    frequencies = [frequency for length, frequency in frequency_dict.items()]
    to_plot = {"word_count": lengths, "frequency": frequencies}
    sns.barplot(to_plot, x="word_count", y="frequency", color="b")
    outpath = os.path.join(output_folder, f"{lang}.pdf")
    plt.savefig(outpath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments to plot word count distribution of the sentences in samples")
    parser.add_argument("input_folder", help="path to the folder that contains all samples")
    parser.add_argument("output_folder", help="path to the folder where plots should be output")

    args = parser.parse_args() 

    all_samples = os.path.join(args.input_folder, "**.tsv")

    for tsv in glob.glob(all_samples):
       
        source_sents = []

        lang = os.path.basename(tsv).split(".")[0]
       
        with open(tsv, "r") as infile:
            tatoeba_reader = csv.reader(infile, delimiter="\t", quotechar="|")
            next(tatoeba_reader, None)  # skip the header
            for source_sent, _, _, _, _ in tatoeba_reader:
                source_sents.append(source_sent)

        plot_distribution(source_sents, lang, args.output_folder)

