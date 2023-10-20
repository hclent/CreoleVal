"""
Description:    Given a file of translation hypothesis and a file of human references, calculate BLEU and chrF.
                Note than the sentence ID is not taken into account.
Usage:          python eval.py -sl <one of: en, es, fr> -r <path to results file>
"""

import argparse
import evaluate


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-sl", "--source_lang", type=str,
                        default='en')
    parser.add_argument("-r", "--results_file", type=str,
                        default='results.txt')
    args = parser.parse_args()
    return args


def main():

    args = create_arg_parser()

    # Load predictions
    with open(f'outputs/{args.source_lang}-ht.hyp', 'r') as hyp_file:
        hyp_lines = hyp_file.readlines()
    predictions = [l.split('\t')[1].rstrip() for l in hyp_lines]

    # Load references
    with open(f'../data/ht-{args.source_lang}.trg', 'r') as ref_file:
        ref_lines = ref_file.readlines()
    references = [[l.split('\t')[1].rstrip()] for l in ref_lines]

    # Compute BLEU and chrF
    sacrebleu = evaluate.load("sacrebleu")
    sacrebleu_results = sacrebleu.compute(predictions=predictions, references=references)
    chrf = evaluate.load("chrf")
    chrf_results = chrf.compute(predictions=predictions, references=references)

    # Write results to file
    with open(args.results_file, 'a') as res_file:
        res_file.write(f'======= {args.source_lang} - ht =======\n')
        res_file.write(f'BLEU: {sacrebleu_results["score"]}\nchrF: {chrf_results["score"]}\n\n')


if __name__ == '__main__':
    main()
