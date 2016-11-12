$.ajaxSetup({cache: false});

function updateVotes(quesID, type){
	//$.ajaxSetup({cache: false});
	var URL = new String('/question/')
	URL = URL.concat(quesID, '/vote/')
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({ voteType: type }),
		dataType : 'json',
		success: function(status){
			status = JSON.parse(status)
			console.log("hry")
			document.getElementById("vote-count").innerHTML = status['count']
			//status['count'];
			//document.getElementById("optionone").setAttribute("value", "green");
			if(type=='up')
				$(this).removeClass("downvoted").addClass('upvoted');
			else
				$(this).removeClass("upvoted").addClass('downvoted');
		},
		cache: false
	});
}


function setBookmark(quesID){
	var URL = new String('/question/')
	URL = URL.concat(quesID, '/bookmark/')
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		success: function(status){
			status = JSON.parse(status)
			if(status['status'] == 'true')
				$(this).addClass('bookmarked')
			else
				$(this).removeClass("bookmarked")
			alert(status['message']);
		},
		cache: false
	});
}