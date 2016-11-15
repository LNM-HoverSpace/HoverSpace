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
				$(this).addClass('upvoted').removeClass("downvoted");
			else if(type=='downvote')
				$(this).addClass('downvoted').removeClass("upvoted");
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

function setFlag(quesID){
	var URL = new String('/question/')
	URL = URL.concat(quesID, '/flag/')
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		success: function(status){
			console.log(status)
			status = JSON.parse(status)
			if(status['flag'] == 'flagged')
				$(this).addClass('flagged')
			else if(status['flag'] == 'flagRemoved')
				$(this).removeClass("flagged")
			alert(status['message']);
		},
		cache: false
	});
}