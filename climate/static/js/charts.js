

      google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('date', 'Day');
      data.addColumn('number', 'Tmin');
      data.addColumn('number', 'Tmax');

      data.addRows([
        [new Date(2011, 0, 1),  37.8, 80.8],
        [new Date(2011, 0, 2),  30.9, 69.5],
      ]);

      var options = {
        title: 'Napi minimum- és maximumhőmérséklet',
		legend: 'none',
		hAxis: { format: 'MMM yyyy' }
      };

      var chart = new google.charts.Line(document.getElementById('linechart_material'));

      chart.draw(data, options);
    }