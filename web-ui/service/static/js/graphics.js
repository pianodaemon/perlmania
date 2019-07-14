
var plotsChart = {
    department    : '',
    check_stage   : '',
    city          : '',
    startDate     : '',
    endDate       : '',
    provider      : '',
    funding       : '',
    program       : '',
    adjudication  : '',
    chartType     : '',
    allowGetData  : true,
    functionClick : function(){;},
    chartTitle    : {
        obras: 0,
        amount: 0,
        titleGral : '',
        setTitle: function(){
            var amount = this.amount.toFixed(2).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
            var city = this.titleGral;
            $('#titleChartGral').html(city);
            return 'TOTAL DE OBRAS ' + this.obras + '<br>$' + amount; 
        }
    },
    initStatusPie : function(){
        if( !plotsChart.allowGetData ){ return; }
        plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

        plotsChart.chartType = 'pieStatus';
        plotsChart.functionClick = function(){console.log("callback");};
        plotsChart.getData();
        $('.linkPlots').removeAttr("active");$('#plotTotal1').attr('active','');
    },
    initStackCities : function(){
        if( !plotsChart.allowGetData ){ return; }
        plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

        plotsChart.chartType = 'barCities';
        plotsChart.functionClick = plotsChart.chartAfterCitiesBar.init;
        plotsChart.getData(  );

        $('.linkPlots').removeAttr("active");$('#plotTotal2').attr('active','');
    },
    initDepartmentsPie : function(){
        if( !plotsChart.allowGetData ){ return; }
        plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

        plotsChart.chartType = 'pieDepartment';
        plotsChart.functionClick = plotsChart.chartAfterDepartmentsPie.init;
        plotsChart.getData(  );

        $('.linkPlots').removeAttr("active");$('#plotTotal3').attr('active','');
    },
    chartAfterCitiesBar: {
        init: function( cityIdDB ){
            plotsChart.city = cityIdDB;
            plotsChart.chartTitle.titleGral = citiesNL[cityIdDB];
            plotsChart.chartAfterCitiesBar.statusPie();
            
            var strOptions = `
                <span class="linkPlots" id="plotTotal1" active onclick="plotsChart.chartAfterCitiesBar.statusPie();">
                    <i class="fas fa-chart-line" style="margin-right:10px;"></i> Estatus
                </span>
                <span class="linkPlots" id="plotTotal2" onclick="plotsChart.chartAfterCitiesBar.pieDepartment();">
                    <i class="fas fa-building" style="margin-right:10px;"></i> Dependencias
                </span>
                <span class="linkPlots" id="plotTotal3" onclick="plotsChart.chartAfterCitiesBar.providerBarWithOutZeros();">
                    <i class="fas fa-user-tie" style="margin-right:10px;"></i> Contratistas
                </span>
            `;
            
            $('#radioSelects').html(strOptions);
        },
        statusPie : function(){
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'pieStatus';
            plotsChart.functionClick = function(s){plotsChart.check_stage = s; plotsChart.openUrl();};
            plotsChart.getData(  );
            $('.linkPlots').removeAttr("active");$('#plotTotal1').attr('active','');
        },
        pieDepartment : function(){
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'pieDepartment';
            plotsChart.functionClick = function(s){plotsChart.department = s; plotsChart.openUrl();};
            plotsChart.getData(  );
            $('.linkPlots').removeAttr("active");$('#plotTotal2').attr('active','');
        },
        providerBarWithOutZeros : function(){
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'providerBarWithOutZeros';
            plotsChart.functionClick = function(s){plotsChart.provider = s; plotsChart.openUrl();};
            plotsChart.getData(  );
            $('.linkPlots').removeAttr("active");$('#plotTotal3').attr('active','');
        }
    },
    chartAfterDepartmentsPie: {
        init: function( departmentIdDB ){
            plotsChart.department = departmentIdDB;
            plotsChart.chartTitle.titleGral = departmentsObras[departmentIdDB];
            plotsChart.chartAfterDepartmentsPie.statusPie();
            var strOptions = `
                <span class="linkPlots" id="plotTotal1" active onclick="plotsChart.chartAfterDepartmentsPie.statusPie();">
                    <i class="fas fa-chart-line" style="margin-right:10px;"></i> Estatus
                </span>
                <span class="linkPlots" id="plotTotal2" onclick="plotsChart.chartAfterDepartmentsPie.stackCities();">
                    <i class="fas fa-map" style="margin-right:10px;"></i> Municipios
                </span>
                <span class="linkPlots" id="plotTotal3" onclick="plotsChart.chartAfterDepartmentsPie.providerBarWithOutZeros();">
                    <i class="fas fa-user-tie" style="margin-right:10px;"></i> Contratistas
                </span>
            `;
            
            $('#radioSelects').html(strOptions);
        },
        statusPie : function(){
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'pieStatus';
            plotsChart.functionClick = function(s){plotsChart.check_stage = s; plotsChart.openUrl();};
            plotsChart.getData( );
            $('.linkPlots').removeAttr("active");$('#plotTotal1').attr('active','');
        },
        stackCities : function(){ 
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'barCities';
            plotsChart.functionClick = function(s){plotsChart.city = s; plotsChart.openUrl();} ;
            plotsChart.getData( );
            $('.linkPlots').removeAttr("active");$('#plotTotal2').attr('active','');
        },
        providerBarWithOutZeros : function(){
            if( !plotsChart.allowGetData ){ return; }
            plotsChart.allowGetData = false; $('.linkPlots').css('cursor','wait');

            plotsChart.chartType = 'providerBarWithOutZeros';
            plotsChart.functionClick = function(s){plotsChart.provider = s; plotsChart.openUrl();} ;
            plotsChart.getData( );
            $('.linkPlots').removeAttr("active");$('#plotTotal3').attr('active','');
        }
    },
    openUrl: function(){
        var urlLink = $('#urlLink').val();

        var department  = plotsChart.department;
        var statusIdNum = plotsChart.check_stage;
        var city        = plotsChart.city ;

        var queryString = '?department=' + department;
        queryString += '&status=' + statusIdNum;
        queryString += '&city=' + city;

        queryString += '&startDate='    + plotsChart.startDate;
        queryString += '&endDate='      + plotsChart.endDate;
        queryString += '&provider='     + plotsChart.provider;
        queryString += '&funding='      + plotsChart.funding;
        queryString += '&program='      + plotsChart.program;
        queryString += '&adjudication=' + plotsChart.adjudication;
        var url = urlLink + queryString ;
        window.open( url ,"_self");
    },
    chart : '',
    data  : undefined,
    getData : function ( ){
        
        document.getElementById('waintingAnimation').style.display = "block";

        $.ajax({
            url: '/graphics',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function (res) {
                
                plotsChart.data = res.data;
                if( plotsChart.chartType == 'pieStatus' ){
                    var values = plotsChart.setJsonChart(res.data);
                    var options = plotsChart.optionsChart(values)
                    $('#genl-pie-chart').css('height','400px');
                    plotsChart.chart = Highcharts.chart('genl-pie-chart', options);
                }else if( plotsChart.chartType == 'barCities' ){
                    var values = plotsChart.setJsonStackedBar(res.data);
                    var optionsHighChart = plotsChart.optionsStackedBar(values[0], values[1], values[2]);
                    $('#genl-pie-chart').css('height','2000px');
                    plotsChart.chart = Highcharts.chart('genl-pie-chart', optionsHighChart);
                    plotsChart.chart.render();  //Renderiza para mostrar los labels que se generan despues de crearse la grafica
                }else if( plotsChart.chartType == 'pieDepartment' ){
                    var values = plotsChart.setJsonDepartmentPie(res.data);
                    var optionsHighChart = plotsChart.optionsChart(values);
                    $('#genl-pie-chart').css('height','400px');
                    plotsChart.chart = Highcharts.chart('genl-pie-chart', optionsHighChart);
                }else if( plotsChart.chartType == 'providerBarWithOutZeros' ){
                    var values = plotsChart.setJsonStackedBarWhitOutZeros(res.data);
                    var optionsHighChart = plotsChart.optionsSimpleBar(values[0], values[1] );
                    var heightChart = values[0].length*40 + 150;
                    $('#genl-pie-chart').css('height', heightChart + 'px');
                    plotsChart.chart = Highcharts.chart('genl-pie-chart', optionsHighChart);
                }
                
                plotsChart.allowGetData = true; $('.linkPlots').css('cursor','pointer'); $('#waintingAnimation').css('display','none');

            },

            data:  JSON.stringify ({'department'    : plotsChart.department.toString(),
                                    'city'          : plotsChart.city.toString(),
                                    'check_stage'   : plotsChart.check_stage.toString(),
                                    'startDate'     : plotsChart.startDate.toString(),
                                    'endDate'       : plotsChart.endDate.toString(),
                                    'provider'      : plotsChart.provider.toString(),
                                    'adjudication'  : plotsChart.adjudication.toString(),
                                    'funding'       : plotsChart.funding.toString(),
                                    'program'       : plotsChart.program.toString(),
                                   })

        }).done(function() { plotsChart.allowGetData = true; $('.linkPlots').css('cursor','pointer'); $('#waintingAnimation').css('display','none');
        }).fail(function() { plotsChart.allowGetData = true; $('.linkPlots').css('cursor','pointer'); $('#waintingAnimation').css('display','none');
        }).always(function() { plotsChart.allowGetData = true; $('.linkPlots').css('cursor','pointer'); $('#waintingAnimation').css('display','none');
        });

    },
    setJsonChart : function( resp ){
        var countStages = ['',0,0,0,0,0,0,0];
        var countStagesAmount = [0,0,0,0,0,0,0,0];  
        var values = [];

        var namesStages = [ '',
            "TERMINADAS",
            "EN TIEMPO",
            "CON RETRASO",
            "RESCINDIDAS",
            "NO INICIADAS",
            "CON AVANCE FINANCIERO MAYOR AL FÍSICO",
            "OBRAS RESTRINGIDAS"
        ]


        for(var i in resp){
            var stat = resp[i];
            countStages[stat.check_stage]++;
            countStagesAmount[ stat.check_stage ] += stat.final_contracted_amount;
        }


        var finalContractedAmountTotal =  countStagesAmount.reduce(function(total, sum){return total + sum;}) ;

        for( var s = 1; s<=7; s++ ){
            if( countStages[s] > 0 ){    
                values.push( {
                    name : namesStages[s],   
                    y: countStages[s],
                    x: s,
                    amount: countStagesAmount[s],
                    color: colorStatus[ s ]
                } )
            }
        }
        
        
        this.chartTitle.obras = resp.length;
        this.chartTitle.amount = finalContractedAmountTotal;
        
        return values;
    },
    setJsonStackedBar: function( jsonResponse ){
        
        //[Estatus][Ciudad]  
        var countCities = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ];
        
        var countCitiesAmount = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ];

        var countCitiesAmountByCity = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] ;  

        var categories        = citiesNL.slice(1);

        //Por cada obra aumenta en 1 el elemento countCities[estatus][ciudad]
        for(var i in jsonResponse){
            var obra = jsonResponse[i];
            countCities[obra.check_stage - 1][obra.city_id - 1]++;
            countCitiesAmount[obra.check_stage - 1][obra.city_id - 1] += obra.final_contracted_amount;
            countCitiesAmountByCity[obra.city_id - 1] += obra.final_contracted_amount;
        }

        var finalContractedAmountTotal =  countCitiesAmountByCity.reduce(function(total, sum){return total + sum;}) ;

        
        var dataForStatus = [[],[],[],[],[],[],[]];
        for( var ciudad in countCities[0] ){

            dataForStatus[0].push({
                y: countCities[0][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[0][ciudad]
            })
            dataForStatus[1].push({
                y: countCities[1][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[1][ciudad]
            })
            dataForStatus[2].push({
                y: countCities[2][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[2][ciudad]
            })
            dataForStatus[3].push({
                y: countCities[3][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[3][ciudad]
            })
            dataForStatus[4].push({
                y: countCities[4][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[4][ciudad]
            })
            dataForStatus[5].push({
                y: countCities[5][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[5][ciudad]
            })
            dataForStatus[6].push({
                y: countCities[6][ciudad],
                city: parseInt(ciudad)+1,
                amount: countCitiesAmount[6][ciudad]
            })

        }
        

        var data = [
            {
                name: 'OBRAS RESTRINGIDAS',
                data: dataForStatus[6],
                color: colorStatus[ 7 ]
            },{
                name: 'CON AVANCE FINANCIERO MAYOR AL FÍSICO',
                data: dataForStatus[5],
                color: colorStatus[ 6 ]
            },{
                name: 'NO INICIADAS',
                data: dataForStatus[4],
                color: colorStatus[ 5 ]
            },{
                name: 'RESCINDIDAS',
                data: dataForStatus[3],
                color: colorStatus[ 4 ]
            },{
                name: 'CON RETRASO',
                data: dataForStatus[2],
                color: colorStatus[ 3 ]
            },{
                name: 'EN TIEMPO',
                data: dataForStatus[1],
                color: colorStatus[ 2 ]
            },{
                name: 'TERMINADAS',
                data: dataForStatus[0],
                color: colorStatus[ 1 ]
            }
        ];
        
        this.chartTitle.obras = jsonResponse.length;
        this.chartTitle.amount = finalContractedAmountTotal;

        return [data, categories, countCitiesAmountByCity];
    },
    setJsonDepartmentPie: function(resp){
        
        var countDepartments = ['',0,0,0,0,0,0,0,0,0,0,0,0,0];
        var countDepartmentsAmount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0];
  
        var values = [];

        var namesDepartments = [ '',
            'INFRAESTRUCTURA',
            'ICIFED',
            'REA',
            'SADM',
            'SSNL',
            'CODETUR',
            'CODEFRONT',
            'DIF',
            'FIDEPROES',
            'FUNDIDORA',
            'CONALEP',
            'CAMINOS',
            'ISSSTELEON'
        ]

        var finalContractedAmountTotal = 0;
        
        //Cuenta o aumenta el elemento que representa al departamento 
        for(var i in resp){
            var stat = resp[i];
            countDepartments[stat.department_id]++;
            countDepartmentsAmount[ stat.department_id ] += stat.final_contracted_amount;
        }

        var finalContractedAmountTotal =  countDepartmentsAmount.reduce(function(total, sum){return total + sum;}) ;

        for( var s = 1; s<=13; s++ ){
            if( countDepartments[s] > 0 ){    
                values.push( {
                    name : namesDepartments[s],   
                    y: countDepartments[s],
                    x: s,
                    amount: countDepartmentsAmount[s],
                    //color: colorStatus[ s ]
                } )
            }
        }
        

        this.chartTitle.obras = resp.length;
        this.chartTitle.amount = finalContractedAmountTotal;
        
        return values;
    },
    setJsonStackedBarWhitOutZeros: function( jsonResponse ){
        
        var providersObj = [];

        //Por cada obra aumenta en 1 el elemento countCities[estatus][ciudad]
        for(var i in jsonResponse){
            var obra = jsonResponse[i];
            if( providersObj['provider_' + obra.provider_id] ){
                 providersObj['provider_' + obra.provider_id].y += 1;
                 providersObj['provider_' + obra.provider_id].amount += obra.final_contracted_amount;
            }else{
                providersObj['provider_' + obra.provider_id] = {
                    y      : 1,
                    id     : obra.provider_id,
                    name   : obra.provider,
                    color  : '#939',
                    amount : obra.final_contracted_amount
                };
            }
            //countCitiesAmount[obra.city_id - 1] += obra.final_contracted_amount;
        }

        
        //var categories = [];
        var data = [];
        var finalContractedAmountTotal = 0;
        for( var p in providersObj ){
            //categories.push(providersObj[p].name);
            data.push(providersObj[p]);
            finalContractedAmountTotal += providersObj[p].amount;
        }
        
 

        plotsChart.chartTitle.obras = jsonResponse.length;
        plotsChart.chartTitle.amount = finalContractedAmountTotal;

        return[ data, jsonResponse.length ];
    },
    optionsChart : function(data){

        var widthWindow = jQuery(window).width()

        if(widthWindow < 600){
            var chartDataLabel = false;                
            var chartShowInLegend = true;
        }else{
            var chartDataLabel = true;
            var chartShowInLegend = true;
        }
        
        var titleTextPev = 'TOTAL DE OBRAS ';

        var options = {
   	        chart: {
   	    	    type: 'pie',
                options3d: {
                    enabled: true,
                    alpha: 45,
                    beta: 0
                },
                events: {
                    render: function () {    //Cuando se ocultan una rebanada o barra se actualizan las cantidades del titulo
                        try{
                            if( plotsChart.chart ){
                                var allStatus = plotsChart.chart.series[0].data;
                                var countAmount = 0;
                                for( var s in allStatus ){
                                    if( allStatus[s].visible ){
                                        countAmount += allStatus[s].amount;
                                    }
                                }
                                var totalProjectsVisible = plotsChart.chart.series[0].total;
                                plotsChart.chartTitle.obras  = totalProjectsVisible;
                                plotsChart.chartTitle.amount = countAmount;
                                plotsChart.chart.setTitle({ text: plotsChart.chartTitle.setTitle() } )
                            }
                        }
                        catch(e){
                            ;
                        }
                    }
                }
   	    	},
   	    	title: {
   	            text: plotsChart.chartTitle.setTitle(),
                useHTML: true
   	    	},
   	    	tooltip: {
   	            pointFormat: '<b>{point.percentage:.1f} %</b>'
   	    	},
   	    	plotOptions: {
   	    	    pie: {
   	    		    allowPointSelect: true,
   	    		    cursor: 'pointer',
                    depth: 35,
                    showInLegend: chartShowInLegend,
   	                point: {
   	                    events: {
   	                        click: function () {
                                plotsChart.functionClick( this.x );
   	                        }/*,
                            legendItemClick: function(){
                                console.log(this.series.total);                                
                            }*/
   	                    }
   	                },									    
   	    		    dataLabels: {
   	    		        enabled: chartDataLabel,
   	    		        color: '#000000',
   	    		        connectorColor: '#000000',
   	    		        //format: 
                        formatter: function(){
                            var point = this.point;
                            var amount = this.point.amount;
                            
                            var sfcat = amount.toFixed(2).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");

                            return '<b>' + point.y + ' ' + point.name + ' <span style="color:#446;">$' + sfcat + '</span>';
                        }
   	                }
   	    	    }
   	        },
            legend: {
                useHTML: true,
                labelFormatter: function () {
                    var a = this.percentage
                    var styleText = ' style="font-family: \'Poppins\', sans-serif; font-weight: 400; margin: 2px 2px;"  '
                    var styleTextS = ' style="font-family: \'Poppins\', sans-serif; font-weight: 400; margin: 2px 0px; font-weight:600;"  '
                    var styleTextN = ' style="font-family: \'Poppins\', sans-serif; font-weight: 400; margin: 2px 2px; font-weight:bold;"  '
                    var nameO = '<span '+ styleTextS +'>' + this.name + '</span>  '
                    var yValue = this.y === null ? 0 : this.y;
                    var pYO = '<span '+ styleTextN +'>' + yValue + '</span> '

                    var decimals = 0;
                    if( (this.percentage*100)%100 == 0 ){ decimals=0; }else if( (this.percentage*10)%10 == 1 ){ decimals=1; }else{decimals=2}

                    var percentO = '<span '+ styleText +'>' + this.percentage.toFixed(decimals) + '%</span>  '

                    if( yValue === 0 ){
                        this.options.color = "#777"
                        this.legendGroup.element.style.display = "none"
                        return null;
                    }
                    
                    var re = this.y === null ? null : percentO + nameO + ': ' + pYO ;
                    return re;
                }
            },
            credits: {
                enabled: false
            },		
   	    	series: [{
   	    	    data: data
   	    	}]
   	    };
        
        return options;
    },
    optionsStackedBar: function(data, categories, amountsByCity ) {

        var options = {
            chart: {
                type: 'bar',
                events: {
                    render: function () {    //Cuando se ocultan una rebanada o barra se actualizan las cantidades del titulo
                        try{
                            if( plotsChart.chart ){
                                var series = this.series;
                                
                                var countAmount = 0;
                                var countObras  = 0;
                                
                                for( var s in series ){
                                    var serie = series[s];
                                    if( serie.visible ){
                                        var cities = serie.data;
                                        for( var c in cities ){
                                            countAmount += cities[c].amount;
                                            countObras += cities[c].y;
                                        }
                                    }
                                }
                                
                                var totalProjectsVisible = countObras;
                                plotsChart.chartTitle.obras  = totalProjectsVisible;
                                plotsChart.chartTitle.amount = countAmount;
                                plotsChart.chart.setTitle({ text: plotsChart.chartTitle.setTitle() } )
                            }
                        }
                        catch(e){
                            ;
                        }
                    }
                }
            },
            title: {
                text: plotsChart.chartTitle.setTitle()
            },
            xAxis: {
                categories: categories,
                labels: {
                    step: 1
                }
            },
            yAxis: {
                stackLabels: {
                    enabled: true,
                    align: 'right',
                    style: {
                        color: '#226',
                        fontWeight: 'bold'
                    },
                    x: 5,
                    y: 10,
                    verticalAlign: 'top',
                    amountsByCity : amountsByCity,
                    formatter: function () {
                        var series = this.axis.series; //status
                        var thisCity = this.x;
                        var sumAmountThisCity = 0;
                        for( var s in series ){ //Son 7
                            if(series[s].data.length){
                                if(series[s].visible){
                                    sumAmountThisCity += series[s].data[thisCity].amount;
                                }
                            }
                        }
                        if(sumAmountThisCity == 0){return '';}
                        var amount = sumAmountThisCity.toFixed(2).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
                        return '<span style="color:#000;font-weight:100;">'+this.total + ' Obras </span><br><span style="color:#336;margin-left:13px;font-weight:100;"> $'+ amount +'</span>';
                    }
                }
            },
            legend: {
                reversed: true
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                },
                bar: {
                    groupPadding:0,
                    //pointWidth:10
                    point: {
   	                    events: {
   	                        click: function () {
                                plotsChart.functionClick( this.x + 1 );
   	                        }
   	                    }
   	                }
                }
            },
            series: data
        }
        
        return options;
    },
    optionsSimpleBar: function(data, jsonLength) {

        var options = {
            chart: {
                type: 'bar'
            },
            title: {
                text: plotsChart.chartTitle.setTitle()
            },
            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true,
                        inside: false,
                        formatter: function(){
                            var aamount = this.point.amount.toFixed(2).toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
                            return this.y + ' Obras <span >$' + aamount + '</span>';
                        }
                    }
                },
                bar: {
                    point: {
   	                    events: {
   	                        click: function () {
                                plotsChart.functionClick( this.id );
   	                        }
   	                    }
   	                }
                }
            },
            xAxis: {
                type: 'category'
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Obras',
                showInLegend: false,
                data: data
            }]
        }
        
        return options;
    },
    search: function(){
        this.department   = $('#departmentSearch').val();
        this.check_stage  = $('#check_stage').val();
        this.city         = $('#city').val();
        this.startDate    = $('#startDate').val();
        this.endDate      = $('#endDate').val();
        this.provider     = $('#provider').val();
        this.funding      = $('#funding').val();
        this.program      = $('#program').val();
        this.adjudication = $('#adjudication').val();

        $('#modalSearch').modal('hide');

        plotsChart.getData();

    }
}


