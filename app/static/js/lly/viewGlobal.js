var userInfo, accessToken = "";
var logined = false;
var loginInfoed = false;

$("document").ready(function() {
	$("#unlogin_topbar").show();
	$("#logined_topbar").hide();
	
	// load user info
	init();
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
				$.post(
					"/api/user/info",
					{
						access_token : accessToken
					},
					function(data) {
						if (data.error_code == "200") {
							userInfo = eval(data);
							logined = true;
						}
						if (logined) {
							$("#unlogin_topbar").hide();
							$("#logined_topbar").show();
							$("#topbar_nickName").text(userInfo.username);
						}
					}
				);
			}
		}
	);
}

function logoutDo() {
	$.post(
		"/api/user/logout",
		{
			access_token : accessToken
		},
		function(data) {
			if (data.error_code == "200") {
				window.location.href = "/";
			}
		}
	);
};