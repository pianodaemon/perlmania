import logging
import os
from flask import Flask, request, jsonify, json, Blueprint, abort, make_response
from flask_restplus import Api, Resource
import dal.studs


provider_api = Blueprint('provider_api', __name__)
api = Api(provider_api)

@api.route('/providers')
class ProviderList(Resource):
    def get(self):
        """
        Procedure to obtain part of contract list for the pagination
        Read the page from the query string /contratos?size=20&page=3
        """
        #Query string /providers?page_number&page_size&order_byy&asc
        page_number = request.args.get('page_number')
        page_size   = request.args.get('page_size')
        order_by    = request.args.get('order_by')
        asc         = request.args.get('asc')
        #Function pending

    def post(self):
        """Create the contract"""
        req = request.data
        dicReq = json.loads(req)
        dal.studs.create_provider(**dicReq)


@api.route('/providers/<int:provider_id>')
class Provider(Resource):

    def get(self, provider_id):
        """Get a dictionary of the contract fields and send them to the client"""
        res = dal.studs.find_provider(provider_id)

    def put(self, provider_id):
        """Edit the contract by Id"""
        #Edit the provider row but you must enter a title [Exception: duplicate key value violates unique constraint "provider_unique_title"]
        req = request.data
        dicReq = json.loads(req)
        dicReq['provider_id'] = provider_id
        dal.studs.edit_provider(**dicReq)

    def delete(self, provider_id):
        """Block the contract"""
        dal.studs.block_provider(provider_id)


