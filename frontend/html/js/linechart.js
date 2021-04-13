function lineChart(){
	var dom = document.getElementById("otherChartContainer");
	var myChart = echarts.init(dom);
	var app ={};
	var option;
	option = {
	title: {
		text:'指數圖',
		left:0
	},
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross'
        }
    },
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line'
    }]
	};

if(option && typeof option === 'object'){
    myChart.setOption(option);
}
}