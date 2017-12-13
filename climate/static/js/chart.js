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
    console.log(this.canvas);
    console.log(document.getElementById(this.canvas));
	var ctx = document.getElementById(this.canvas).getContext('2d');
    var xLabels = [];
    for (var i = 0; i < this.data[0].length; i++) {
        xLabels.push("");
    }

    var colors = [
        '#34495e',
        '#9b59b6',
        '#3498db',
        '#1abc9c',
        '#f1c40f',
        '#f39c12',
        '#d35400',
        '#e74c3c',
        '#c0392b',
    ];

    var datasetOpts = [];
    for (var i = 0; i < this.data.length; i++) {
        datasetOpts.push({
            label: this.labels[i],
            data: this.data[i],
            borderColor: colors[i],
            borderWidth: 3,
            pointHoverBorderColor: colors[i],
            pointHoverBackgroundColor: colors[i],
            pointSize: 6
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
        	backgroundColor: 'rgba(0, 0, 0, 0)'
    	},
    	maintainAspectRatio: false,
        layout: {
        padding: {
            right: 10
        }
    }
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

    var xLabels = [];
    for (var i = 0; i < this.data[0].length; i++) {
        xLabels.push("");
    }

    var colors = [
        '#2c3e50',
        '#34495e',
        '#8e44ad',
        '#9b59b6',
        '#2980b9',
        '#3498db',
        '#16a085',
        '#1abc9c',
        '#ecf0f1',
        '#f1c40f',
        '#f39c12',
        '#e67e22',
        '#d35400',
        '#e74c3c',
        '#c0392b',
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
        	backgroundColor: 'rgba(0, 0, 0, 0)'
    	},
    	maintainAspectRatio: false,
    	barPercentage: 0.9,
    }
});
}
