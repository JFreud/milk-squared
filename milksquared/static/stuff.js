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
  var chart = d3.select(".bar_chart");

   $.ajax({
      type: "POST",
      url: "/gamekillgraph/" + id,
      async: false,
    }).done(function(response) {
      var obj = JSON.parse(response);
      gamekills = obj.gamekills;
    });
    console.log(gamekills);
}
