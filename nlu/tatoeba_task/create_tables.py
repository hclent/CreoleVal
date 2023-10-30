import os
import csv
import glob
import argparse
import pandas as pd
from statistics import mean
from collections import defaultdict


def extract_scores(input_folder):
    """
    When provided an input folder for an experiment, it extracts the accuracy and average cosine similarity scores, and returns the experiment name and these scores.

    :param input_folder: path pointing at the folder containing the output of an experiment
    :return: a tuple of experiment name, accuracy and average cosine similarity scores
    """
    experiment_name = os.path.basename(input_folder)
    accuracy_path = os.path.join(input_folder, "accuracy.txt")
    path_to_output = os.path.join(input_folder, "output.tsv")

    with open(accuracy_path, "r") as infile:
        content = infile.read()
        content = content.strip("{").strip("}")
        content = content.strip("'accuracy': ")
        accuracy = float(content)

    cosine_similarities = []

    with open(path_to_output, "r") as infile:
        csv_reader = csv.reader(infile, delimiter="\t", quotechar="|")
        next(csv_reader, None)
        for _, _, _, _, _, _, _, cosine_similarity in csv_reader:
            cosine_similarity = float(cosine_similarity)
            cosine_similarities.append(cosine_similarity)

    avg_cosine_similarity = round(mean(cosine_similarities), 3)

    return experiment_name, accuracy, avg_cosine_similarity
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Arguments for collecting experimental outputs in a single output file.")
    parser.add_argument("path_to_experiments", help="path to the folder containing the experimental outputs")
    parser.add_argument("-o", "--output_path",
                        help="path where the resulting table should be output, default is ./tables/results.tsv",
                        default="./tables/results.tsv")

    args = parser.parse_args()

    glob_pattern = os.path.join(args.path_to_experiments, "**/**")

    if not os.path.isdir(os.path.dirname(args.output_path)):
        os.mkdir(os.path.dirname(args.output_path))

    experiments = []
    output_dict = defaultdict(dict)

    for experiment in sorted(glob.glob(glob_pattern)):
        model_name = os.path.basename(os.path.dirname(experiment))
        experiment_name, accuracy, avg_cosine_sim = extract_scores(experiment)
        output_dict[experiment_name][f"{model_name}_acc"] = accuracy
        output_dict[experiment_name][f"{model_name}_cos"] = avg_cosine_sim

    df = pd.DataFrame.from_dict(output_dict).T

    df.to_csv(args.output_path, sep="\t")


