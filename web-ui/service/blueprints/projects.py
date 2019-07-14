import os, json, requests
from flask import Flask, url_for, render_template, request, jsonify, Blueprint


from general import URLFrp, menuProject

bp = Blueprint('projects', __name__,
                        template_folder='templates')


@bp.route('/projects', methods=['GET', 'POST'])
def projectsList():

    #Renderiza el template de la lista de proveedores
    if request.method == 'GET':
        
        return render_template( 'projects/index.html', catalog='projects', menu = menuProject, title='Obras' )
    
    else:
        data = request.get_json()
        
        paginationStart     = data['paginationStart']
        paginationStep      = data['paginationStep']
        paginationBy        = data['by']
        paginationOrder     = data['order']
        searchBy            = data['searchBy']
        valueSearchBy       = data['valueSearchBy']
        

        if searchBy == '':
            urlCount = URLFrp + 'projects/count'
            searchQuery = '' 
        else:
            urlCount = URLFrp + 'projects/count?' + searchBy + '=' + valueSearchBy
            searchQuery = '&'+ searchBy +'=' + valueSearchBy


        countAmount = requests.get( urlCount ).json()['count']
        queryStr = 'projects/?offset=' + str(paginationStart) + '&limit=' + str(paginationStep) + searchQuery
        url = URLFrp + queryStr


        r = requests.get( url) 
        dataRes = r.json() 
        
        return jsonify( { 'data' : dataRes, 'count' : countAmount} )



#Agrega project
@bp.route('/projects/add', methods=['GET', 'POST'])
def projectsAdd():

    #Renderiza el template del formulario para agregar un 
    if request.method == 'GET':
        
        #Obtiene todos contracts para el select
        urlCountContracts = URLFrp + 'contracts/count'
        countAmountContracts = requests.get( urlCountContracts ).json()['count']

        queryStrContracts = 'contracts/?offset=0&limit=' + str(countAmountContracts)
        urlContracts = URLFrp + queryStrContracts

        rContracts = requests.get( urlContracts ) 
        contracts = rContracts.json() 
        

        return render_template( 'projects/add.html', catalog='projects', menu = menuProject, contracts = contracts )
    

    #Cuando termina de cargar la pagina el javascrip pide la lista de los proveedores
    else:
        data = request.get_json()

        dicData = { 
            'title'         : data['title'         ], 
            'description'   : data['description'   ], 
            'city'          : data['city'          ], 
            'category'      : data['category'      ], 
            'department'    : data['department'    ], 
            'budget'        : data['budget'        ], 
            'contract'      : data['contract'      ], 
            'planed_kickoff': data['planed_kickoff'], 
            'planed_ending' : data['planed_ending' ], 
            'inceptor_uuid' : data['inceptor_uuid' ], 
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'projects/'
        r = requests.post( url, data=dataJSON)

        return jsonify( {'status_code': r.status_code } )



#Edita projects
@bp.route('/projects/edit/<int:provider_id>', methods=['GET', 'POST', 'DELETE'])
def projectsEdit(provider_id):

    #Renderiza el template del formulario para agregar un proveedor
    if request.method == 'GET':
        
        url = URLFrp + 'projects/' + str(provider_id)
        r = requests.get( url) 
        reqJ = r.json()

        if reqJ['id'] == None:
            displayExistRegister = "display:none;"
            titleDontExist = 'El registro no existe'
        else:
            displayExistRegister = ""
            titleDontExist = ''
        
        #Obtiene todos contracts para el select
        urlCountContracts = URLFrp + 'contracts/count'
        countAmountContracts = requests.get( urlCountContracts ).json()['count']

        queryStrContracts = 'contracts/?offset=0&limit=' + str(countAmountContracts)
        urlContracts = URLFrp + queryStrContracts

        rContracts = requests.get( urlContracts ) 
        contracts = rContracts.json() 
        
        return render_template( 'projects/edit.html', 
                                data = reqJ, 
                                catalog = 'projects', 
                                menu = menuProject, 
                                contracts = contracts,
                                displayExistRegister = displayExistRegister,
                                titleDontExist = titleDontExist
                        )
    
    #Cuando termina de cargar la pagina el javascrip pide la lista de los proveedores
    elif request.method == 'POST':
        data = request.get_json()
        
        idRegister = data['id']

        dicData = { 
            'title'         : data['title'         ], 
            'description'   : data['description'   ], 
            'city'          : data['city'          ], 
            'category'      : data['category'      ], 
            'department'    : data['department'    ], 
            'budget'        : data['budget'        ], 
            'contract'      : data['contract'      ], 
            'planed_kickoff': data['planed_kickoff'], 
            'planed_ending' : data['planed_ending' ], 
            'inceptor_uuid' : data['inceptor_uuid' ], 
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'projects/' + idRegister
        r = requests.put( url, data=dataJSON)

        return jsonify( {'status_code': r.status_code} )

    elif request.method == 'DELETE':
        url = URLFrp + 'projects/' + str(provider_id)
        r = requests.delete( url )
        return jsonify( {'status_code': r.status_code } )




