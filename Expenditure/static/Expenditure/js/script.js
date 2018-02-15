//for displaying total balence and current balence in gauge
      var cur_bal;
      var tot_bal;

      if(window.balence)
      {
      cur_bal= balence[0]["fields"].balence;
      tot_bal= balence[1]["fields"].balence;
      }

       var yest_bal=parseInt(cur_bal)+parseInt(todays_debits);
      //Balence Left gauge
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart_deb);
        function drawChart_deb() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Balence Left',0]
        ]);

        var options = {
          min: 0,max: tot_bal,width: 300, height: 200,
          redFrom: 0, redTo: tot_bal/5,
          yellowFrom:tot_bal/5, yellowTo: 2*tot_bal/5,
          minorTicks: 5,
          animation:{
        duration: 4000,
        easing: 'inAndOut'
     		 }
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_deb'));

        chart.draw(data, options);
        
        data.setValue(0,1,cur_bal);
        chart.draw(data, options);
      }
      
     //Todays Debits Gauge
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart_cre);

      function drawChart_cre() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Todays Debits',0]
        ]);

        var options = {
          min: 0,max:yest_bal,width: 300, height: 200,
          redFrom: 4*yest_bal/5, redTo: yest_bal,
          yellowFrom:3*yest_bal/5, yellowTo: 4*yest_bal/5,
          minorTicks: 5,
           animation:{
        duration: 4000,
        easing: 'inAndOut'
     		 }
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_cre'));

        chart.draw(data, options);
        data.setValue(0,1,todays_debits);//set value to total debits today
        chart.draw(data, options);
      }
      
      //Todays Credits Gauge
      google.charts.load('current', {'packages':['gauge']});
      google.charts.setOnLoadCallback(drawChart_exp);

      function drawChart_exp() {

        var data = google.visualization.arrayToDataTable([
          ['Label', 'Value'],
          ['Todays Credits',0]
        ]);

        var options = {
          min: 0,max: 50000,width: 300, height: 200,
          redFrom: 0, redTo: 1000,
          yellowFrom:1000, yellowTo: 5000,
          minorTicks: 5,
          animation:{
        duration: 4000,
        easing: 'inAndOut'
     		 }
        };

        var chart = new google.visualization.Gauge(document.getElementById('chart_exp'));

        chart.draw(data, options);
        
         data.setValue(0,1,todays_credits);//set value to total credits today
        chart.draw(data, options);

        
      }

       //Systems pie

      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart_spie);
      function drawChart_spie() {
        var data = google.visualization.arrayToDataTable([
          ['System', 'Debits'],
          ['Breaks',     11],
          ['Engine',      2],
          ['Chasis',  2],
          ['Suspension', 2],
          ['Misc',    7]
        ]);

        var options = {
          title: 'System Wise Analysis',
          is3D: true,
          chartArea:{width:'100%',height:'100%'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('spiechart_3d'));
        chart.draw(data, options);
      }
      
      // Catgory pie 
      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart_cpie);
      function drawChart_cpie() {
        var data = google.visualization.arrayToDataTable([
          ['System', 'Debits'],
          ['Cat1 ', parseInt(price_cat1) ],
          ['Cat2',  parseInt(price_cat2)],
          ['Cat3',  parseInt(price_cat3)],
          ['Other', parseInt(price_other)]
        ]);

        var options = {
          title: 'Category Wise Analysis',
          is3D: true,
          chartArea:{width:'100%',height:'100%'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('cpiechart_3d'));
        chart.draw(data, options);
      }



      //tax donut

      google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart_tdnt);
      function drawChart_tdnt() {
        var data = google.visualization.arrayToDataTable([
          ['Tax', 'Expenditure'],
          ['GST',     parseInt(price_gst)],
          ['NON-GST', parseInt(price_non_gst)]
        ]);

        var options = {
          title: 'Tax Wise Analysis',
          pieHole: 0.4,
          chartArea:{width:'100%',height:'100%'}
        };

        var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
        chart.draw(data, options);
      }
            
$(document).resize(function(){
  drawChart_cre();
  drawChart_deb();
  drawChart_exp();
  drawChart_spie();
  drawChart_cpie();
  drawChart_tdnt();
});


