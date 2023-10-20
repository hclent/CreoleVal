"""
Description:    Given a file containing data in the format <ID TAB SOURCE_SENTENCE>, translate the sentence using a
                pre-trained OPUS MT model and write results to file in the format: <ID TAB TRANSLATION>
Usage:          python translate.py -sl <one of: en, es, fr>
"""

import argparse
from transformers import pipeline


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sl", "--source_lang", type=str,
                        default='en')
    args = parser.parse_args()
    return args


def main():

    args = create_arg_parser()

    # Load source file
    with open(f"../data/ht-{args.source_lang}.src", 'r') as source:
        f_lines = source.readlines()

    # Define model in HuggingFace pipeline
    translator = pipeline("translation", model=f"Helsinki-NLP/opus-mt-{args.source_lang}-ht")

    # Translate and write to file
    with open(f"outputs/{args.source_lang}-ht.hyp", "w") as outfile:
        for line in f_lines:
            id, sent = line.split('\t')
            outfile.write(f"{id}\t{translator(sent.rstrip())[0]['translation_text']}\n")


if __name__ == '__main__':
    main()
