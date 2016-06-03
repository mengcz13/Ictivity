$("document").ready(function() {
	var obj;
	$(".alert").hide();
	$("form").bind("submit", login);
	$("#loginBtn").click(login);
});

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
					window.location.href = "/";
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