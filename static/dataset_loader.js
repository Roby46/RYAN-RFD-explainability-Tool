
function load_data(){
    var a = document.getElementById('file2').value;
    console.log(a)
    names = a.split("fakepath\\")
    console.log(names)
    console.log(names[1])

    $.ajax({
		type:"POST",
		dataType:"text",
		contentType: "application/text",
		xhrFields: { withCredentials: false },
		crossDomain: true,
		// async: false, // async dovrebbe andare bene in quanto è una componente di output
		data:names[1],
		url:"http://127.0.0.1:5000/upload",
	})
	.done(function(response){
		//   console.log("Response StatisticsComponent: ",outputs['rfds'])
	})
	.fail(function(xhr, textStatus, errorThrown){
		console.log("ERROR: ",xhr.responseText)
		return xhr.responseText;

	}).then(function(value){
		
	})
}
