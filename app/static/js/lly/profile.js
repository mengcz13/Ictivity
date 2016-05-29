$("document").ready(function() {
	basicInfoInit();
	pwdInit();
	
	$("#basicForm").bind("submit", saveBasic);
	$("#basicSaveBtn").click(saveBasic);
	
	$("#pwdForm").bind("submit", changepwd);
	$("#passwordChangeBtn").click(changepwd);
	
	$("#uploadWrong").hide();
	$("#uploadToggleBtn").click(function() {
		$("#photoUploadModal").modal();
	});
	$("#uploadPhotoBtn").click(uploadPhoto);
	
	$("#photoLoadToggle").click(loadPhoto);
});

function basicInfoInit() {
	$("#basic_wrong").hide();
	if (!logined) {
		setTimeout(basicInfoInit, 200);
		return;
	}
	$.post(
		"/api/user/info",
		{
			access_token: accessToken
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				$("#username_input").val(data.username);
				$("#email_input").val(data.email);
				$("#location_input").val(data.location);
				$("#birthday_input").val(data.birthday);
			} else 
				$("#basic_wrong").show();
		}
	)
}

function saveBasic() {
	$(".alert").hide();
	$.post(
		"/api/user/changeinfo",
		{
			access_token: accessToken,
			email: $("#email_input").val(),
			location: $("#location_input").val(),
			birthday: $("#birthday_input").val()
		},
		function(data) {
			obj = eval(data);
			if (obj.error_code == "200")
				window.location.reload();
			else 
				$("#basic_wrong").show();
		}
	);
	return false;
}

function changepwd() {
	$(".alert").hide();
	if ($("#newpassword_input").val() != $("#newpassword2_input").val()) {
		$("#newpassword2_wrong").show();
		return false;
	}
	if ($("#newpassword_input").val() == "") {
		$("#newpassword_wrong").show();
		return false;
	}
	$.post(
		"/api/user/changepwd",
		{
			access_token: accessToken,
			oldpwd: $("#password_input").val(),
			newpwd: $("#newpassword_input").val()
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "3")
				$("#password_wrong").show();
			else if (data.error_code != "200")
				$("#password_wrong").show();
			else {
				alert("密码已修改。");
				window.location.reload();
			}
		}
	);
	return false;
}

function pwdInit() {
	$("#password_input").val("");
	$("#newpassword_input").val("");
	$("#newpassword2_input").val("");
	$("#password_wrong").hide();
	$("#newpassword_wrong").hide();
	$("#newpassword2_wrong").hide();
	$("#pwd_wrong").hide();
}

function uploadPhoto() {
	var formData = new FormData();
	formData.append("photo", $("#inputfile")[0].files[0]);
	formData.append("access_token", accessToken);
	$.ajax({
		url: "/api/user/uploadphoto",
		type: 'POST',
		cache: false,
		data: formData,
		processData: false,
		contentType: false,
		success: function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				window.location.reload();
			} else {
				$("#uploadWrong").show();
				$("#uploadWrongSpan").text(data.error_code);
			}
		}
	});
}

function loadPhoto() {
	$.post(
		"/api/user/photos",
		{
			access_token: accessToken
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				$("#photoCount").text(data.photos.length);
				$("#photoSpace").text("");
				cont = "";
				for (i in data.photos) {
					if ((i % 4) == 0) {
						cont += "<div class='row'>";
					}
					cont += "<div class='col-md-4'><div class='tab_image'>";
					cont += "<img src='" + data.photos[i].url + "' alt>";
					cont += "<div class='widget-trade'><div class='trade-time'>" + data.photos[i].time + "</div></div>";
					cont += "</div></div>";
					if (((i % 4) == 3) || (i == (data.photos.length - 1))) {
						cont += "</div>";
					}
				}
				$("#photoSpace").append(cont);
			}
		}
	);
}