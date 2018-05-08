from SPARQLWrapper import SPARQLWrapper, JSON
import json
from vocabulary.vocabulary import Vocabulary as vb
from nlp import find_entities
from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify


def obtain_result(named_entity, query_properties):
    property_code = []
    properties = open('property.json', 'r')
    properties = json.load(properties)
    print(type(properties))
    for noun in query_properties:
        noun_synonyms = vb.synonym(noun, format="dict")
        for p, prop in properties.items():
            if prop == noun:
                property_code.append(p)
                break
            else:
                if type(noun_synonyms) != bool:
                    for synonym in noun_synonyms.itervalues():
                        if prop == synonym:
                            property_code.append(p)
                            break
    print(property_code)

    if (len(property_code) != 0):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        query = """SELECT ?label ?property WHERE
                    { 
                    ?entity rdfs:label ?label .
                    ?entity wdt:""" + property_code[0] + """ ?property_id .
                    ?property_id rdfs:label ?property .
                    FILTER (STR(?label) = '""" + named_entity[0] + """') .
                    FILTER (LANG(?property) = "en")
                    }
                    LIMIT 1"""
        print query
    else:
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
        query = """SELECT ?label ?description WHERE
                    { 
                    ?entity rdfs:label ?label .
                    ?entity dbo:abstract ?description .
                    FILTER (STR(?label) = '""" + named_entity[0] + """') .
                    }"""
        print query

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    result = str()
    for result in results["results"]["bindings"]:
        result = result["property"]["value"]
    result = json.loads('{ "data" : "'+result+'"}')
    return result



app = Flask(__name__)
api = Api(app)


class Departments_Meta(Resource):
    def get(self):
        return jsonify(departments="Shahbaz")


class Query(Resource):
    def get(self, query):
        print query
        named_entity, query_properties = find_entities(query)
        result = obtain_result(named_entity, query_properties)
        return jsonify(result)
        # We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient


api.add_resource(Query, '/dept/<string:query>')
api.add_resource(Departments_Meta, '/')

if __name__ == '__main__':
    app.run()
