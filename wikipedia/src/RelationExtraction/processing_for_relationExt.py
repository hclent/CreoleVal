import json
import os
from itertools import combinations
import regex

import pandas as pd
import jsonlines
import spacy

from termcolor import cprint


def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text == "[[" or token.text == "]]":
            doc[token.i].is_sent_start = False
        return doc


nlp = spacy.load("xx_ent_wiki_sm")
nlp.add_pipe("sentencizer")
tokenizer = nlp.tokenizer


# data is very limited , maybe also due to the quality of OpenTapioca
# other ways to get more entities:
# 1. string matching the entities found already  in the text
# 2. entity extraction using spacy and check whether it exists in wikidata.
#

def get_stats_each_lang(lang):
    # how many entities, and filter out the sentences.
    outputfolder = "data/ent_extraction"

    inputfolder = "data/annotated_wikidumps"
    inputfile = os.path.join(inputfolder, f"{lang}.jsonl")

    data = []
    pattern = r"\[\[(.*?)\]\]"
    p = regex.compile(pattern)
    with open(inputfile, "r", encoding="utf-8-sig") as f:
        for line in f.readlines():
            line = json.loads(line)
            linked_text = line["linked_text"]

            if "[[" in linked_text and "]]" in linked_text:
                clean_text = linked_text.replace("[[", "").replace("]]", "")

                ents = []  # entities in one doc, not sentence
                ent_counter = 0
                ent_in_text = []
                for m in p.finditer(linked_text):
                    ent = m.group()
                    ent_start = m.start()
                    ent_str = ent.replace("[[", "").replace("]]", "")
                    ent_start_ = ent_start - 4 * ent_counter
                    ent_counter += 1
                    ent_in_text.append((ent_str, ent_start_))

                doc = nlp(clean_text)
                for sent in doc.sents:
                    sent_start = sent[0].idx
                    sent_end = sent[-1].idx + len(sent[-1])

                    sent_copy = sent.text

                    ent_in_sent = []
                    for t in ent_in_text:
                        ent_str, ent_s = t
                        ent_e = ent_s + len(ent_str)

                        if ent_e < sent_end and ent_s > sent_start:
                            # to make sure the entities are in the corresponding sentences.
                            ent_start_new = ent_s - sent_start
                            ent_end = ent_start_new + len(ent_str)

                            ent_in_sent.append((ent_str, ent_start_new, ent_end))

                    if len(ent_in_sent) > 1 and len(ent_in_sent) < 6:
                        tokens = [token.text for token in sent]

                        edgesets = list()
                        for comb in combinations(ent_in_sent, 2):
                            e1, e2 = comb

                            e1_ent, e1_start, e1_end = e1
                            e2_ent, e2_start, e2_end = e2
                            # need the span rather than offsets

                            def get_index_for_ents(e, tokens):

                                e_l = tokenizer(e)
                                e_s = e_l[0].text
                                e_e = e_l[-1].text
                                e_start_pos = tokens.index(e_s)
                                e_end_pos = tokens.index(e_e)
                                return [x for x in range(e_start_pos, e_end_pos+1)]

                            try:
                                e1_pos = get_index_for_ents(e1_ent, tokens)
                                e2_pos = get_index_for_ents(e2_ent, tokens)

                                if e1 != e2:
                                    edgesets.append({"left": e1_pos,
                                                     "right": e2_pos})
                            except Exception as msg:
                                print(tokens, len(tokens))
                                print(ent_in_sent)
                                print(msg)
                                print("*"*40)

                        if len(edgesets) > 0:
                            # print(tokens, len(tokens))
                            # print(ent_in_sent)
                            # print(tokens, len(tokens))
                            # print(ent_in_sent)

                            data_entry = {
                                "tokens": tokens,
                                "edgeSet": edgesets
                            }
                            # print(data_entry)

                            data.append(data_entry)

    cprint(f"{lang} data length {len(data)}")
    outputfile = os.path.join(outputfolder, f"{lang}.json")
    with open(outputfile, "w") as writer:
        json.dump(data, writer)


if __name__ == '__main__':
    import plac

    plac.call(get_stats_each_lang)
