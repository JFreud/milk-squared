var confPassword = function(){
    var passw = document.getElementById("password").value
    var confPassw = document.getElementById("confPassword").value
    var response = document.getElementById("responsePass2")
    if( passw != confPassw ){
	response.innerHTML = "<font color='red'> Passwords do not match </font>"
    }
}



var makeBar = function() {
  var id = document.getElementById("gameID").value;
  console.log(id);
  var gamekills;
  var playersAlive;
  var playersDead;
   $.ajax({
      type: "POST",
      url: "/gamekillgraph/" + id,
      async: false,
    }).done(function(response) {
      var obj = JSON.parse(response);
      gamekills = obj.gamekills;
      playersAlive = obj.playersAlive;
      playersDead = obj.playersDead;
    });
  console.log(gamekills);
  var data = d3.values(gamekills);
  var ids = Object.keys(gamekills);
  console.log(ids);

  var chart = d3.select(".bar_chart");
  var margin = {top: 50, right: 50, bottom: 20, left: 20}
  var height = 400;
  var width = 550;
  var spacing = 10;
  console.log(height);
  console.log(width);
  var xAxis = d3.scaleLinear()
                .range([0, width]);
  var barHeight = height / data.length;
  console.log(data.length);
  var bar = chart.selectAll("g").data(data).enter().append("g").attr("transform", function(d, i) {
            return "translate(0," + i * barHeight + ")"; });
  bar.append("rect").attr("width", function(d) {
            return xAxis(d); })
        .attr("height", barHeight - spacing).style("fill", "red").style("stroke", "black");
  bar.append("text")
        .attr("x", function(d) {
            return 20; })
        .attr("y", barHeight / 2)
        .text(function(d) { return d; });
  bar.append("text")
        .attr("x", function(d) {
            return 40; })
        .attr("y", barHeight / 2)
        .text(function(d, i) { return ids[i]; });


  //===== PIE CHART =======
  var height = 400;
  var width = 550;
  var data = [playersAlive, playersDead];
  var labels = ["Players Alive", "Players Dead"]
  var colors = ["green", "red"]
  console.log(data);
  var pChart = d3.select(".pie_chart"),
      radius = Math.min(width, height) / 2,
      g = pChart.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
  var color = d3.scaleOrdinal(["red", "blue"]);
  var pie = d3.pie()
    .sort(null)
    .value(function(d) { return d; });
  var path = d3.arc()
    .outerRadius(radius - 10)
    .innerRadius(0)
  var label = d3.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);
  var otherlabel = d3.arc()
    .outerRadius(radius - 100)
    .innerRadius(radius - 100);
  var arc = g.selectAll(".arc")
    .data(pie(data))
    .enter().append("g")
      .attr("class", "arc");
  arc.append("path")
      .attr("d", path)
      .attr("fill", function(d, i) { return colors[i]; });
  arc.append("text")
      .attr("transform", function(d) { return "translate(" + otherlabel.centroid(d) + ")"; })
      .attr("dy", "0.35em")
      .text(function(d, i) { return labels[i]; });
  arc.append("text")
      .attr("transform", function(d) { return "translate(" + label.centroid(d) + ")"; })
      .attr("dy", "0.35em")
      .text(function(d, i) { return data[i]; });



}
