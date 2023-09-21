import os
import pandas as pd
import regex
from SPARQLWrapper import SPARQLWrapper, JSON
import time
import urllib.error
import urllib.request
from ast import literal_eval


# if entity == "lookup":
#     e = "the item"  # "[ the item]] in brackets"
#     qcode = query_wikidata(e)
#
# elif entity.startswith("https://en.wikipedia.org/"):
#     qcode = query_wikidata(url)
#
# elif entity.startswith("https://https://www.wikidata.org")
#     qcode = url.split("/wiki/")[-1]  # just grab the Code
#
# else:
#     # I've written the entity as plain English, which should be easy to look up
#     qcode = query_wikidata(string)


def get_entities(text):
    pattern = r"\[\[(.*?)\]\]"
    p = regex.compile(pattern)
    ents = []
    for m in p.finditer(text):
        ent = m.group()
        ents.append(ent.replace("[[", "").replace("]]", ""))
    return tuple(ents)


def handling_qcode_list(qcodes):
    pass


def query_wikidata(label, lang):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    query_0 = "SELECT * WHERE {"
    query_1 = f"?s ?label \"{label}\"@{lang}."
    query_2 = "}"
    query_str = query_0 + query_1 + query_2
    print("query ->", query_str)
    sparql.setQuery(query_str)
    sparql.setReturnFormat(JSON)
    q = sparql.query()
    results = q.convert()

    prefix = "http://www.wikidata.org/entity/"
    qcode_dict = {}
    if results["results"]["bindings"] is not []:
        for item in results["results"]["bindings"]:
            qid = item["s"]["value"]
            if prefix in qid:
                qid = qid.replace(prefix, "")
                qid_ = qid.replace("Q", "")
                try:
                    qcode_dict[qid] = int(qid_)
                except Exception:
                    continue

    print(qcode_dict)
    sorted_qcode_dict = dict(sorted(qcode_dict.items(), key=lambda x: x[1]))
    return list(sorted_qcode_dict.keys())


def query_wikipedia_url(ent):
    title = ent.replace("https://en.wikipedia.org/wiki/", "")
    query = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={title}&format=json"
    req = urllib.request.Request(query)
    try:
        resource = urllib.request.urlopen(req)
        with resource as response:
            page = response.read().decode(resource.headers.get_content_charset())
            page_d = literal_eval(page)
            qcode = list(page_d["query"]["pages"].values())[0]["pageprops"]["wikibase_item"]
            return qcode

    except urllib.error.HTTPError as e:
        print(e.reason)
        return None


def handle_entity(ent, ent_found, lang):
    if ent.startswith("https://en.wikipedia.org/"):
        # query wikidata item using wikipedia link
        qcode = query_wikipedia_url(ent)
        return qcode
    elif ent.startswith("https://www.wikidata.org/wiki/"):
        return ent.split("/wiki/")[-1]
    else:

        qcode = query_wikidata(ent_found, lang)
        if len(qcode) > 0:
            print(qcode)
            return "Q" + qcode[0]
        else:
            if ent != "lookup":
                # ent is english
                qcode_ = query_wikidata(ent, "en")
                if len(qcode_) > 0:
                    print(qcode_)
                    return qcode_[0]
                else:
                    print("no qcode!")
                    return None
            else:
                print("no qcode!")
                return None


def processing_one_file(filepath):
    filename = os.path.basename(filepath)
    lang = filename.replace(".csv", "").replace("2023-04-24-", "")
    dfdict = pd.read_csv(filepath, sep="|").to_dict(orient="index")
    properties = []
    e1s = []
    e2s = []
    sentences = []
    for _, d in dfdict.items():
        print("*" * 20)
        e1 = d["e1"]
        e2 = d["e2"]
        sentence = d["Sentence"]
        property = d["Property"]

        t = get_entities(sentence)
        if len(t) == 2:
            e1_, e2_ = t
            print(sentence)
            e1_qcode = handle_entity(e1, e1_, lang=lang)
            e2_qcode = handle_entity(e2, e2_, lang=lang)
            if e1_qcode is None:
                print(e1, e1_)
            if e2_qcode is None:
                print(e2, e2_)
            sentences.append(sentence)
            properties.append(property)
            e1s.append(e1_qcode)
            e2s.append(e2_qcode)


        else:
            print("no entities extracted")
            print(t)
            print(sentence)

    df = pd.DataFrame.from_dict({
        "Property": properties,
        "e1": e1s,
        "e2": e2s,
        "Sentence": sentences
    })
    outputpath = filepath.replace(".csv", "").replace(lang, f"{lang}_output.csv")
    df.to_csv(outputpath, index=False)


if __name__ == '__main__':
    import plac

    plac.call(processing_one_file)
    # query_wikidata("Bochotnica", "bi")
