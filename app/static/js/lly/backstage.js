var role = -1;
var activity = "";

$(document).ready(function() {
	$("#infoTab .alert").hide();

	actInit();
	infoInit();
	
	$("#changeInfoBtn").click(changeInfo);
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
}

function changeInfo() {
	alert("1");
}
