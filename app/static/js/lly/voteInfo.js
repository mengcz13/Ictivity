var accessToken;
var loginInfoed = false, logined = false;
var openVote = true;

$(document).ready(function() {
	$("#openView").hide();
	$("#selectView").hide();
	$(".alert").hide();
	$("#voteBtn").click(vote);
	init();
	voteInit();
});

function init() {
	$.post(
		"/api/user/token",
		{},
		function(data) {
			obj = eval(data);
			loginInfoed = true;
			if (obj.error_code == "1")
				logined = false;
			if (obj.error_code == "200") {
				logined = true;
				accessToken = obj.access_token;
			}
		}
	);
}

function voteInit() {
	if (!loginInfoed) {
		setTimeout("voteInit()", 200);
		return;
	}
	var urlReg = new RegExp("code=(.*)");
	var qrcodeurl = window.location.search.substr(1).match(urlReg)[1];
	
	if (qrcodeurl == "") {
		failed();
		return;
	}
	$.post(
		"/api/interact/voteTimeVerify",
		{
			access_token: accessToken,
			code: qrcodeurl
		},
		function(data) {
			deta = eval(data);
			if (data.error_code == "200") {
				$("#voteName").html(data.name);
				$("#captionView").html(data.caption);
				if (data.ischoose) {
					openVote = false;
					
					var s = "";
					for (i in data.chooselist) {
						s += "<div class='input_styled'><div class='rowRadio'><input type='radio' name='voteSelect' value='" +
							data.chooselist[i] + 
							"' id='voteSelect" +
							data.chooselist[i] + 
							"'><label for='voteSelect" + 
							data.chooselist[i] + 
							"'>" +
							data.chooselist[i] + 
							"</label></div></div>";
					}
					$("#selectView").html(s);
					$('input').customInput();
					
					$("#selectView").show();
					$("#openView").hide();
				} else {
					openVote = true;
					$("#openView").show();
					$("#selectView").hide();
				}
			} else {
				failed();
			}
		}
	);
}

function failed() {
	window.location.href = "/interact/voteError";
}

function vote() {
	$(".alert").hide();
	var vote_t = "";
	if (openVote) {
		if ($("#voteMsg").val() == "") {
			$("#voteNameWrong").show();
			return;
		}
		vote_t = $("#voteMsg").val();
	} else {
		if ($("input:checked").length == 0) {
			$("#voteSelectWrong").show();
			return;
		}
		vote_t = $(":checked").val();
	}
	$.post(
		"/api/interact/vote",
		{
			access_token: accessToken,
			msg: vote_t
		},
		function(data) {
			if (data.error_code == "200")
				window.location.href = "/interact/voteSuccess";
			else
				window.location.href = "/interact/voteError";
		}
	);
}