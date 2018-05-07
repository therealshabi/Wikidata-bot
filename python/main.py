from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
import json
from vocabulary.vocabulary import Vocabulary as vb

vb.synonym("wife")

def parts_of_speech(corpus):
    "returns named entity chunks in a given text"
    sentences = nltk.sent_tokenize(corpus)
    tokenized = [nltk.word_tokenize(sentence) for sentence in sentences]
    pos_tags = [nltk.pos_tag(sentence) for sentence in tokenized]
    common_nouns = []
    print(pos_tags[0])
    for name, tag in pos_tags[0]:
        if tag == 'NN':
            common_nouns.append(name)
    print(common_nouns)
    chunked_sents = nltk.ne_chunk_sents(pos_tags, binary=True)
    return chunked_sents


def find_entities(chunks):
    "given list of tagged parts of speech, returns unique named entities"

    def traverse(tree):
        "recursively traverses an nltk.tree.Tree to find named entities"

        entity_names = []

        if hasattr(tree, 'label') and tree.label:
            if tree.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in tree]))
            else:
                for child in tree:
                    entity_names.extend(traverse(child))

        return entity_names

    named_entities = []

    for chunk in chunks:

        entities = sorted(list(set([word for tree in chunk
                                    for word in traverse(tree)])))
        for e in entities:
            if e not in named_entities:
                named_entities.append(e)
    return named_entities

print find_entities(parts_of_speech("What is the height of Yuvraj Singh?"))

properties = open('property.json','r')
properties = json.load(properties)
print(type(properties))
for p, prop in properties.items():
    if prop=="spouse":
        print p

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


app = Flask(__name__)
api = Api(app)


class Departments_Meta(Resource):
    def get(self):
        return jsonify(departments="Shahbaz")


class Departmental_Salary(Resource):
    def get(self, department_name):
        print department_name
        result = {'data': department_name}
        return jsonify(result)
        # We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient


api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/')

# if __name__ == '__main__':
#     app.run()

