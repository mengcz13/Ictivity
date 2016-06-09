var role = -1;
var activity = "";
var members;
var signList;

$(document).ready(function() {
	$("#mainTab").hide();
	$("#commentWrong").hide();
	$("#noticeWrong").hide();
	$("#noSignDiv").hide();
	$("#signDiv").hide();
	actInit();
	detailInit();
	noticesInit();
	signInit();
	commentsInit();
	membersInit();

	$("#joinToggleBtn").click(joinToggle);
	$("#joinMsgBtn").click(joinActivity);
	$("#commentToggleBtn").click(commentToggle);
	$("#commentToggleBtn2").click(commentToggle);
	$("#commentBtn").click(newComment);
	$("#noticeToggleBtn").click(noticeToggle);
	$("#noticeBtn").click(newNotice);
	$("#backstageToggleBtn").click(backstageToggle);
});

function actInit() {
	var illegal = false;

	function refreshStat(data) {
		data = eval(data);
		if (data.error_code == "200") {
			$("#activityNameLabel").text(data.name);
			$("#activityTags").html("");
			s = "";
			for (i in data.tags) {
				s += '<a href="#"><span>' + data.tags[i] + '</span></a>';
			}
			$("#activityTags").html(s);
			$("#activityDescription").text(data.description);
			$("#activityCount").text(data.count);
			$("#activityRight").text((data.ispublic)?"公开":"非公开");
			activity = data;
			return false;
		}
		return true;
	}

	if (!loginInfoed) {
		setTimeout("actInit()", 200);
		return;
	}
	var idReg = new RegExp("id=([0-9]*)");
	var id = window.location.search.substr(1).match(idReg);
	
	if (id[1] == "") illegal = true;
	if (!illegal) {
		if (logined) {
			$.post("/api/activity/info",
			{
				access_token: accessToken,
				id: id[1]
			},
			function(data) {
				illegal = refreshStat(data);
				if (illegal) 
					window.location.href="/404";
			});
			$.post("/api/activity/role",
			{
				access_token: accessToken,
				id: id[1]
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200")
					role = data.role;
				else
					window.location.href="/404";
			});
		} else {
			role = 0;
			$.post("/api/activity/ginfo",
			{
				id: id[1]
			},
			function(data) {
				illegal = refreshStat(data);
				if (illegal)
					window.location.href="/404";
			});
		}
	}
	if (illegal) {
		window.location.href="/404";
	}
}

function detailInit() {
	if (role == -1) {
		setTimeout("detailInit()", 200);
		return;
	}
	if (role == 0) {
		$(".touristTab").show();
		$(".clientTab").hide();
		$(".managerTab").hide();
		$("#roleTab").html("您尚未加入此活动。");
	}
	if (role == 1) {
		$(".touristTab").hide();
		$(".clientTab").show();
		$(".managerTab").hide();
		$("#roleTab").html("您已加入此活动。");
	}
	if (role == 2) {
		$(".touristTab").hide();
		$(".clientTab").hide();
		$(".managerTab").show();
		$("#roleTab").html("您是此活动的管理员。");
	}
	$("#mainTab").show();
}

function noticesInit() {
	if (role == -1) {
		setTimeout("noticesInit()", 200);
		return;
	}
	if ((role == 1) || (role == 2)) { // list for joiner(1) and manager(2)
		$.post(
			"/api/activity/notices",
			{
				access_token: accessToken,
				id: activity.id
			},
			function(data) {
				if (data.error_code == "200") {
					if (role == 1)
						$("#notices").html("");
					if (role == 2)
						$("#mnotices").html("");
					var notices = "";
					for (i in data.notices) {
						notices += '<div class="notice">'
						notices += "<h2>" + data.notices[i].title + "</h2>";
						notices += '<div class="trade-time">';
						notices += data.notices[i].time;
						notices += '</div>';
						notices += '<div class="tab-text h4">'
						notices += data.notices[i].text;
						notices += '</div>';
						notices += '</div>';
						if (i != data.notices.length - 1)
							notices += '<hr>';
					}
					if (role == 1)
						$("#notices").html(notices);
					if (role == 2)
						$("#mnotices").html(notices);
				}
			}
		);
	}
}

function signInit() {
	if (role == -1) {
		setTimeout("signInit()", 200);
		return;
	}
	if (role == 1) {
		$.post(
			"/api/interact/signList",
			{
				access_token: accessToken,
				act_id: activity.id
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					signList = data.ids;
					if (data.ids.length == 0) {
						$("#noSignDiv").show();
					} else {
						var s = "";
						for (i in data.ids) {
							s += "<tr><td>" + data.ids[i].id + "</td><td>" + data.ids[i].name +
								"</td><td id='isSign" + data.ids[i].id + "'></td></tr>";
						}
						$("#signItems").html(s);
						$("#signDiv").show();
					}
					for (i in signList)
						$.post(
							"/api/interact/signed",
							{
								access_token: accessToken,
								act_id: activity.id,
								sign_id: signList[i].id
							},
							function(data) {
								data = eval(data);
								if (data.error_code == "200") {
									$("#isSign" + data._signid).html((data.signed)?"<span class='text-success'>是</span>":"<span class='text-danger'>否</span>");
								}
							}
						);
				}
			}
		);
	}
}

function commentsInit() {
	if (role == -1) {
		setTimeout("commentsInit()", 200);
		return;
	}
	if ((role == 1) || (role == 2)) { // list not for tourist
		$.post(
			"/api/activity/comments",
			{
				access_token: accessToken,
				id: activity.id
			},
			function(data) {
				if (data.error_code == "200") {
					if (role == 1)
						$("#comments").html("");
					if (role == 2)
						$("#mcomments").html("");
					var comments = "";
					for (i in data.comments) {
						comments += '<div class="comment">'
						comments += "<h4 style='text-color:##457b9a'>" + data.comments[i].nickname + "</h4>";
						comments += '<div class="trade-time">';
						comments += data.comments[i].time;
						comments += '</div>';
						comments += '<div class="tab-text h4">'
						comments += data.comments[i].text;
						comments += '</div>';
						comments += '</div>';
						if (i != data.comments.length - 1)
							comments += '<hr>';
					}
					if (role == 1)
						$("#comments").html(comments);
					if (role == 2)
						$("#mcomments").html(comments);
				}
			}
		);
	}
}

function membersInit() {
	if (role == -1) {
		setTimeout("membersInit()", 200);
		return;
	}
	if ((role == 1) || (role == 2)) {
		$.post(
			"/api/activity/members",
			{
				access_token: accessToken,
				id: activity.id
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					members = data.members;
					text = "";
					text += "<div class='mytab'>";
					text += "共有&nbsp;" + members.length + "&nbsp;名成员"
					text += "</div>"
					for (i in members) {
						if (i % 3 == 0)
							text += "<div class='row'>";
						text += "<div class='col-md-4'>";
						text += "<div class='tab_image'>";
						text += "<img src='" + "/static/images/icons/user.png" + "' alt>";
						text += "<div class='text-center'>" + members[i].nickname + "</div>";
						text += "<div class='text-center' style='color:#FF1111'>";
						if (members[i].ismanager) text += "管理员";
						text += "</div>";
						text += "</div>";
						text += "</div>";
						if ((i % 3 == 2) || (i == members.length - 1))
							text += "</div>"
						if (i == 50)
							break;
					}
					if (members.length > 50) {
						if (role == 1) // client
							text += "<div class='text-center'><a href='#' id='memberMoreToggleBtn'>更多</a></div>";
						if (role == 2)
							text += "<div class='text-center'><a href='#' id='mmemberMoreToggleBtn'>更多</a></div>";
					}
					if (role == 1) {
						$(".clientTab #memberSpace").html(text);
						$("#memberMoreToggleBtn").click(memberMore);
					}
					if (role == 2) {						
						$(".managerTab #memberSpace").html(text);
						$("#mmemberMoreToggleBtn").click(memberMore);
					}
				}
			}
		);
	}
}

function memberMore() {
	text = "";
	text += "<div class='mytab'>";
	text += "共有&nbsp;" + members.length + "&nbsp;名成员"
	text += "</div>"
	for (i in members) {
		if (i % 4 == 0) text += "<div class='row'>";
		text += "<div class='col-md-3'>";
		text += "<div class='tab_image'>";
		text += "<img src='" + "/static/images/icons/user.png" + "' alt>";
		text += "<div class='text-center'>" + members[i].nickname + "</div>";
		text += "<div class='text-center' style='color:#FF1111'>";
		if (members[i].ismanager) text += "管理员";
		text += "</div>";
		text += "</div>";
		text += "</div>";
		if ((i % 4 == 3) || (i == members.length - 1)) text += "</div>"
	}
	$("#memberMoreDiv").html(text);
	$("#memberMoreModal").modal();
}

function joinToggle() {
	if (!logined) {
		alert("抱歉，您尚未登录。");
		window.location.href="/user/login";
	}
	if (!activity.isverify) {
		$("#joinMsgDiv").hide();
	}
	$("#joinModal").modal();
}	

function joinActivity() {
	if (activity.isverify)
		$.post(
			"/api/activity/join",
			{
				access_token: accessToken,
				id: activity.id,
				nickname: $("#nicknameInput").val(),
				join_msg: $("#joinMsgInput").val()
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					alert("申请已成功提交！");
					$("#joinModal").modal("hide");
				} else {
					alert("申请提交失败。");
				}
			}
		)
	else
		$.post(
			"/api/activity/join",
			{
				access_token: accessToken,
				id: activity.id,
				nickname: $("#nicknameInput").val(),
				join_msg: ""
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					window.location.reload();
				} else {
					alert("加入申请提交失败。");
				}
			}
		);
}

function commentToggle() {
	$("#commentModal").modal();
}

function newComment() {
 	if ($("#commentInput").val().length < 15) {
 		$("#commentWrong").show();
 		return;
 	}
	$.post(
		"/api/activity/newComment",
		{
			access_token: accessToken,
			id: activity.id,
			comment: $("#commentInput").val()
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				window.location.reload();
			} else {
				alert("评论提交失败。");
			}
		}
	);
}

function noticeToggle() {
	$("#noticeModal").modal();
}

function newNotice() {
	if (($("#noticeInput").val() == "") || ($("noticeTitleInput").val() == "")) {
		$("#noticeWrong").show();
		return;
	}
	$.post(
		"/api/activity/newNotice",
		{
			access_token: accessToken,
			id: activity.id,
			title: $("#noticeTitleInput").val(),
			notice: $("#noticeInput").val()
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				window.location.reload();
			} else {
				alert("公告发布失败。");
			}
		}
	);
}

function backstageToggle() {
	window.open("/backstage?id=" + activity.id);
}