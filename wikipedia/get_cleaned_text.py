import glob

import bs4
import json
import os
import sys
import spacy
import jsonlines

from utils import process_entry

nlp = spacy.blank("en")
nlp.add_pipe('opentapioca')


def main(lang):
    output_dir = "output/cleaned_text"
    # pattern = f"/Users/yiyichen/Documents/experiments/datasets/wikidumps/text/AA/wiki_{lang}*"
    pattern = f"/Users/yiyichen/Documents/experiments/datasets/wikidumps/{lang}/AA/wiki_*"
    finished = [11, 16, 29, 20, 27, 18, 26, 19, 21, 17, 28, 10, 25, 13, 22, 23, 24, 12, 15, 2, 5, 4, 3]
    filepaths = glob.glob(pattern, recursive=False)

    output_json_file = os.path.join(output_dir, f"{lang}.jsonl")
    output_json_file_writer = jsonlines.open(output_json_file, mode="w")

    output_annos = os.path.join(output_dir, f"{lang}_annos_02.csv")
    output_annos_writer = open(output_annos, "w+")

    output_annos_writer.write("Text\tWiki_ID\tWikidata_ID\tSource\n")

    for filepath in filepaths:
        nr_ = int(os.path.basename(filepath).split("_")[-1])
        print(f"open file {filepath} nr {nr_}")

        if nr_ not in finished:

            with open(filepath) as f:
                for line in f:
                    line_ = json.loads(line)
                    text = line_["text"]
                    print(text)
                    print("===")
                    texts = text.split("\n")
                    linked_texts = []
                    for idx_text, text in enumerate(texts):
                        soup_ = bs4.BeautifulSoup(text, "html.parser").encode(formatter=None)
                        soup = bs4.BeautifulSoup(soup_, "html.parser")
                        soup_str = str(soup)
                        soup_str_ = soup_str
                        doc_ = soup_str  # for changing the text use
                        a_attrs = soup.find_all("a")

                        if a_attrs != []:
                            for link in a_attrs:
                                # l = link.get('href')  # WIKIPEDIA_ID
                                l_text = link.get_text()  # WIKIPEDIA_Title
                                u = process_entry(l_text, lang)
                                if u != "boohoo":
                                    wiki_id, wikidata_id = u
                                    output_annos_writer.write(f"{l_text}\t{wiki_id}\t{wikidata_id}\tWikipedia\n")
                                    print(f"{l_text}\t{wiki_id}\t{wikidata_id}\tWikipedia\n")
                                    soup_str_ = soup_str_.replace(str(link), f"[[{str(l_text)}]]")
                                else:
                                    # output_annos_writer.write(f"{l_text}\t{None}\t{None}\tWikipedia\n")
                                    soup_str_ = soup_str_.replace(str(link), f"{str(l_text)}")
                            linked_texts.append(soup_str_)


                    linked_text = " ".join(linked_texts)
                    line_["linked_text"] = linked_text
                    output_json_file_writer.write(line_)
                    print(linked_text)
                    print("*" * 80)
        finished.append(nr_)
        print("finished:", finished)
    output_json_file_writer.close()
    output_annos_writer.close()


if __name__ == '__main__':
    # Hatian Creole, Chavacano, Guianan Creole, Papiamento, Jamaican Creole, Tok Pisin, Bislama,
    creoles = ["ht", "gcr", "pap", "jam", "tpi", "bi", "pih", "sg"]
    # finished: pap, jam, "tpi", "bi", "pih", "sg"

    #  "cbk-zam", ht
    for lang in ["ht"]:
        main(lang)
