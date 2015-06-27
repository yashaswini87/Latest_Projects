var countPieGui = angular.module('hackdayGui', ['ui.bootstrap']);


countPieGui.controller('mainController',function($scope, $http){
	
 var renderPie = function(data) {
	 
	  var chartConfig = {
		        chart: {
		            plotBackgroundColor: null,
		            plotBorderWidth: 1, //null,
		            plotShadow: false
		        },
		        title: {
		            text: 'Feature Importance by Reviews'
		        },
		        tooltip: {
		            pointFormat: '{series.name}: <b>{point.raw}</b>'
		        },
		        plotOptions: {
		            pie: {
		                allowPointSelect: true,
		                cursor: 'pointer',
		                dataLabels: {
		                    enabled: true,
		                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
		                    style: {
		                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
		                    }
		                }
		            }
		        },
		        series: [{
		            type: 'pie',
		            name: 'Feature Importance by Reviews',
		            data: null
		        }]
		 };
	  
	    chartConfig.series[0].data = data;
	 
	 
	    $('#container').highcharts(chartConfig);
	 
	 
 };
 

	$http.defaults.headers.common.Accept = "application/json";
	$http.defaults.headers.common["WM_SVC.VERSION"]="1.0";
	$http.defaults.headers.common["WM_SVC.ENV"]="STG";
	$http.defaults.headers.common["WM_QOS.CORRELATION_ID"]= "1234";
	$http.defaults.headers.common["WM_CONSUMER.ID"]= "100";
	$http.defaults.headers.common["WM_SVC.NAME"]= "item-validation-app";
   
   $http.get('http://172.28.90.252:8888/?productId=12345678').success(
           function(response) {

        	   console.log('Success: ' + JSON.stringify(response));  
        	   
        	   
        	   var data = response.data;
        	   
        	   console.log(data);
        	   
        	   renderPie(data);
                
           }).error(function(data) {
          
           	
           	console.log('Error: received from server ' + JSON.stringify(data));
        	alert('Error: received from server, rendering with mock data');
           	
            var data = [
                        ['Mock-Success', 98.0],
                        ['Mock-Failures', 2.0]
                    ];
            
              renderPie(data);
	});

}); 



