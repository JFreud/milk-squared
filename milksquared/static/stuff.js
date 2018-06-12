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
   $.ajax({
      type: "POST",
      url: "/gamekillgraph/" + id,
      async: false,
    }).done(function(response) {
      var obj = JSON.parse(response);
      gamekills = obj.gamekills;
    });
  console.log(gamekills);
  var data = d3.values(gamekills);

  var chart = d3.select(".chart");
  var height = 400;
  var width = 550;
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
        .attr("height", barHeight);
   bar.append("text")
        .attr("x", function(d) {
            return xAxis(d) + 20; })
        .attr("y", barHeight / 2)
        .text(function(d) { return d; });

}
