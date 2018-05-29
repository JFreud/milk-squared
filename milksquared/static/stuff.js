var confPassword = function(){
    var passw = document.getElementById("password").value
    var confPassw = document.getElementById("confPassword").value
    var response = document.getElementById("responsePass2")
    if( passw != confPassw ){
	response.innerHTML = "<font color='red'> Passwords do not match </font>"
    }
}
