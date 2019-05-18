import os
import logging
from flask import Flask,  request, jsonify, json
from markupsafe import Markup, escape 
from jinja2 import Template  
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix 
import psycopg2
from dal.studs import *
#from otherClass.providers import Provider, ProviderList

app = Flask(__name__)
api = Api(app, version='1.0', title='Obras API',
    description='Sistema de Control de Gastos de Obras Publicas',
)

conn = psycopg2.connect(dbname="minus", user="minuxpos", host="localhost", password="")
cur = conn.cursor()


@app.route("/")
def hello():
    app.logger.debug('HELLO!!!!!!!!!!')
    return "<h1 style='color:blue'>Hello There!</h1>"


@api.route('/contracts')
class ContractList(Resource):
    def get(self):
        """
        Procedure to obtain part of contract list for the pagination
        Read the page from the query string /contratos?size=20&page=3
        """
        
        cur.execute("SELECT * FROM contracts;")
        ob = cur.fetchone()
        print(ob)
        return ob[3]
        

    def post(self):
        """Create the contract"""
        req = request.data
        dicReq = json.loads(req)
        create_contract(**dicReq)


@api.route('/contracts/<int:contract_id>')
class Contract(Resource):

    def get(self, contract_id):
        """Get a dictionary of the contract fields and send them to the client"""
        
        cur.execute("SELECT * FROM contracts WHERE id=' "+ str(contract_id) +"';")
        ob = cur.fetchone()
        print(ob)
        return ob[0] #Id of contract

    def put(self, contract_id):
        """Edit the contract by Id"""
        req = request.data
        dicReq = json.loads(req)
        edit_contract(**dicReq)

    def delete(self, contract_id):
        """Block the contract"""
        block_contract(contract_id)


@api.route('/projects')
class ProjectList(Resource):
    def get(self):
        """ 
        Procedure to obtain part of project list for the pagination
        Read the page from the query string /proyectos?size=20&page=3
        """
        return {projects: {}}

    def post(self):
        """Create the project"""
        create_project(**kwargs)


@api.route('/projects/<int:project_id>')
class Project(Resource):

    def get(self, project_id):
        """ Get a dictionary of the project fields and send them to the client"""
        return {project: {}}

    def put(self, project_id):
        """Edit the contract"""
        edit_project(**kwargs)

    def delete(self, project_id):
        """Block the project"""
        block_project(project_id)




if __name__ == "__main__":
    app.run(host='0.0.0.0')
else:
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

