$("document").ready(function() {
	// load user info
	newActivityInit();
	
	$("#createBtn").click(function() {
		newActivityInit();
		$.post(
			"/api/activity/create",
			{
				access_token: accessToken,
				name: $("#activitiyName_input").val(),
				tags: $("#tags_input").val(),
				description: $("#description_input").val(),
				ispublic: $("#signIspublic_input").is(':checked'),
				isverify: $("#signIsverify_input").is(':checked')
			},
			function(data) {
				data = eval(data);
				if (data.error_code == "1")
					alert("您尚未登录，不能创建新活动");
				if (data.error_code == "2")
					$("#general_wrong").show();
				if (data.error_code == "200") {
					alert("新活动创建成功");
					window.location.href = "/activity?id=" + data._id; 
				}
			}
		);
	});
});

function newActivityInit() {
	$("#activitiyName_wrong").hide();
	$("#tags_input_wrong").hide();
	$("#description_input_wrong").hide();
	$("#general_wrong").hide();
}