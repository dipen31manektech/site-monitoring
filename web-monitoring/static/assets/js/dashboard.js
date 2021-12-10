const primary = '#6993FF';
const success = '#1BC5BD';
const info = '#8950FC';
const warning = '#FFA800';
const danger = '#F64E60';

$('#selected_domain').on('change', function(ev) {
    $.ajax({
      url: 'http://127.0.0.1:8000/monitor/dashboard/performance',
      data: {'data': this.selectedOptions[0].value},
      type:"post",
      dataType:"json",
      headers: {  'Access-Control-Allow-Origin': '*' },
      success: function (data) {
      	console.log(data)
        $.each( data.global_datas, function( key, value ) {
        $('#title_' + key).text(value.title);
        $('#data_' + key).text(value.numericValue +" "+value.numericUnit);
        $('#description_' + key).text(value.description);
        });
      },
   });
});
function chart() {
		const apexChart = "#chart_3";
        $.ajax({
            type: "get",
            url: "http://127.0.0.1:8000/monitor/dashboard/chart",
            dataType: "json",
             headers: {  'Access-Control-Allow-Origin': '*' },
            success: function(data){

               var options = {
			series: [{
				name: 'Down Time',
				data: data['downTimeList']!== undefined ? data['downTimeList'] : [0]
			}, {
				name: 'Total Time',
				data: data['totalTimeList']!== undefined ? data['totalTimeList'] : [0]
			}, {
				name: 'Up Time',
				data: data['upTimeList']!== undefined ? data['upTimeList'] : [0]
			}],
			chart: {
				type: 'bar',
				height: 350
			},
			plotOptions: {
				bar: {
					horizontal: false,
					columnWidth: '55%',
					endingShape: 'rounded'
				},
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				show: true,
				width: 2,
				colors: ['transparent']
			},
			xaxis: {
				categories: data['exceptionData']!== undefined ? data['exceptionData'] : [0],
			},
			yaxis: {
				title: {
					text: 'Time (minutes)'
				}
			},
			fill: {
				opacity: 1
			},
			tooltip: {
				y: {
					formatter: function (val) {
						return val + " minutes"
					}
				}
			},
			colors: [primary, success, warning]
		};
		    var chart = new ApexCharts(document.querySelector(apexChart), options);
		    chart.render();
		    if (data['totalUpTime'] !== undefined)
		        $('#totalUpTime').text(data['totalUpTime']);
		    else
		        $('#totalUpTime').text(0);
		    if (data['totalDownTime'] !== undefined)
		        $('#totalDownTime').text(data['totalDownTime']);
		    else
		        $('#totalDownTime').text(0);
            },
            error: function(e){
                alert(e);
            }
        });
	}
	chart();