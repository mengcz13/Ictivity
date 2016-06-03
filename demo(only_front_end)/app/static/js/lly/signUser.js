var loginInfoed = false, logined = false;

$(document).ready(function() {
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
			}
			mainInit();
		}
	);
}

function jump() {
	window.location.href = "/interact/signInfo" + window.location.search.substr(0);
}

function mainInit() {
	if (logined) 
		jump();
	else {
		$(".alert").hide();
		$("#loginBtn").click(login);
		$("#registerBtn").click(register);
	};
}

function login() {
		$(".alert").hide();
		var canpassed = true;
		if ($("#username_input").val() == "") {
			$("#username_wrong").show();
			canpassed = false;
		}
		if ($("#password_input").val() == "") {
			$("#password_wrong").show();
			canpassed = false;
		}
		if (!canpassed) return false;
		$.post(
			"/api/user/login",
			{
				username: $("#username_input").val(), 
			 	password: $.md5($("#password_input").val()),
			},
			function(data) {
				obj = eval(data);
				if (obj.error_code == "200")
					jump();
				else if (obj.error_code == "1")
					$("#username_wrong2").show();
				else if (obj.error_code == "2") {
					$("#password_input").val("");
					$("#password_wrong2").show();
				} else
					$("#general_wrong").show();
			}
		);
	return false;
}

function register() {
		$(".alert").hide();
		var canpassed = true;
		if ($("#rusername_input").val() == "") {
			$("#rusername_wrong").show();
			canpassed = false;
		}
		if ($("#rpassword_input").val() == "") {
			$("#rpassword_wrong").show();
			canpassed = false;
		}
		if ($("#rpassword_again_input").val() != $("#rpassword_input").val()) {
			$("#rpassword_again_wrong").show();
			$("#rpassword_input").val("")
			$("#rpassword_again_input").val("");
			canpassed = false;
		}
		if (!canpassed) return;
		$.post(
			"/api/user/register",
			{
				username: $("#rusername_input").val(), 
			 	password: $.md5($("#rpassword_input").val()),
			 	email: $("#remail_input").val(),
			 	location: $("#rlocation_input").val(),
			 	birthday: $("#rbirthday_input").val()
			},
			function(data) {
				obj = eval(data);
				if (obj.error_code == "200")
					jump();
				else
					$("#rgeneral_wrong").show();
			}
		);
}