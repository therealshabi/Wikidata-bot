from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

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