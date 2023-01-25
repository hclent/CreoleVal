import json
import os
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

    pattern = r"\[\[(.*?)\]\]"
    p = regex.compile(pattern)
    with open(inputfile, "r", encoding="utf-8-sig") as f:
        for line in f.readlines():
            line = json.loads(line)
            linked_text = line["linked_text"]

            if "[[" in linked_text and "]]" in linked_text:
                doc = nlp(linked_text)
                # cprint(linked_text, "magenta")
                for sent in doc.sents:
                    text = sent.text
                    if "[[" in text and "]]" in text:

                        clean_text = text.replace("[[", "").replace("]]", "")

                        ents_in_one_set = []
                        counter_ent_in_one_sent = 0

                        for m in p.finditer(text):
                            # print(m.start(), m.group(), m.span())
                            ent = m.group()

                            ent_str = ent.replace("[[", "").replace("]]", "")
                            ent_start = m.start() - 2 - 4 * counter_ent_in_one_sent

                            ents_in_one_set.append((ent_str, ent_start))
                            # cleaned_entity = m.group().replace("[[", "").replace("]]", "")
                            counter_ent_in_one_sent += 1

                        if counter_ent_in_one_sent > 1 and counter_ent_in_one_sent < 20:
                            cprint(text, "magenta")
                            print(ents_in_one_set)
                            print(counter_ent_in_one_sent)

                            print("*" * 20)

                # entities = regex.findall(pattern, text)
                # if len(entities) > 1 and len(entities) < 20:
                #     cprint(text, "green")
                #     cprint(" ~ ".join(entities), "magenta")
                #     for entity in entities:
                #         print(entity.span())
                #     print(clean_text)


if __name__ == '__main__':
    import plac

    plac.call(get_stats_each_lang)
