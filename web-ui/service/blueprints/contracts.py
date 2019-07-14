import os, json, requests
from flask import Flask, url_for, render_template, request, jsonify, Blueprint


from general import URLFrp, menuContract

bp = Blueprint('contracts', __name__,
                        template_folder='templates')


#Paginacion
@bp.route('/contracts', methods=['GET', 'POST'])
def contractsList():

    #Renderiza el template de la lista de proveedores
    if request.method == 'GET':
        
        return render_template( 'contracts/index.html', catalog='contracts', menu = menuContract, title='Contratos' )
    
    else:
        data = request.get_json()
        
        paginationStart     = data['paginationStart']
        paginationStep      = data['paginationStep']
        paginationBy        = data['by']
        paginationOrder     = data['order']
        searchBy            = data['searchBy']
        valueSearchBy       = data['valueSearchBy']
        


        if searchBy == '':
            urlCount = URLFrp + 'contracts/count'
            searchQuery = '' 
        else:
            urlCount = URLFrp + 'contracts/count?' + searchBy + '=' + valueSearchBy
            searchQuery = '&'+ searchBy +'=' + valueSearchBy


        countAmount = requests.get( urlCount ).json()['count']
        queryStr = 'contracts/?offset=' + str(paginationStart) + '&limit=' + str(paginationStep) + searchQuery
        url = URLFrp + queryStr


        r = requests.get( url) 
        dataRes = r.json() 
        
        return jsonify( { 'data' : dataRes, 'count' : countAmount} )




#Agrega contract
@bp.route('/contracts/add', methods=['GET', 'POST'])
def contractsAdd():

    #Renderiza el template del formulario para agregar un proveedor
    if request.method == 'GET':
        
        
        #Obtiene todos providers para el select
        urlCountProviders = URLFrp + 'providers/count'
        countAmountProviders = requests.get( urlCountProviders ).json()['count']

        queryStrProviders = 'providers/?offset=0&limit=' + str(countAmountProviders)
        urlProviders = URLFrp + queryStrProviders

        rProviders = requests.get( urlProviders ) 
        providers = rProviders.json() 




        return render_template( 'contracts/add.html', catalog='contracts', menu = menuContract, providers =providers )
    
    #Cuando termina de cargar la pagina el javascrip pide la lista de los proveedores
    else:
        data = request.get_json()

        dicData = { 
            'number'                     : data['number'                   ], 
            'title'                      : data['title'                    ], 
            'description'                : data['description'              ], 
            'provider'                   : data['provider'                 ], 
            'delivery_stage'             : data['delivery_stage'           ], 
            'initial_contracted_amount'  : data['initial_contracted_amount'], 
            'kickoff'                    : data['kickoff'                  ], 
            'ending'                     : data['ending'                   ], 
            'down_payment'               : data['down_payment'             ], 
            'down_payment_amount'        : data['down_payment_amount'      ], 
            'ext_agreement'              : data['ext_agreement'            ], 
            'ext_agreement_amount'       : data['ext_agreement_amount'     ], 
            'final_contracted_amount'    : data['final_contracted_amount'  ], 
            'total_amount_paid'          : data['total_amount_paid'        ], 
            'outstanding_down_payment'   : data['outstanding_down_payment' ], 
            'adjudication'               : data['adjudication'             ], 
            'funding'                    : data['funding'                  ], 
            'program'                    : data['program'                  ], 
            "inceptor_uuid"              : "string"
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'contracts/'
        r = requests.post( url, data=dataJSON)

        return jsonify( {'status_code': r.status_code } )



#Edita contracs
@bp.route('/contracts/edit/<int:provider_id>', methods=['GET', 'POST', 'DELETE'])
def contractsEdit(provider_id):

    #Renderiza el template del formulario para agregar un proveedor
    if request.method == 'GET':
        
        url = URLFrp + 'contracts/' + str(provider_id)
        r = requests.get( url) 
        reqJ = r.json()
        
        if reqJ['id'] == None:
            displayExistRegister = "display:none;"
            titleDontExist = 'El registro no existe'
        else:
            displayExistRegister = ""
            titleDontExist = ''


        #Obtiene todos providers
        urlCountProviders = URLFrp + 'providers/count'
        countAmountProviders = requests.get( urlCountProviders ).json()['count']

        queryStrProviders = 'providers/?offset=0&limit=' + str(countAmountProviders)
        urlProviders = URLFrp + queryStrProviders

        rProviders = requests.get( urlProviders ) 
        providers = rProviders.json() 
        
        

        return render_template( 'contracts/edit.html', 
                                data = reqJ, 
                                catalog = 'contracts', 
                                menu = menuContract, 
                                providers = providers,
                                displayExistRegister = displayExistRegister,
                                titleDontExist = titleDontExist
                        )
    
    #Cuando termina de cargar la pagina el javascrip pide la lista de los proveedores
    elif request.method == 'POST':
        data = request.get_json()
        
        idRegister = data['id']

        dicData = { 
            'number'                     : data['number'                  ], 
            'title'                      : data['title'                    ], 
            'description'                : data['description'              ], 
            'provider'                   : data['provider'                 ], 
            'delivery_stage'             : data['delivery_stage'           ], 
            'initial_contracted_amount'  : data['initial_contracted_amount'], 
            'kickoff'                    : data['kickoff'                  ], 
            'ending'                     : data['ending'                   ], 
            'down_payment'               : data['down_payment'             ], 
            'down_payment_amount'        : data['down_payment_amount'      ], 
            'ext_agreement'              : data['ext_agreement'            ], 
            'ext_agreement_amount'       : data['ext_agreement_amount'     ], 
            'final_contracted_amount'    : data['final_contracted_amount'  ], 
            'total_amount_paid'          : data['total_amount_paid'        ], 
            'outstanding_down_payment'   : data['outstanding_down_payment' ], 
            'adjudication'               : data['adjudication'             ], 
            'funding'                    : data['funding'                  ], 
            'program'                    : data['program'                  ], 
            "inceptor_uuid"              : "string"
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'contracts/' + idRegister
        r = requests.put( url, data=dataJSON)

        return jsonify( {'status_code': r.status_code} )

    elif request.method == 'DELETE':
        url = URLFrp + 'contracts/' + str(provider_id)
        r = requests.delete( url )
        return jsonify( {'status_code': r.status_code } )



