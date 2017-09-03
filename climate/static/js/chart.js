Chart.pluginService.register({
    beforeDraw: function (chart, easing) {
        if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
            var helpers = Chart.helpers;
            var ctx = chart.chart.ctx;
            var chartArea = chart.chartArea;

            ctx.save();
            ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
            ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
            ctx.restore();
        }
    }
});

function LineChart(canvas, data, labels) {
	this.canvas = canvas;
	this.data = data;
    this.labels = labels
}

LineChart.prototype.draw = function() {
	var ctx = document.getElementById(this.canvas).getContext('2d');
	Chart.defaults.global.defaultFontSize = 18;
	Chart.defaults.global.defaultFontStyle = 'bold'
	Chart.defaults.global.defaultFontFamily = "Quicksand";
    var xLabels = [];
    for (var i = 0; i < this.data[0].length; i++) {
        xLabels.push("");
    }

    var colors = [
        '#F27991',
        '#8888AA',
        '#557755',
        '#338811',
        '#7F3F4C',
        '#992233',
        '#3D404C',
        '#881133',
        '#112288',
        '#111010',
        '#001166',
        '#220000',
        '#F2DADE',
        '#BBDDAA',
        '#99ADFF',
    ];

    var datasetOpts = [];
    for (var i = 0; i < this.data.length; i++) {
        datasetOpts.push({
            label: this.labels[i],
            data: this.data[i],
            borderColor: colors[i],
            backgroundColor: colors[i],
            borderWidth: 3,
            pointHoverBorderColor: colors[i],
            pointHoverBackgroundColor: colors[i]
        });
    }

	var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: xLabels,
        datasets: datasetOpts
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        },
        legend: {
        	labels: {

        	}
        },
        tooltips: {
        	mode: 'index',
        	borderWidth: 1
        },
        chartArea: {
        	backgroundColor: 'rgba(0, 0, 0, 0.6)'
    	},
    	maintainAspectRatio: false
    }
});
}

function StackedBarChart(canvas, data, labels) {
	this.canvas = canvas;
	this.data = data;
    this.labels = labels;
}

StackedBarChart.prototype.draw = function() {
	var ctx = document.getElementById(this.canvas).getContext('2d');
	Chart.defaults.global.defaultFontSize = 18;
	Chart.defaults.global.defaultFontStyle = 'bold'
	Chart.defaults.global.defaultFontFamily = "Quicksand";

    var xLabels = [];
    for (var i = 0; i < this.data[0].length; i++) {
        xLabels.push("");
    }

    var colors = [
        '#F27991',
        '#8888AA',
        '#557755',
        '#338811',
        '#7F3F4C',
        '#992233',
        '#3D404C',
        '#881133',
        '#112288',
        '#111010',
        '#001166',
        '#220000',
        '#F2DADE',
        '#BBDDAA',
        '#99ADFF',
    ];

    var datasetOpts = [];
    for (var i = 0; i < this.data.length; i++) {
        datasetOpts.push({
            label: this.labels[i],
            data: this.data[i],
            borderColor: 'rgba(255,255,255,1)',
            backgroundColor: colors[i],
            borderWidth: 0
        });
    }

	var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: xLabels,
        datasets: datasetOpts
    },
    options: {
        spanGaps: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                },
                stacked: true
            }],
            xAxes: [{
                stacked: true
            }]
        },
        legend: {
        	labels: {

        	}
        },
        tooltips: {
        	mode: 'index',
        	borderWidth: 1
        },
        chartArea: {
        	backgroundColor: 'rgba(0, 0, 0, 0.6)'
    	},
    	maintainAspectRatio: false,
    	barPercentage: 0.9
    }
});
}
