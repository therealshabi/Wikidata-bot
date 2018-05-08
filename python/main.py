from SPARQLWrapper import SPARQLWrapper, JSON
import json
from vocabulary.vocabulary import Vocabulary as vb
from nlp import find_entities, query_properties


named_entity = find_entities("Who is the wife of Yuvraj Singh?")

property_code = []
properties = open('property.json','r')
properties = json.load(properties)
print(type(properties))
for noun in query_properties:
    noun_synonyms = vb.synonym(noun, format="dict")
    for p, prop in properties.items():
        if prop==noun:
            property_code.append(p)
        else:
            for synonym in noun_synonyms.itervalues():
                if prop == synonym:
                    property_code.append(p)
print(property_code)

str = "Yuvraj Singh"
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
query = """
  SELECT ?name ?dob ?spouse WHERE {
  ?person rdfs:label ?name .
  ?person wdt:P569 ?dob .
  ?person wdt:P106 ?occupation .
  ?occupation wdt:P279* wd:Q12299841.
  ?person wdt:P26 ?spouse_id .
  ?spouse_id rdfs:label ?spouse .
  FILTER(STR(?name) = '""" + str + """' && LANG(?spouse) = "en")
}
LIMIT 1
"""
print query
sparql.setQuery(query)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
print(results)

# for result in results["results"]["bindings"]:
#      print('%s: %s' % (result["author_name"]["value"], result["title"]["value"]))


