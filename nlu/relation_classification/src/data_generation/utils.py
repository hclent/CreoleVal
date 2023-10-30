from itertools import islice
import requests


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def process_entry(entry, lang):
    """
    Get Wikidata ID from a Wikipedia page's title
    :param entry: a wikipedia page's title, e.g., "Yunaeted Nesen"
    :param lang: Specify a wikipedia language code, e.g., "bi"
    :return:
    """
    try:
        template = f"https://{lang}.wikipedia.org/w/api.php?action=query&format=json&prop=pageprops&titles=" + "{}"
        req = requests.get(url=template.format(entry)).json()
        print(req)
        page_id = list(req["query"]["pages"].keys())[0]
        qcode = req['query']['pages'][page_id]['pageprops']['wikibase_item']
        return page_id, qcode
    except Exception as e:
        return "boohoo"


def retrieve_relation_type(entity1, entity2):

    """SELECT ?l
    WHERE {
      wd:Q5571382 ?p wd:Q223243 .
      ?property ?ref ?p .
      ?property rdf:type wikibase:Property .
      ?property rdfs:label ?l FILTER (lang(?l) = "en")
    }"""

    query_string_01 = """
    SELECT ?l ?property
    WHERE{
    """
    
    query_string_02 = f"{entity1} ?p {entity2} ."

    query_string_03 = """
    ?property ?ref ?p .
    ?property rdf:type wikibase:Property .
    ?property rdfs:label ?l FILTER (lang(?l) = "en")
    }
    """

    return query_string_01 + query_string_02 + query_string_03




