var name = "", actId = "", signId = "", repeat = false;
var membersList = [], candidateNameList = [], nameList = [];
var accessToken = "";
var logined = false;
var cnt = 0;
var stat = false;
var t;

$(document).ready(function() {
	$("#prizeBtn").click(prize);
	run();

	$("#prizeBtn").attr("disabled", true);
	var nameReg = new RegExp("name=(.*)&actid");
	if (window.location.search.substr(1).match(nameReg) == null) failJump();
	name = window.location.search.substr(1).match(nameReg)[1];
	var actidReg = new RegExp("actid=(.*)&signid");
	if (window.location.search.substr(1).match(actidReg) == null) failJump();
	actId = window.location.search.substr(1).match(actidReg)[1];
	var signidReg = new RegExp("signid=([0-9]*)&repeat");
	if (window.location.search.substr(1).match(signidReg) == null) failJump();
	signId = window.location.search.substr(1).match(signidReg)[1];
	var repeatReg = new RegExp("repeat=true");
	if (window.location.search.substr(1).match(repeatReg) == null)
		repeat = false;
	else
		repeat = true;
	if ((name == "") || (repeatReg == ""))
		failJump();
	$.post(
		"/api/user/token",
		{},
		function(data) {
			obj = eval(data);
			if (obj.error_code == "1")
				logined = false;
			if (obj.error_code == "200") {
				logined = true;
				accessToken = obj.access_token;
			}
			if (!logined)
				failJump();
			listInit();
		}
	);
});

function failJump() {
	window.location.href = "/prizeError";
}

function listInit() {
	$.post(
		"/api/activity/members",
		{
			access_token: accessToken,
			id: actId
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				for (i in data.members) {
					candidateNameList.push(data.members[i].id);
					membersList[data.members[i].id] = data.members[i].nickname;
				}
				listInit2();
			} else
				failJump();
		}
	);
}

function listInit2() {
	for (i in candidateNameList) {
		$.post(
			"/api/interact/msigned",
			{
				access_token: accessToken,
				act_id: actId,
				sign_id: signId,
				user_id: candidateNameList[i]
			},
			function(data) {
				cnt ++;
				data = eval(data);
				if (data.error_code == "200") {
					if (data.signed)
						nameList.push(membersList[data._userid]); 
				} else
					failJump();
				if (cnt == candidateNameList.length)
					readySig();
			}
		)
	}
}

function readySig() {
	$("#prizeBtn").attr("disabled", false);
	$("#btnText").text("开始抽奖");
}

function prize() {
	if (membersList.length == 0) {
		$("#mainText").text("列表已为空");
		$("#prizeBtn").attr("disabled", true);
		return;
	}
	if (stat) {
		stat = false; 
		$("#btnText").text("开始");
		if (!repeat) {
			for (i = t + 1; i < membersList.length; i++) {
				membersList[i-1] = membersList[i];
			}
			membersList.pop();
		}
	} else {
		stat = true;
		$("#btnText").text("停");
	}
}

function run() {
	setTimeout("run()", 10);
	if (!stat) {
		return;
	} else {
		t = Math.floor(Math.random() * membersList.length);
		$("#mainText").text(membersList[t]);
	}
}