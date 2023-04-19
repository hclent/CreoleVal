"""
This script allows the preparation of Tatoeba data to the right format.
"""

import os
import csv
import glob
import random
import argparse


COLUMNS = ["source_sent", "target_sent", "target_id", "gold_sent", "gold_id"]


def main(input_folder, output_dir, random_seed, threshold):
    """
    Takes a source and target file from the Tatoeba sets,
    shuffles the target file and outputs the shuffled set
    and the correct indices in a tsv.

    :param source_file: .src file
    :param target_file: .trg file
    :param output_dir: directory to store the tsv in
    :param random_seed: 42 by default for reproducibility
    :param threshold: if set, an assertion error is thrown if it is not met by the file set
    """
    random.seed(random_seed)

    # lang names
    lang_names = os.path.basename(input_folder)
    lang1, lang2 = lang_names.split("-")

    source_files = os.path.join(input_folder, "**.src")
    target_files = os.path.join(input_folder, "**.trg")

    source_set = []
    target_set = []

    for source_file in sorted(glob.glob(source_files)):
        with open(source_file, "r") as infile:
            source_sents = infile.read().split("\n")
            source_set.extend(source_sents)

    for target_file in sorted(glob.glob(target_files)):
        with open(target_file, "r") as infile:
            target_sents = infile.read().split("\n")
            target_set.extend(target_sents)

    # with open("cbk_test.tsv", "w") as outfile:
    #     csv_writer = csv.writer(outfile, delimiter="\t", quotechar="|")
    #     for s, t in zip(source_set, target_set):
    #         row = [s, t]
    #         csv_writer.writerow(row)
    #
    # exit(1)

    # make sure that the source set is non-English or non-French and the target set is English or French
    if lang1 in ("eng", "fra"):
        source_set, target_set = target_set, source_set
        lang_names = f"{lang2}-{lang1}"

    # if the length of the source set is above threshold, pick 3 samples of 1000 sentences
    sample_idx = dict()

    if len(source_set) > threshold:
        sample_idx["sample1"] = random.sample(range(len(source_set)), 1000)
        sample_idx["sample2"] = random.sample(range(len(source_set)), 1000)
        sample_idx["sample3"] = random.sample(range(len(source_set)), 1000)
    else:
        try:
            sample_idx["sample"] = random.sample(range(len(source_set)), 1000)
        except ValueError:
            sample_idx["sample"] = range(len(source_set))

    for idx, (sample, indices) in enumerate(sample_idx.items()):

        sampled_source_set = [src_sent for src_idx, src_sent in enumerate(source_set) if src_idx in indices]
        sampled_target_set = [trg_sent for trg_idx, trg_sent in enumerate(target_set) if trg_idx in indices]

        sampled_target_set = [(trg_sent, trg_idx) for trg_idx, trg_sent in enumerate(sampled_target_set)]
        random.shuffle(sampled_target_set)
        
        labels = []
        gold_sents = []

        for src_idx, src_sent in enumerate(sampled_source_set):
            for trg_sent, trg_idx in sampled_target_set:
                if src_idx == trg_idx:
                    label = sampled_target_set.index((trg_sent, trg_idx))
                    gold_sents.append(trg_sent)
                    labels.append(label)

        if len(sample_idx.keys()) > 1:
            output_path = os.path.join(output_dir, f"{lang_names}_sample{idx+1}.tsv")
        else:
            output_path = os.path.join(output_dir, f"{lang_names}.tsv")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, "w") as outfile:
            writer = csv.writer(outfile, delimiter="\t", quotechar="|")
            writer.writerow(COLUMNS)
            for src_sent, (trg_sent, trg_idx), label, gold_sent in zip(sampled_source_set, sampled_target_set, labels, gold_sents):
                row = [src_sent, trg_sent, trg_idx, gold_sent, label]
                writer.writerow(row)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="arguments for preparing the sets for Tatoeba evaluation")
    parser.add_argument("input_folder", help="path to the folder containing the source and target sets")
    parser.add_argument("-o", "--output_dir", help="directory where the processed files should be put out, default is ./data/",
            default="./data/")
    parser.add_argument("-r", "--random_seed", help="random seed for reproducibility, 42 by default", default=42, type=int)
    parser.add_argument("-t", "--threshold",
            help="minimum sentence count of the source and target sets, if set, it creates 3 random samples as test sets",
            type=int, default=2000)

    args = parser.parse_args()

    main(args.input_folder, args.output_dir, args.random_seed, args.threshold)

