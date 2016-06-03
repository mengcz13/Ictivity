var role = -1;
var activity = "";
var signList = "";
var signInfo = [];
var signGetCnt = 0;
var	members = [];
var membersRead = false;

$(document).ready(function() {
	$("#infoTab .alert").hide();
	$("#noVerifyDiv").hide();
	$("#verifyDiv").hide();
	$("#signModal .alert").hide();
	$("#signListDiv").hide();
	$("#noSignListDiv").hide();

	actInit();
	infoInit();
	verifyInit();
	signInit();
	
	$("#changeInfoBtn").click(changeInfo);
	$("#newSignToggleBtn").click(signToggle);
	$("#signBtn").click(sign);
});

function actInit() {
	var illegal = false;

	function refreshStat(data) {
		data = eval(data);
		if (data.error_code == "200") {
			$("#activityNameLabel").text(data.name);
			$("#activityCount").text(data.count);
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
				if (!((data.error_code == "200") && (data.role == 2)))
					window.location.href="/404";
				else
					role = data.role;
			});
		} else
			window.location.href="/404";
	}
	if (illegal) {
		window.location.href="/404";
	}
}

function infoInit() {
	if (role == -1) {
		setTimeout("infoInit()", 200);
		return;
	}
	$("#id_input").val(activity.id);
	$("#name_input").val(activity.name);
	$("#description_input").val(activity.description);
	if (activity.ispublic)
		$("#ispublic_input").attr("checked", true);
	else
		$("#ispublic_input").attr("checked", false);
	if (activity.isverify)
		$("#isverify_input").attr("checked", true);
	else
		$("#isverify_input").attr("checked", false);
	var tagsS = "";
	for (i in activity.tags)
		if (i != activity.tags.length - 1)
			tagsS += activity.tags[i] + ",";
		else
			tagsS += activity.tags[i];
	$("#tags_input").val(tagsS);
	s = "";
	for (i in activity.tags) {
		s += '<a href="#"><span>' + activity.tags[i] + '</span></a>';
	}
	$("#activityTags").html(s);
	$("#activityRight").text((activity.ispublic)?"公开":"非公开");
}

function changeInfo() {
	$.post(
		"/api/activity/editInfo",
		{
			access_token: accessToken,
			id: activity.id,
			tags: $("#tags_input").val(),
			description: $("#description_input").val(),
			ispublic: $("#ispublic_input").is(':checked'),
			isverify: $("#isverify_input").is(':checked')
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				alert("成功修改!");
				window.location.reload();
			} else {
				alert("修改失败。");	
			}
		}
	);
}

function verifyInit() {
	if (role == -1) {
		setTimeout("verifyInit()", 200);
		return;
	}
	if (!activity.isverify) {
		$("#noVerifyDiv").show();
		return;
	}
	$.post(
		"/api/activity/verifyList",
		{
			access_token: accessToken,
			act_id: activity.id
		},
		function(data) {
			data = eval(data);
			text = "";
			if (data.error_code == "200") {
				for (i in data.list) {
					text += "<tr><td>" + data.list[i].id + "</td>";
					text += "<td>" + data.list[i].msg + "</td>";
					text += "<td><div class='pull-right'><a class='btn btn-green' onclick='verifyPassBtn(" + data.list[i].id 
						+ ")'><span class='gradient'>通过</span></a>";	
					text += "&nbsp;<a class='btn btn-red' onclick='verifyRejectBtn(" + data.list[i].id 
						+ ")'><span class='gradient'>删除</span></a>";	
					text += "</div></td></tr>";
				}
			}
			$("#verifyList").html(text);
		}
	);
	
	$("#verifyDiv").show();
}

function verifyRejectBtn(id) {
	$.post(
		"/api/activity/verifyReject",
		{
			access_token: accessToken,
			act_id: activity.id,
			id: id
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200")
				verifyInit();
			else
				alert("删除失败。");
		}
	);
}

function verifyPassBtn(id) {
	$.post(
		"/api/activity/verifyPass",
		{
			access_token: accessToken,
			act_id: activity.id,
			id: id
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200")
				verifyInit();
			else
				alert("通过失败。");
		}
	);
}

function signToggle() {
	
	function datetimeInit() {
		Date.prototype.format = function(format) { 
      		var date = { 
              "M+": this.getMonth() + 1, 
              "d+": this.getDate(), 
              "h+": this.getHours(), 
              "m+": this.getMinutes(), 
              "s+": this.getSeconds(), 
              "q+": Math.floor((this.getMonth() + 3) / 3), 
              "S+": this.getMilliseconds() 
    	 	}; 
       		if (/(y+)/i.test(format)) { 
              	format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length)); 
       		} 
      		for (var k in date) { 
              	if (new RegExp("(" + k + ")").test(format)) { 
                    format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? date[k] : ("00" + date[k]).substr(("" + date[k]).length)); 
              	} 
       		} 
    		return format; 
		} 
		
		var nowDate = new Date();
		
		var dL = nowDate.format('yyyy-MM-dd hh:mm:ss');
		$("#signTimeL").val(dL); 
		nowDate.setMinutes(nowDate.getMinutes() + 10);
		var dR = nowDate.format('yyyy-MM-dd hh:mm:ss');
		$("#signTimeR").val(dR);
	}
	
	datetimeInit();
	$("#signModal").modal();
}

function sign() {
	var flag = true;
	$("#signModal .alert").hide();
	
	if ($("#signNameInput").val() == "") {
		$("#signNameWrong").show();
		flag = false;
	}
	
	var dateReg = new RegExp("^[0-9]{4}[-][0-9]{2}[-][0-9]{2} [0-9]{2}[:][0-9]{2}[:][0-9]{2}$");
	if ((!dateReg.test($("#signTimeL").val())) ||
		(!dateReg.test($("#signTimeR").val()))) {
		$("#signTimeWrong").show();
		flag = false;	
	}
	
	var numReg = new RegExp("^[0-9]{4}$");
	if (!numReg.test($("#signCommand").val())) {
		$("#signCommandWrong").show();
		flag = false;
	}
	
	if (!flag) return;
	
	$.post(
		"/api/interact/createSign",
		{
			access_token: accessToken,
			act_id: activity.id,
			name: $("#signNameInput").val(),
			timeL: $("#signTimeL").val(),
			timeR: $("#signTimeR").val(),
			command: $("#signCommand").val(),
			isface: $("#signIsface").is(':checked'),
			isverify: $("#signIsverify").is(':checked')
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				alert("新签到创建成功。");
				$("#signModal").modal("hide");
				signInit();
			} else
				alert("新签到创建失败！");
		}
	);
}

function signInit() {
	if (role == -1) {
		setTimeout("signInit()", 200);
		return;
	}
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
				if (signList.length > 0)
					$("#signListDiv").show();
				else
					$("#noSignListDiv").show();
				for (i in signList) {
					$.post(
						"/api/interact/signInfo",
						{
							access_token: accessToken,
							act_id: activity.id,
							sign_id: signList[i]
						},
						function(data) {
							data = eval(data);
							if (data.error_code == "200") {
								var no = -1;
								for (i in signList)
									if (data._id == signList[i])
										 no = i;
								signInfo[no] = data;
								++signGetCnt;
								if (signGetCnt == signList.length)
									signInfoInit();
							}
						}
					)
				}
			};
		}
	);
}


function signInfoInit() {
	s = "";
	for (i in signInfo) {
		s += "<tr><td>";
		s += signInfo[i]._id;
		s += "</td><td>";
		s += signInfo[i].name;
		s += "</td><td>";
		s += signInfo[i].timeL;
		s += "</td><td>";
		s += signInfo[i].timeR;
		s += "</td><td>";
		s += "<a onclick='signDetailToggle(" + signInfo[i]._id + ")' class='btn btn-small'>";
		s += "<span class='gradient'>详情 </span></a>";
		s += "</td></tr>"
	}
	$("#signList").html(s);
}

function signDetailToggle(sign_id) {
	signDetailInit(sign_id);
	$("#signDetailModal").modal();
}

function signDetailInit(sign_id) {
	
	function signDetailMemberInit(sign_id) {
		var s = "";
		for (i in members) {
			s += "<tr id='signDetailMember" + members[i].id + "'></tr>"
		}
		$("#signDetailMemberDiv").html(s);
		for (i in members) {
			$.post(
				"/api/interact/msigned",
				{
					access_token: accessToken,
					act_id: activity.id,
					sign_id: sign_id,
					user_id: members[i].id
				},
				function(data) {
					data = eval(data);
					if (data.error_code == "200") {
						var nickname = "";
						for (i in members)
							if (members[i].id == data._userid) {
								nickname = members[i].nickname;
								break;
							}
						if (data.signed) {
							s = "<td style='color:#FF0000'>是</td><td>" + nickname + "</td><td>" + data.msg + "</td>";
						} else {
							s = "<td style='color:#00FF00'>否</td><td>" + nickname + "</td><td></td>";
						}
						$("#signDetailMember" + data._userid).html(s);
					}
				}
			)
		}
	}
	
	function signDetailInfoInit(sign_id) {
		$.post(
			"/api/interact/signInfo",
			{
				access_token: accessToken,
				act_id: activity.id,
				sign_id: sign_id
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					var head="<p class='text-success'>", tail="</p>";
					$("#signDetailInfoId").html("123123");
					$("#signDetailInfoName").html(head + data.name + tail);
					$("#signDetailInfoTimeL").html(head + data.timeL + tail);
					$("#signDetailInfoTimeR").html(head + data.timeR + tail);
					$("#signDetailInfoCommand").html(head + data.command + tail);
					var t = (data.isface)?"是":"否";
					var t2 = (data.isverify)?"是":"否";
					$("#signDetailInfoIsface").html(head + t + tail);
					$("#signDetailInfoIsverify").html(head + t2 + tail);
				}
			}
		);
	}
	
	function signDetailURLInit(sign_id) {
		$.post(
			"/api/interact/signurl",
			{
				access_token: accessToken,
				act_id: activity.id,
				sign_id: sign_id
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "200") {
					var s;
					s = "<center><a class='btn btn-blue' href='" + data.url + "' target='_blank'>" +
						"<span class='gradient'>" + "签到认证页" + "</span></a></<center>";
					$("#detailURLDiv").html(s);
					s = "<center><a class='btn btn-green' href='" + "/interact/qrcodeshow?codeurl=" + data.qrcodeurl + "' target='_blank'>" +
						"<span class='gradient'>" + "签到二维码展示" + "</span></a></center>";
					$("#detailPicDiv").html(s);
				}
			}
		);
	}
	
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
				membersRead = true;
				signDetailMemberInit(sign_id);
				signDetailInfoInit(sign_id);
				signDetailURLInit(sign_id);
			}
		}
	);
	
	
}