import os, json, requests
from flask import Flask, url_for, render_template, request, jsonify, Blueprint


from general import URLFrp

bp = Blueprint('catalogs', __name__,
                        template_folder='templates')



@bp.route('/getAllContracts', methods=['POST'])
def getAllContracts():

    #Obtiene todos contracts para el select
    urlCountContracts = URLFrp + 'contracts/count'
    countAmountContracts = requests.get( urlCountContracts ).json()['count']

    queryStrContracts = 'contracts/?offset=0&limit=' + str(countAmountContracts)
    urlContracts = URLFrp + queryStrContracts

    rContracts = requests.get( urlContracts ) 
    contracts = rContracts.json() 
    
    return jsonify(contracts)


@bp.route('/getAllProjects', methods=['POST'])
def getAllProjects():

    #Obtiene todos projects para el select
    urlCountContracts = URLFrp + 'projects/count'
    countAmountContracts = requests.get( urlCountContracts ).json()['count']

    queryStrContracts = 'projects/?offset=0&limit=' + str(countAmountContracts)
    urlContracts = URLFrp + queryStrContracts

    rContracts = requests.get( urlContracts ) 
    contracts = rContracts.json() 
    
    return jsonify(contracts)


@bp.route('/getAllCategories', methods=['POST'])
def getAllCategories():

    #Obtiene todos projects para el select
    url = URLFrp + 'catalogues/categories'

    rContracts = requests.get( url ) 
    contracts = rContracts.json() 
    
    return jsonify(contracts)



