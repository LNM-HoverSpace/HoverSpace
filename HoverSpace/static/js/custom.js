$.ajaxSetup({cache: false});

function updateVotes(quesID, type){
	var URL = new String('/question/')
	URL = URL.concat(quesID, '/vote/')
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({ voteType: type }),
		success: function(status){
			console.log(status)
			status = JSON.parse(status)
			document.getElementById("vote-count").innerHTML = status['count']
			if(type=='upvote')
				$(this).removeClass("downvoted").addClass('upvoted');
			else if(type=='downvote')
				$(this).removeClass("upvoted").addClass('downvoted');
			else
				$(this).removeClass("upvoted").removeClass("downvoted");
			if(status['type']=='upvote')
				alert('You have successfully upvoted.')
			else if(status['type']=='downvote')
				alert('You have successfully downvoted.')
			else
				alert('Your vote has been removed.')
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
			console.log(status)
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