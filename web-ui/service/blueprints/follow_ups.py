import os, json, requests
from flask import Flask, url_for, render_template, request, jsonify, Blueprint


from general import URLFrp, menuFollowUps

bp = Blueprint('follow_ups', __name__,
                        template_folder='templates')


#Paginacion
@bp.route('/follow_ups/projects', methods=['GET', 'POST'])
def followupsList():

    #Renderiza el template de la lista de proveedores
    if request.method == 'GET':
        
        return render_template( 'follow_ups/index.html', catalog='/follow_ups/projects', goToLinkRegister = '/follow_ups/project', menu = menuFollowUps, title='Avance de Obras' )
    
    else:
        data = request.get_json()
        
        
        paginationStart     = data['paginationStart']
        paginationStep      = data['paginationStep']
        paginationBy        = data['by']
        paginationOrder     = data['order']
        searchBy            = data['searchBy']
        valueSearchBy       = data['valueSearchBy']
        

        if searchBy == '':
            urlCount = URLFrp + 'projects/with_follow_up/count'
            searchQuery = '' 
        else:
            urlCount = URLFrp + 'projects/with_follow_up/count?' + searchBy + '=' + valueSearchBy
            searchQuery = '&'+ searchBy +'=' + valueSearchBy


        countAmount = requests.get( urlCount ).json()['count']
        queryStr = 'projects/with_follow_up?offset=' + str(paginationStart) + '&limit=' + str(paginationStep) + searchQuery 
        url = URLFrp + queryStr
        

        r = requests.get( url) 
        dataRes = r.json() 
        return jsonify( { 'data' : dataRes, 'count' : countAmount} )



@bp.route('/follow_ups/project/<int:project_id>', methods=['GET', 'POST'])
def followUpsProject(project_id):

    if request.method == 'GET':

        queryStr = 'projects/with_follow_up?project='+ str(project_id) 
        
        url = URLFrp + queryStr
        r = requests.get( url).json()
        
        return render_template( 'follow_ups/edit2.html', 
                                catalog='/follow_ups/project/'+str(project_id), 
                                menu = menuFollowUps, 
                                goToLinkRegister = '/follow_ups/edit',
                                goToAddRegister = '/follow_ups/add',
                                dataProject = r[0],
                                title='Avance de Obras' )
    
    else:
        data = request.get_json()
        
        paginationStart     = data['paginationStart']
        paginationStep      = data['paginationStep']
        paginationBy        = data['by']
        paginationOrder     = data['order']
        searchBy            = data['searchBy']
        valueSearchBy       = data['valueSearchBy']
        
        orderList = '&order='+str(paginationOrder)
        urlCount = URLFrp + 'follow_ups/count?project='+ str(project_id)


        countAmount = requests.get( urlCount ).json()['count']
        queryStr = 'follow_ups/?project='+ str(project_id) +'&offset=' + str(paginationStart) + '&limit=' + str(paginationStep) + orderList
        url = URLFrp + queryStr
        

        r = requests.get( url) 
        dataRes = r.json() 
        return jsonify( { 'data' : dataRes, 'count' : countAmount} )
        



#Edita 
@bp.route('/follow_ups/edit/<int:follow_up_id>', methods=['GET', 'POST', 'DELETE'])
def followUpsEdit(follow_up_id):

    #Renderiza el template del formulario para agregar un proveedor
    if request.method == 'GET':
        
        url = URLFrp + 'follow_ups/' + str(follow_up_id)
        r = requests.get( url) 
        reqJ = r.json()

        checkStages = 'catalogues/check_stages'
        urlCheckStages = URLFrp + checkStages

        rCheckStages = requests.get( urlCheckStages ).json()
        if reqJ['id'] != None:
            projectUrl = 'projects/with_follow_up?project='+ str(reqJ['project']) 
            urlProject = URLFrp + projectUrl
            projectTitle = requests.get( urlProject).json()[0]['project_title']
            displaNoneFields = ''
        else:
            displaNoneFields = 'display:none;'
            projectTitle = 'El registro no existe'
        
        return render_template( 'follow_ups/edit_follow_up.html', 
                                data = reqJ, 
                                catalog = '/follow_ups/edit/', 
                                menu = menuFollowUps, 
                                checkStages = rCheckStages,
                                projectTitle = projectTitle,
                                pathUrl = URLFrp + 'attachments/',
                                displaNoneFields = displaNoneFields
                                )
    

    elif request.method == 'POST':
        data = request.get_json()
        
        idRegister = data['id']

        dicData = { 
            'project'           : data['project'          ], 
            'verified_progress' : data['verified_progress'], 
            'financial_advance' : data['financial_advance'], 
            'img_paths'         : data['img_paths'        ], 
            'check_stage'       : data['check_stage'      ], 
            'check_date'        : data['check_date'       ], 
            'inceptor_uuid'     : data['inceptor_uuid'    ]
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'follow_ups/' + idRegister
        r = requests.put( url, data=dataJSON)

        return jsonify( {'status_code': r.status_code, 'follow_up_id': follow_up_id } )



    elif request.method == 'DELETE':
        url = URLFrp + 'follow_ups/' + str(follow_up_id)
        r = requests.delete( url )
        return jsonify( {'status_code': r.status_code } )



#Agrega 
@bp.route('/follow_ups/add/<int:project_id>', methods=['GET', 'POST'])
def followUpsAdd(project_id):

    #Renderiza el template del formulario para agregar un proveedor
    if request.method == 'GET':
        
        checkStages = 'catalogues/check_stages'
        urlCheckStages = URLFrp + checkStages
        rCheckStages = requests.get( urlCheckStages ).json()
        
        
        projectUrl = 'projects/with_follow_up?project='+ str(project_id) 
        urlProject = URLFrp + projectUrl
        projectTitle = requests.get( urlProject).json()[0]['project_title']
        
        return render_template( 'follow_ups/add.html', 
                                catalog = '/follow_ups/add/', 
                                menu = menuFollowUps, 
                                checkStages = rCheckStages,
                                projectTitle = projectTitle,
                                projectId = project_id
                                )
    

    elif request.method == 'POST':
        data = request.get_json()
        
        dicData = { 
            'project'           : data['project'          ], 
            'verified_progress' : data['verified_progress'], 
            'financial_advance' : data['financial_advance'], 
            'img_paths'         : data['img_paths'        ], 
            'check_stage'       : data['check_stage'      ], 
            'check_date'        : data['check_date'       ], 
            'inceptor_uuid'     : data['inceptor_uuid'    ]
        }

        dataJSON = json.dumps(dicData)

        url = URLFrp + 'follow_ups/'
        r = requests.post( url, data=dataJSON)

        rowJson = json.loads(r.content)
        
        return jsonify( {'status_code': r.status_code, 'follow_up_id': rowJson['id'] } )




@bp.route('/save_image_followups/<int:follow_ups_id>', methods=['POST'])
def saveImageFollowUps(follow_ups_id):

    url = URLFrp + 'follow_ups/'+ str(follow_ups_id) +'/attachment'
    
    r = requests.post(url, files=request.files)

    
    return jsonify( {'status_code': r.status_code} )




