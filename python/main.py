import json

from SPARQLWrapper import SPARQLWrapper, JSON
from flask import Flask
from flask_restful import Resource, Api
from vocabulary.vocabulary import Vocabulary as vb

# imported from nlp.py (local file created by the developer)
from nlp import find_entities


# function to process the sparql query for the required query on a subject
def obtain_result(named_entity, query_properties):
    """
     an array to store property codes for wikidata query,
      as wikidata needs code not natural language for SPARQL query
    """
    property_code = []

    # if there are any query properties then only search for it's code
    if len(query_properties) != 0:
        # loading properties with it's code from property.json file which is property dump of wikidata
        properties = open('property.json', 'r')
        properties = json.load(properties)
        print(type(properties))

        # extracting the first query from the query properties list
        noun = query_properties[0]

        """
        finding the synonyms of the queried property using a library called vocabulary
        so that it matches the property from wikidata
            E.g. wikidata doesn't have a property wife, but it has a property spouse, so it'll 
            consider the property code corresponding to spouse property
        """
        noun_synonyms = vb.synonym(noun, format="dict")

        # checking if the query itself is a property in the property.json file
        for p, prop in properties.items():
            if prop == noun:
                property_code.append(p)
                break

        # if the query is not found as a property in property.json file, then search in it's synonyms
        if len(property_code) == 0:
            # dict.items() extracts key and value from a dictionary
            for p, prop in properties.items():
                # vocabulary returns bool if there isn't any synonym for a particular word
                if type(noun_synonyms) != bool:
                    # dict.itervalues basically iterate through the values of the dictionary
                    for synonym in noun_synonyms.itervalues():
                        if prop == synonym:
                            property_code.append(p)
                            break

        print(property_code)

    # if our NLP program fails to detect the named entity (subject) from the query sentence, then flag an error response
    if len(named_entity) != 0:

        """
         if there is any query for properties then use wikidata for that
         E.g :- Who is the wife of Shahrukh Khan? Here, "wife" is the query property and "Shahrukh Khan" is the subject
        """
        if len(property_code) != 0:
            flag = 0
            sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
            query = """SELECT ?label ?property ?thumbnail WHERE
                        { 
                        ?entity rdfs:label ?label .
                        ?entity wdt:""" + property_code[0] + """ ?property_id .
                        ?property_id rdfs:label ?property .
                        OPTIONAL { ?property_id wdt:P18 ?thumbnail .}
                        FILTER (STR(?label) = '""" + named_entity[0] + """') .
                        FILTER (LANG(?property) = "en")
                        }"""
            print query
        else:
            """
            if there is no query for any property then use dbpedia for extracting the abstract of that entity
                E.g : Who is Shahrukh Khan? Note: There is no query property, but there is a subject 
            """
            flag = 1
            sparql = SPARQLWrapper("https://dbpedia.org/sparql")
            query = """SELECT ?label ?description ?thumbnail WHERE
                { 
                ?entity rdfs:label ?label .
                ?entity dbo:abstract ?description .
                ?entity dbo:thumbnail ?thumbnail .
                FILTER (STR(?label) = '""" + named_entity[0] + """' && LANG(?description) = "en") .
                }
                LIMIT 1"""
            print query

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        global result
        result = list()
        temp = str()
        try:
            results = sparql.query().convert()
            print(results)

            # parsing the result obtained from SPARQLquery
            if flag == 0:
                # parsing for wikidata
                for data in results["results"]["bindings"]:
                    result.append(data["property"]["value"])

                    # if the thumbnail do not exist for an entity
                    if "thumbnail" in data and data["thumbnail"]["value"] != "":
                        temp = data["thumbnail"]["value"]
            else:
                # parsing for dbpedia
                for data in results["results"]["bindings"]:
                    result.append(data["description"]["value"])

                    # if the thumbnail do not exist for an entity
                    if "thumbnail" in data and data["thumbnail"]["value"] != "":
                        temp = data["thumbnail"]["value"]

            # removing redundant data from the result set, by using set function and then converting it to a list
            result = list(set(result))
            response = []
            for i in result:
                print(i)
                # encoding required to remove the 'u' character from the list elements, by deafult there in Python list
                response.append(u''.join(i).encode('utf-8'))
            print(response)

            # Response sent as result status, the data and the thumbnail for that data
            if flag == 0:
                data = {"status": "200", "data": response, "thumbnail": temp}
            else:
                data = {"status": "200", "data": response, "thumbnail": temp}
            result = json.dumps(data)
            print(results)
        except:
            response = ["Unable to retrieve data"]
            data = {"status": "500", "data": response}
            result = json.dumps(data)
            raise
    else:
        response = ["Unable to retrieve data"]
        data = {"status": "500", "data": response}
        result = json.dumps(data)

    print(result)
    return result


# Flask API for communication with the frontend of the webpage \

app = Flask(__name__)
api = Api(app)


# get request for /wiki/<string:query>
class Query(Resource):
    def get(self, query):
        print query
        """
        extracting the named entity (proper noun) and 
        query properties (the property to be queried for the subject
         -> common noun basically using NLP (nlp.py)
        """
        named_entity, query_properties = find_entities(query)
        response = obtain_result(named_entity, query_properties)
        return response


api.add_resource(Query, '/wiki/<string:query>')

if __name__ == '__main__':
    app.run()
