import os.path

import numpy as np
import plac
from SPARQLWrapper import SPARQLWrapper, JSON
import time
import pandas as pd



def get_query(t1, t2):
    query_before = """
    SELECT ?item
    WHERE 
{
  """
    # wd:Q686 ?item  wd:Q6256 .
    # wd:Q423 ?property wd:Q18808.
    query = f"wd:{t1} ?item wd:{t2}."

    query_after = """ 
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""
    query_string = query_before + query + query_after
    return query_string


def run_one_query(t1, t2):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query_string = get_query(t1, t2)
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    q = sparql.query()
    results = q.convert()

    property_list = []
    if results["results"]["bindings"] is not []:
        for item in results["results"]["bindings"]:
            qid = item["item"]["value"].split("/")[-1]
            property_list.append(qid)

    return t1, t2, property_list


def processing_one_lang(file):
    # data/relation_extraction/qcodes/bi.csv
    df = pd.read_csv(file)
    print(file)
    basename = os.path.basename(file)
    writer = open(os.path.join("data/relation_extraction/properties", basename), "w+")
    writer.write("ENT1\tENT2\tProperties\n")

    for e1, e2 in zip(df["e1"], df["e2"]):
        try:
            e1, e2, properties = run_one_query(e1, e2)
            print(e1, e2, properties)
            if properties:
                writer.write(f"{e1}\t{e2}\t{properties}\n")
            else:
                print(f"{e1}, {e2}")
                writer.write(f"{e1}\t{e2}\t{np.NAN}\n")
        except Exception as msg:
            print(msg)
            time.sleep(120)
            print("sleeping...")


# Property,e1,e2,Sentence
# P1376,Q216,Q37,[[Vilnius]] i kapital blong [[Litwania]].

if __name__ == '__main__':
    import plac
    plac.call(processing_one_lang)