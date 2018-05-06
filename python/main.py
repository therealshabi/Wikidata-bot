from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
from flask import Flask, request
from flask_restful import Resource, Api

# sentence = """Who is Yuvraj Singh?"""
# tokens = nltk.word_tokenize(sentence)
# print(tokens)
# tagged = nltk.pos_tag(tokens)
# entities = list(nltk.chunk.ne_chunk(tagged))
# ans = str(entities[2])
# ans = ans.split(" ")
# print(ans)

# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# sparql.setQuery("""
#     SELECT ?author_name ?title
#     WHERE {
#     ?author rdf:type dbo:Writer .
#     ?author rdfs:label ?author_name .
#     ?author dbo:notableWork ?work .
#     ?work rdfs:label ?title
#      }
#      LIMIT 10
# """)
#
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# for result in results["results"]["bindings"]:
#      print('%s: %s' % (result["author_name"]["value"], result["title"]["value"]))




# Create a engine for connecting to SQLite3.
# Assuming salaries.db is in your app root folder

app = Flask(__name__)
api = Api(app)


class Departments_Meta(Resource):
    def get(self):
        return {'departments': "Shahbaz"}


class Departmental_Salary(Resource):
    def get(self, department_name):
        result = {'data': department_name}
        return result
        # We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient


api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/')

if __name__ == '__main__':
    app.run()