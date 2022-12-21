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
    output_dir = "output"
    # pattern = f"/Users/yiyichen/Documents/experiments/datasets/wikidumps/text/AA/wiki_{lang}*"
    pattern = f"/Users/yiyichen/Documents/experiments/datasets/wikidumps/{lang}/AA/wiki_*"
    finished = [0, 1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 22, 23, 24, 25, 30, 31]
    # finished = [0, 1, 2, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 22, 23, 24, 25, 30, 31, 11, 16, 29, 20, 27]
    # remember to change the file path
    filepaths = glob.glob(pattern, recursive=False)
    output_json_file = os.path.join(output_dir, f"{lang}_04.jsonl")
    output_json_file_writer = jsonlines.open(output_json_file, mode="w")

    output_annos = os.path.join(output_dir, f"{lang}_annos_04.csv")
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
                        else:
                            doc = nlp(doc_)
                            offset_start = 0
                            offset_end = 0

                            for span in doc.ents:
                                if span.text:
                                    print((span.text, span.kb_id_, span.label_, span._.description, span._.score,
                                           span.start_char,
                                           span.end_char))
                                    output_annos_writer.write(f"{span.text}\t{None}\t{span.kb_id_}\tOpenTapioca\n")
                                    doc_ = doc_[:span.start_char + offset_start] + "[[" + span.text + "]]" + doc_[
                                                                                                             span.end_char + offset_end:]
                                    offset_start += 4
                                    offset_end += 4
                            linked_texts.append(doc_)

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
    # ht: "ht/text/AA..." 11,16,29,20,27,18,26,19,21,17,28,10,03(not finished)
    # finished: pap, jam, "tpi", "bi", "pih", "sg"
    #  "cbk-zam"
    for lang in ["ht"]:
        main(lang)
