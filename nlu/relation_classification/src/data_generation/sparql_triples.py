import os.path

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


def run_query(datafile):
    df = pd.read_csv(datafile, sep="\t")

    entity_pairs_1 = list(set([(ent1, ent2) for ent1, ent2 in zip(df["Left_ID"], df["Right_ID"])]))
    entity_pairs_2 = list(set([(ent2, ent1) for ent1, ent2 in zip(df["Left_ID"], df["Right_ID"])]))
    entity_pairs = entity_pairs_1 + entity_pairs_2

    print(entity_pairs)
    print(len(entity_pairs))

    basename = os.path.basename(datafile)
    writer = open(os.path.join("data/triples-wd", basename), "w+")
    writer.write("ENT1\tENT2\tProperties\n")
    for entity_pair in entity_pairs:
        ent1, ent2 = entity_pair
        try:
            t1, t2, property_list = run_one_query(ent1, ent2)
            if property_list:
                print(t1, t2, property_list)
                writer.write(f"{t1}\t{t2}\t{property_list}\n")
        except Exception as msg:
            print(msg)
            time.sleep(120)
            print("sleeping...")
    writer.close()


if __name__ == '__main__':
    plac.call(run_query)
