var countPieGui = angular.module('hackdayGui', ['ui.bootstrap']);


countPieGui.controller('mainController',function($scope, $http){


 var renderBarChart = function(categories, seriesData){

	var chartConfig = {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'What people say'
        },
        subtitle: {
            text: 'Source: <a href="http://www.walmart.com/ip/4408441">Product Link</a>'
        },
        xAxis: {
            categories: null,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Feature Sentiment',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' millions'
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 80,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: null 
    }; 

   chartConfig.xAxis.categories = categories;
   chartConfig.series = seriesData;
   $('#container2').highcharts(chartConfig);	

 };
	
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
		        credits: {
                    enabled: false
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

	
	$scope.productSearch = function(){
		
	alert("hi "+$scope.productIdStr);
	remoteCall($scope.productIdStr);	
	};	
 
	var remoteCall = function(productId){

   $http.get('http://172.28.90.252:8888/?productId='+productId).success(
           function(response) {

                   console.log('Success: ' + JSON.stringify(response));


                   var data = response.data;

                   console.log(data);

                   renderPie(data);
		   renderBarChart(response.col_cats,response.col_data);

           }).error(function(data) {


                console.log('Error: received from server ' + JSON.stringify(data));
                alert('Error: received from server, rendering with mock data');

            var data = [
                        ['Mock-Success', 98.0],
                        ['Mock-Failures', 2.0]
                    ];

              renderPie(data);
        });

	};


   

}); 



