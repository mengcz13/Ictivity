$("document").ready(function() {
	var obj;
	$(".alert").hide();
	$("#registerBtn").click(function(){
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
		if ($("#password_again_input").val() != $("#password_input").val()) {
			$("#password_again_wrong").show();
			$("#password_input").val("")
			$("#password_again_input").val("");
			canpassed = false;
		}
		if (!canpassed) return;
		$.post(
			"/api/user/register",
			{
				username: $("#username_input").val(), 
			 	password: $.md5($("#password_input").val()),
			 	email: $("#email_input").val(),
			 	location: $("#location_input").val(),
			 	birthday: $("#birthday_input").val()
			},
			function(data) {
				obj = eval(data);
				if (obj.error_code == "200")
					window.location.href = "/";
				else
					$("#general_wrong").show();
			}
		);
	});
});