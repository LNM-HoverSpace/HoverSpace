$.ajaxSetup({cache: false});

function updateShortDescription(quesID, short_des){
	document.removeChild(".edit-short")
}

function updateQuesVotes(quesID, type){
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
			if(type=='upvote')
				$(this).addClass('upvoted').removeClass("downvoted");
			else if(type=='downvote')
				$(this).addClass('downvoted').removeClass("upvoted");
			else
				$(this).removeClass("upvoted").removeClass("downvoted");
			if(status['type']=='notAllowed')
				alert('You are not allowed to vote your own question')
			else {
				document.getElementById("qvote-count").innerHTML = status['count']
				if(status['type']=='upvote')
					alert('You have successfully upvoted.')
				else if(status['type']=='downvote')
					alert('You have successfully downvoted.')
				else
					alert('Your vote has been removed.')
			}
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

function setQuesFlag(quesID){
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

function updateAnsVotes(ansID, type){
	var URL = new String('/answer/')
	URL = URL.concat(ansID, '/vote/')
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({ voteType: type }),
		success: function(status){
			console.log(status)
			status = JSON.parse(status)
			if(type=='upvote')
				$(this).addClass('upvoted').removeClass("downvoted");
			else if(type=='downvote')
				$(this).addClass('downvoted').removeClass("upvoted");
			else
				$(this).removeClass("upvoted").removeClass("downvoted");
			if(status['type']=='notAllowed')
				alert('You are not allowed to vote your own answer')
			else {
				document.getElementById(ansID).getElementsByTagName("span")[0].innerHTML = status['count']
				if(status['type']=='upvote')
					alert('You have successfully upvoted.')
				else if(status['type']=='downvote')
					alert('You have successfully downvoted.')
				else
					alert('Your vote has been removed.')
			}
		},
		cache: false
	});
}

function setAnsFlag(ansID){
	var URL = new String('/answer/')
	URL = URL.concat(ansID, '/flag/')
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

function setAcceptedAns(quesID, ansID){
	var URL = new String('/question/')
	URL = URL.concat(quesID, '/setAccepted/', ansID)
	console.log(URL)
	$.ajax({
		type: 'POST',
		url: URL,
		contentType: 'application/json; charset=utf-8',
		success: function(status){
			console.log(status)
			status = JSON.parse(status)
			if(status['status'] == 'set')
				$(this).addClass('accepted-on')
			else if(status['status'] == 'removed')
				$(this).removeClass("accepted-on")
			alert(status['message']);
		},
		cache: false
	});
}