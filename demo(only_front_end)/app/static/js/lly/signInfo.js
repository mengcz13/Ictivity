var loginInfoed = false, logined = false;
var accessToken;

$(document).ready(function () {
	var nameReg = new RegExp("name=(.*)&isFace");
	var isFaceReg = new RegExp("isFace=(.*)\&");
	var isVerifyReg = new RegExp("isVerify=(.*)");
	var name = window.location.search.substr(1).match(nameReg)[1];
	var isFace = window.location.search.substr(1).match(isFaceReg)[1];
	var isVerify = window.location.search.substr(1).match(isVerifyReg)[1];
	name = decodeURIComponent(name);
	if (isFace == "true")
		isFace = true;
	else
		isFace = false;
	if (isVerify == "true")
		isVerify = true;
	else
		isVerify = false;
	$("#signName").html(name);
	if (!isFace)
		$("#photoDiv").hide();
	if (!isVerify)
		$("#msgDiv").hide();
	$("#signBtn").click(sign);
	
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
			if (!logined)
				window.location.href = "/interact/signError";
		}
	);
});

function sign() {
	if (!loginInfoed) return;
	var formData = new FormData();
	formData.append("photo", $("#signInputfile")[0].files[0]);
	formData.append("access_token", accessToken);
	formData.append("command", $("#signCommand").val());
	formData.append("msg", $("#signMsg").val());
	$.ajax({
		url: "/api/interact/sign",
		type: 'POST',
		cache: false,
		data: formData,
		processData: false,
		contentType: false,
		success: function(data) {
			data = eval(data);
			if (data.error_code == "200")
				window.location.href = "/interact/signSuccess";
			else
				window.location.href = "/interact/signError";
		}
	});
}