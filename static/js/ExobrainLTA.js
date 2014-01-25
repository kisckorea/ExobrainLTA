var baseUrl = 'http://127.0.0.1:8000/';

var username;
var password;
var loginstring;
var candidateID;

var doJoin = function() {
	username = $("#username").val();
	name = $("#name").val();
	password = $("#password").val();
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/create/',
		data : {
			username : username,
			name : name,
			password : password
		},
		success : function() {
			
			location.href = "login.html";
		},
		error : function(msg) {
			alert("Error!");
		},
	});
};
var goAdmin = function() {
	location.href = baseUrl + "admin/";
};
var doLogin = function() {
	username = $('#username').val();
	password = $('#password').val();
	loginstring = "Basic " + Base64.encode(username + ":" + password);

	$.ajax({
		type : 'get',
		async : true,
		url : baseUrl + 'api/login/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			setLoginString();
			window.location = "task.html";
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
};
var doGetTask = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/task/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {

			for (var i in data.group_list) {
				//alert(data.group_list[i]);
				doAppendTaskGroup(data.group_list[i]);
			}

			//doAppendTaskGroup(data);

			$("#username").html(username);
			$("#first_name").html(firstname);
			//$("#total").html(data.test);
			$("#total").html('100');
			$("#mine").html('0');
			//$("#mine").html($('[name=deleteMsg]').length - 1);

		},
		error : function() {
			alert("Fail to get data!!!");
		},
	});
};

var doAppendTaskGroup = function(data) {

	node = $('#groupTemplate').clone();

	$('.sub_cluster_0', node).append(data);
	//$('.sub_cluster_1', node).append(data[1]);

	// $('.like', node).prepend(data.liked + "  ");
	$('#like', node).attr("value", data.id);

	node.show();
	$('#grouparea').append(node);
};

var doGetSubtask = function() {
	var group = $(this).parent().text();
	
	
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/subtask/',
		data : {
			group : group
			
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
			
		},
		success : function(data) {
			
			$('.selected_group', node).append(data.subject);
			
			//빨리 subtask에서 넘겨준 내용을 뿌려야함
			/*
			for (var i in data.candidates) {
				
				doAppendSubTaskCandidate(data.candidates[i]);
				
			}
			*/
			//지금은 노가다로 찍고 있음
			doAppendSubTaskCandidate(data.candidates1, data.candidates1_c);
			doAppendSubTaskCandidate(data.candidates2, data.candidates2_c);
			doAppendSubTaskCandidate(data.candidates3, data.candidates3_c);
			doAppendSubTaskCandidate(data.candidates4, data.candidates4_c);
			doAppendSubTaskCandidate(data.candidates5, data.candidates5_c);
			$(".selected_group").html(data.selected_group);
			 $("#username").html(username);
			 $("#total").html(data.total);
			 $("#mine").html(data.mine);
			
		},
		error : function(msg) {
			alert("subtask Error!");
		},
	});
};

var doClearSubTask = function() {
	$(".selected_group").html('');
	$('#candidateTemplate').html('');
	$('#candidatearea').html('');
};
var doAppendSubTaskCandidate = function(data,data2) {

	node = $('#candidateTemplate').clone();
	
	//지금은 노가다로 찍고 있음
	$('.triple', node).append(data);
	$('.triple', node).append(" (");
	$('.triple', node).append(data2);
	$('.triple', node).append("개)");
	
	//빨리 subtask에서 넘겨준 내용을 뿌려야함
	/*
	$('.triple', node).append(" ");
	$('.triple', node).append(data.object);
	$('.sub_cluster_1', node).append(data[1]);

	$('.like', node).prepend(data.liked + "  ");
	
	$('#select_candidate', node).attr("value", data.id);
	*/
	node.show();
	$('#candidatearea').append(node);
};

//FOR Validation
var doCompleteValidation = function() {

	var subject = $("#knowledge_subject").text();
	var object = $("#knowledge_object").text();
	var predicate = $("#knowledge_predicate").text();
	var triple = subject + ":" + object + ":" + predicate;

	var validated = $("input[name='answer']:checked").val();

//	alert(triple);

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/validation/create/',
		data : {
			triple : triple,
			validated : validated

		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function() {
			alert('저장완료');
			//doReloadValidation();
		},
		error : function(msg) {
			alert("Fail to write data!");
		},
	});
};
var doGetValidation = function() {
	
	//subtask.html에서 user가 선택한 버튼의 id를 읽어와서 그 id에 해당하는 지식을 서버에서 가져와야함
	// var triple = $(this).parent().text();
	// var id = $(this).val();
	
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/validation/',
		// data : {
			// id : id
		// },
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			
			//alert('validation success');
			
	
			//alert(data.subject);

			// for (var i in data) {
			// alert(data[i]);
// 			
			// }
			
			//현재는 강제로 이동시킴
			window.location = "validation.html";
			
			doAppendValidationSubject(data);
			doAppendValidationObject(data);

			$("#knowledge_subject").html(data.subject);
			$("#knowledge_object").html(data.object);
			$("#knowledge_predicate").html(data.predicate);

			$("#username").html(username);
			//$("#total").html(data.total_count);

		},
		error : function() {
			alert("Validation: Fail to get data!");
		},
	});
};

var doGetValidation2 = function() {
	// var triple = $(this).parent().text();
	// var id = $(this).val();
	
	//alert(id);
	//doGoValidation(id);
	
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/validation2/',
		// data : {
			// id : id
		// },
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			
			
			
	
			//alert(data.subject);

			// for (var i in data) {
			// alert(data[i]);
// 			
			// }
			window.location = "validation2.html";
			
			doAppendValidationSubject(data);
			doAppendValidationObject(data);

			$("#knowledge_subject").html(data.subject);
			$("#knowledge_object").html(data.object);
			$("#knowledge_predicate").html(data.predicate);

			$("#username").html(username);
			//$("#total").html(data.total_count);

		},
		error : function() {
			alert("Validation: Fail to get data!");
		},
	});
};

var doAppendValidationSubject = function(data) {

	node = $('#subTemplate').clone();

	$('.subject', node).append(data.subject);
	$('.sub_desc', node).append(data.sub_desc);

	// $('.like', node).prepend(data.liked + "  ");
	// $('#like', node).attr("value", data.id);

	node.show();
	$('#subjectarea').append(node);
};
var doAppendValidationObject = function(data) {

	node = $('#objTemplate').clone();

	$('.object', node).append(data.object);
	$('.obj_desc', node).append(data.obj_desc);

	// $('.like', node).prepend(data.liked + "  ");
	// $('#like', node).attr("value", data.id);

	node.show();
	$('#objectarea').append(node);
};
//FOR TIMELINE
var doWriteTimeline = function() {
	var msg = $("#writearea").val();
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/create/',
		data : {
			message : msg
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function() {

			doReload();
		},
		error : function(msg) {
			alert("Fail to write data!")
		},
	});
};
var doGetTimeline = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/timeline/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			for (var i in data.messages) {
				doAppend(data.messages[i]);
			}
			$("#total").html(data.total_count);
			$("#mine").html($('[name=deleteMsg]').length - 1);
			$("#username").html(username);
			$("#writearea").val("");
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
};
var doAppend = function(data) {
	node = $('#msgTemplate').clone();

	$('.name', node).append(data.username);
	$('.content', node).append(data.message);
	$('.date', node).append(data.created);
	$('.like', node).prepend(data.liked + "  ");
	$('#like', node).attr("value", data.id);

	if (username == data.username)
		$('[name=deleteMsg]', node).attr("value", data.id);
	else
		$('[name=deleteMsg]', node).remove();

	node.show();
	$('#timelinearea').append(node);
};

var doReloadValidation = function() {
	doClear();
	//doGetValidation();
};

var doReload = function() {
	doClear();
	doGetTimeline();
};

var doClear = function() {
	$('#timelinearea').html('')
};
var doDeleteTimeline = function() {
	var id = $(this).val();
	alert(id);
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/' + id + "/delete/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			doReload();
		},
		error : function(msg) {
			alert("Fail to delete data!");
		},
	});
};
var doSearchTimeline = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/timeline/find/',
		data : {
			query : $("#search").val()
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			doClear();
			for (var i in data) {
				doAppend(data[i]);
			}
			$("#total").html(data.length);
			$("#mine").html($('[name=deleteMsg]').length - 1);
			$("#search").val("");
		},
		error : function() {
			alert("Fail to get data!");
		},
	});
};
var doLogout = function() {
	resetLoginString();
	window.location = "login.html";
};
var doLike = function() {
	var id = $(this).val();
	alert(id);
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/timeline/' + id + "/like/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function() {
			doReload();
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
};
var doGetUserInfo = function() {
	var username = $("div", this).html();
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/profile/' + username + "/",
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			$("#modalid").html(data.username);
			$("#modalnickname").html(data.nickname);
			$("#modalcountry").html(data.country);
			$("#modalcomment").html(data.comment);
			$("#modalurl").html(data.url);
			$("#myModal").modal("show");

		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
//END TIMELINE

// FOR PROFILE
var doGetProfile = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/profile/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			console.log(data);
			fillProfile(data);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var fillProfile = function(data) {

	$("#bigid").html(data.username);
	$("#bignickname").html(" a.k.a " + data.nickname);
	$("#bigcomment").html(data.comment);

	$("#comment").val(data.comment);
	$("#nickname").val(data.nickname);
	$("#country").val(data.country);
	$("#web").val(data.url);
	$("#labelnick").html("Nickname : " + data.nickname);
	$("#labelcountry").html("Country : " + data.country);
	$("#labelurl").html("URL : " + data.url);
};
var doSetProfile = function() {
	var nickname = $("#nickname").val();
	var comment = $("#comment").val();
	var country = $("#country").val();
	var url = $("#web").val();

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/profile/',
		data : {
			nickname : nickname,
			comment : comment,
			country : country,
			url : url
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			location.href = "profile.html";
		},
		error : function(msg) {
			alert("Error!");
		},
	});
};
var doCancel = function() {
	location.reload();
};
//END PROFILE

//FOR ACCOUNT
var doCheckPassword = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/checkpassword/',
		data : {
			password : $("#oldpassword").val()
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert(data.status);
			console.log(data);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doSetPassword = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/setpassword/',
		data : {
			password : $("#newpassword").val()
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			loginstring = "Basic " + Base64.encode(username + ":" + $("#newpassword").val());
			setLoginString();
			$("#oldpassword").val($("#newpassword").val());
			$("#newpassword").val("");
		},
		error : function(msg) {
			alert(msg.responseText);
		},
	});
};
var doGetName = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/user/name/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			$("#getname").val(data.name);
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doSetName = function() {
	$.ajax({
		type : 'post',
		url : baseUrl + 'api/user/name/',
		data : {
			name : $("#getname").val()
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
};

var doGetUserList = function() {
	$.ajax({
		type : 'get',
		url : baseUrl + 'api/user/list/',
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			console.log(data);
			myIgnoreList = new Array();
			$('#listarea').html("");
			for (var i in data) {
				if (username == data[i].username)
					myIgnoreList = data[i].ignores;
			}
			for (var i in data) {
				if (username != data[i].username)
					doAppendIgnored(data[i], myIgnoreList);
			}
		},
		error : function(msg) {
			alert("Fail to get data!");
		},
	});
};
var doAppendIgnored = function(data, ignoreList) {

	var isIgnored = $.inArray(data.user, ignoreList);

	node = $('#ignoreTemplate').clone();
	$('#name', node).html(data.username);
	$('.ignoreBtn', node).attr("value", data.user);

	if (isIgnored == -1) {
		$('#ignored', node).html("");
		$('#icon', node).removeClass().addClass("icon-plus");
	} else {
		$('#ignored', node).html(" : Ignored");
		$('#icon', node).removeClass().addClass("icon-minus");
	}

	node.show();
	$('#listarea').append(node);
};
var doIgnore = function() {
	var id = parseInt($(this).val());
	var isIgnored = $.inArray(id, myIgnoreList);

	if (isIgnored == -1)
		myIgnoreList.push(id);
	else
		myIgnoreList.splice(isIgnored, 1);

	$.ajax({
		type : 'post',
		url : baseUrl + 'api/profile/',
		data : {
			ignore : "[" + myIgnoreList.toString() + "]"
		},
		beforeSend : function(req) {
			req.setRequestHeader('Authorization', loginstring);
		},
		success : function(data) {
			alert("OK");
			doGetUserList();
		},
		error : function(msg) {
			alert("Fail to set data!");
		},
	});
};
//END ACCOUNT

// UTILITY METHODS 세션에 인증 데이터를 남겨 놓기 위한 방법
function setCookie(name, value, day) {
	var expire = new Date();
	expire.setDate(expire.getDate() + day);
	cookies = name + '=' + escape(value) + '; path=/ ';
	if ( typeof day != 'undefined')
		cookies += ';expires=' + expire.toGMTString() + ';';
	document.cookie = cookies;
}

function getCookie(name) {
	name = name + '=';
	var cookieData = document.cookie;
	var start = cookieData.indexOf(name);

	var value = '';
	if (start != -1) {
		start += name.length;
		var end = cookieData.indexOf(';', start);
		if (end == -1)
			end = cookieData.length;
		value = cookieData.substring(start, end);
	}
	return unescape(value);
}

function getLoginString() {
	loginstring = getCookie("loginstring");
	username = getCookie("username");
}

function getCandidateID() {
	loginstring = getCookie("candidateID");
}

function setLoginString() {
	setCookie("loginstring", loginstring, 1);
	setCookie("username", username, 1);
}
function setCandidateID() {
	setCookie("candidateID", candidateID, 1);
	
}

function resetLoginString() {
	setCookie("loginstring", "", "-1");
	setCookie("username", "", "-1");
}

//login string의 유효성 검사, loginstring이 비어있다면 현재 페이지 접근을 막고 이전 페이지로 돌아감.
function checkLoginString() {
	if (loginstring == "") {
		history.back();
	}
}
