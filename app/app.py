from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine, select, inspect, MetaData, Table, Column
from json import dumps
# from flask_marshmallow import Marshmallow

#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

e = create_engine('sqlite:///salaries.db')

app = Flask(__name__)
api = Api(app)
# ma = Marshmallow(app)

#Connect to databse

class Departments_Meta(Resource):
    def get(self):
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute("select distinct DEPARTMENT from salaries")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}

class Departmental_Salary(Resource):
    def get(self, department_name):
        parser = reqparse.RequestParser()
        parser.add_argument('start', type = str, required=True, help="Indicate letter of first last name to start (e.g., start=d)")
        parser.add_argument('stop', type = str, required=True, help="Indicate letter of first last name to stop (e.g., stop=e)")
        args = parser.parse_args()
        query = conn.execute("SELECT Name,`Employee Annual Salary`  FROM salaries WHERE Department=? AND Name BETWEEN ? and ?", [department_name.upper(), args['start'].upper(),args['stop'].upper()]) 
        return {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

class Positions_Meta(Resource):
    def get(self):
        conn = e.connect()
        #Perform query and return JSON data
        query = conn.execute('SELECT distinct `Position Title` FROM salaries').fetchall()
        return {'positions': [x[0] for x in query]}

api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')
api.add_resource(Positions_Meta, '/positions')
# api.add_resource(Department_Name_Range, '/dept/<string:department_name>')

if __name__ == '__main__':
    app.run(debug=True)