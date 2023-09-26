"""
This script evaluates the language model performance by running the Tateoba task.
"""

import os
import csv
import glob
import faiss
import types
import random
import argparse
import numpy as np
import pandas as pd
import transformers
from tqdm import tqdm
from transformers import AutoTokenizer, AutoConfig, AutoModel, pipeline, MT5EncoderModel, MT5Tokenizer


transformers.logging.set_verbosity_error()


def random_baseline(source, target, k=1):
    """
    Creates a random baseline using source and target sentences.
    """
    random_preds = []

    target_ids = range(len(target))

    for sentence in source:
        choice = random.choices(target_ids, k=k)
        random_preds.append(choice[0])

    return random_preds


def get_scores_predictions(x, y, dim, k=1):
    """
    Calculates cosine similarities of two groups of sentences.

    :param x: source sentences
    :param y: target sentences
    :param dim: dimensionality of the model
    :param k: the number of results to return
    :return: a tuple of scores and predictions
    """
    idx = faiss.IndexFlatL2(dim)
    faiss.normalize_L2(x)
    faiss.normalize_L2(y)
    idx.add(y)
    scores, predictions = idx.search(x, k)
    return scores, predictions


# function from XTREME
def accuracy(labels, preds):
    correct = sum([int(l == p) for p, l in zip(preds, labels)])
    accuracy_score = float(correct) / len(preds)
    return {"accuracy": round(accuracy_score * 100, 2)}


def average_pooling(sentence):
    """
    Given an input sentence it retrieves the average of the token embeddings.

    :param sentence: str
    :return: numpy array of embeddings
    """
    embeddings = []
    embeds = pipe(sentence, framework="pt", device=0)[0]
    for embed in embeds:
        embed = np.asarray(embed).astype(np.float32)
        embeddings.append(embed)
    return np.mean(embeddings, axis=0)


def process_sentences(sentences):
    """
    Create sentence embeddings from the mean of the pooled subword tokens
    for multiple sentences.

    :param sentences:
    :return: numpy array of average pooled embeddings
    """
    pooled_sentences = []
    with tqdm(total=len(sentences), desc="Iterating: ") as pbar:
        for sentence in sentences:
            pooled_sentence = average_pooling(sentence)
            pooled_sentences.append(pooled_sentence)
            pbar.update(1)
    return np.asarray(pooled_sentences)


def main(input_path, output, model, dimensions, experiment_name=None):
    """
    Function to call a single Tatoeba translation pair detection experiment.

    :param input_path: filepath to the tsv containing source and target sentences and the labels
    :param output_path: filepath to the results of the experiment
    """
    source_sents = []
    target_sents = []
    gold_sents = []
    labels = []

    lang_names = os.path.basename(input_path).rstrip(".tsv")

    with open(input_path, "r") as infile:
        tatoeba_reader = csv.reader(infile, delimiter="\t", quotechar="|")
        next(tatoeba_reader, None)  # skip the header
        for source_sent, target_sent, target_id, gold_sent, gold_id in tatoeba_reader:
            source_sents.append(source_sent)
            target_sents.append(target_sent)
            gold_sents.append(gold_sent)
            labels.append(gold_id)

    labels = [int(label) for label in labels]

    if model == "random":
        top_k = random_baseline(source_sents, target_sents)
        top_scores = [1 for k in top_k]

    else:
        src_embeds = process_sentences(source_sents)
        trg_embeds = process_sentences(target_sents)

        scores, predictions = get_scores_predictions(src_embeds, trg_embeds, dimensions, k=1)

        # evaluation
        top_k = [p[0] for p in predictions]
        top_scores = [s[0] for s in scores]

    top_k_metric = accuracy(labels, top_k)
    top_correct = [str(p == l) for p, l in zip(top_k, labels)]

    # return sentences
    predicted_sentences = [target_sents[label] for label in top_k]

    # label if it is a correct pair
    pair = ["True" if label == pred else "False" for label, pred in zip(labels, top_k)]

    output_df = pd.DataFrame({
        "source_sent": source_sents,
        "gold_sent": gold_sents,
        "predicted_sent": predicted_sentences,
        "true_id": labels,
        "predicted_id": top_k,
        "correct_pair": pair,
        "cosine_similarity": top_scores})

    # output paths
    if "/" in model:
        model = model.split("/")[1]
    if experiment_name:
        output_folder = os.path.join(output, model, experiment_name)
    else:
        output_folder = os.path.join(output, model, lang_names)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    metric_path = os.path.join(output_folder, "accuracy.txt")
    df_path = os.path.join(output_folder, "output.tsv")

    with open(metric_path, "w") as outfile:
        outfile.write(f"{top_k_metric}")

    output_df.to_csv(df_path, sep="\t")

    print()
    print(lang_names)
    print(top_k_metric)
    print()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Arguments for running the Tatoeba test.")
    parser.add_argument("input_path", help="filepath to the input file containing source and target sentences and the labels")
    parser.add_argument("output_folder", help="folder where the outputs of the experiments are saved")
    parser.add_argument("model", help="language model to use: for now it is valid to use model names from the huggingface model hub")
    parser.add_argument("--max_length", type=int, default=512, help="max length of an input sequence, defaults to 512")
    parser.add_argument("-e", "--experiment_name", help="experiment name, if not given, the experiment is named after the languages used")

    args = parser.parse_args()

    # model_name = "bert-base-multilingual-cased"
    model_name = args.model


    if model_name == "google/mt5-base":
        config = AutoConfig.from_pretrained(model_name)
        model = MT5EncoderModel.from_pretrained(model_name, config=config)
        tokenizer = MT5Tokenizer.from_pretrained(model_name)
    elif model_name == "random":
        pass
    else:
        config = AutoConfig.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name, config=config)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # max_length = config.max_position_embeddings
    max_length = 512

    if model_name != "random":
        dimensions = config.hidden_size
        pipe = pipeline("feature-extraction", model=model, tokenizer=tokenizer)


        # function from https://stackoverflow.com/questions/71240331/getting-an-error-even-after-using-truncation-for-tokenizer-while-predicting-mlm
        def _my_preprocess(self, inputs, max_length=max_length, return_tensors=None, **preprocess_parameters):
            if return_tensors is None:
                return_tensors = self.framework
            model_inputs = self.tokenizer(inputs, truncation=True, max_length=max_length,
                                        return_tensors=return_tensors)
            return model_inputs


        # preprocess method is replaced to allow the truncation of input
        pipe.preprocess = types.MethodType(_my_preprocess, pipe)
    else:
        dimensions = 0

    main(args.input_path, args.output_folder, model_name, dimensions, experiment_name=args.experiment_name)

