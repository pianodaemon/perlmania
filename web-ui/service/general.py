URLFrp = 'http://15.164.48.84/api/v1/' 

menuContract = [
    {'name':'Contratos',  'url':'/contracts ', 'nameSingular': 'Contrato'  },
    {'name':'Contratistas','url':'/providers ', 'idHTML':'menuComponentProviders', 'iconClass':'fas fa-ethernet'     , 'isActive':''                },
    {'name':'Contratos',  'url':'/contracts ', 'idHTML':'menuComponentContracts', 'iconClass':'fas fa-file-contract', 'isActive':'active'          },
    {'name':'Obras',      'url':'/projects ' , 'idHTML':'menuComponentProjects' , 'iconClass':'fas fa-hard-hat'     , 'isActive':''                },
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'idHTML':'menuComponentFollowUp' , 'iconClass':'fas fa-business-time', 'isActive':''           },
    {'name':'Tableros',   'url':'/graphics', 'idHTML':'menuComponentGraphics' , 'iconClass':'fas fa-chart-pie'    , 'isActive':''                },
]


menuProvider = [
    {'name':'Contratistas','url':'/providers'  , 'nameSingular': 'Contratista' },
    {'name':'Contratistas','url':'/providers'  , 'idHTML':'menuComponentProviders', 'iconClass':'fas fa-ethernet'     , 'isActive':'active'          },
    {'name':'Contratos',  'url':'/contracts'  , 'idHTML':'menuComponentContracts', 'iconClass':'fas fa-file-contract', 'isActive':''                },
    {'name':'Obras',      'url':'/projects'   , 'idHTML':'menuComponentProjects' , 'iconClass':'fas fa-hard-hat'     , 'isActive':''                },
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'idHTML':'menuComponentFollowUp' , 'iconClass':'fas fa-business-time', 'isActive':''           },
    {'name':'Tableros',   'url':'/graphics'  , 'idHTML':'menuComponentGraphics' , 'iconClass':'fas fa-chart-pie'    , 'isActive':''                },
]


menuProject = [
    {'name':'Obras',          'url':'/projects' ,'nameSingular': 'Obra'  },
    {'name':'Contratistas',   'url':'/providers', 'idHTML':'menuComponentProviders', 'iconClass':'fas fa-ethernet'     , 'isActive':''           },
    {'name':'Contratos',      'url':'/contracts', 'idHTML':'menuComponentContracts', 'iconClass':'fas fa-file-contract', 'isActive':''           },
    {'name':'Obras',          'url':'/projects' , 'idHTML':'menuComponentProjects' , 'iconClass':'fas fa-hard-hat'     , 'isActive':'active'     },
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'idHTML':'menuComponentFollowUp' , 'iconClass':'fas fa-business-time', 'isActive':''           },
    {'name':'Tableros',       'url':'/graphics', 'idHTML':'menuComponentGraphics' , 'iconClass':'fas fa-chart-pie'    , 'isActive':''           },
]


menuFollowUps = [
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'nameSingular': 'Registro'  },
    {'name':'Contratistas',   'url':'/providers', 'idHTML':'menuComponentProviders', 'iconClass':'fas fa-ethernet'     , 'isActive':''           },
    {'name':'Contratos',      'url':'/contracts', 'idHTML':'menuComponentContracts', 'iconClass':'fas fa-file-contract', 'isActive':''           },
    {'name':'Obras',          'url':'/projects' , 'idHTML':'menuComponentProjects' , 'iconClass':'fas fa-hard-hat'     , 'isActive':''           },
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'idHTML':'menuComponentFollowUp' , 'iconClass':'fas fa-business-time', 'isActive':'active'     },
    {'name':'Tableros',       'url':'/graphics', 'idHTML':'menuComponentGraphics' , 'iconClass':'fas fa-chart-pie'    , 'isActive':''           },
]

menuGraphics = [
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'nameSingular': 'Registro'  },
    {'name':'Contratistas',   'url':'/providers', 'idHTML':'menuComponentProviders', 'iconClass':'fas fa-ethernet'     , 'isActive':''           },
    {'name':'Contratos',      'url':'/contracts', 'idHTML':'menuComponentContracts', 'iconClass':'fas fa-file-contract', 'isActive':''           },
    {'name':'Obras',          'url':'/projects' , 'idHTML':'menuComponentProjects' , 'iconClass':'fas fa-hard-hat'     , 'isActive':''           },
    {'name':'Avance de Obras','url':'/follow_ups/projects', 'idHTML':'menuComponentFollowUp' , 'iconClass':'fas fa-business-time', 'isActive':''     },
    {'name':'Tableros',       'url':'/graphics', 'idHTML':'menuComponentGraphics' , 'iconClass':'fas fa-chart-pie'    , 'isActive':'active'           },
]


#No se usan
checkStageClassColors = ['checkStage1','checkStage1','checkStage2','checkStage3','checkStage4','checkStage5','checkStage6','checkStage7']
