
$(document).ready(function() {

	var urlReg = new RegExp("code=(.*)");
	var qrcodeurl = window.location.search.substr(1).match(urlReg)[1];

	if (qrcodeurl == "") {
		failed();
		return;
	}
	
	$.post(
		"/api/interact/signTimeVerify",
		{
			code: qrcodeurl
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				var isface, isverify;
				if (data.isFace)
					isface = "true";
				else
					isface = "false";
				if (data.isVerify)
					isverify = "true";
				else
					isverify = "false";
				window.location.href = "/interact/signUser?name=" + data.name + "&isFace=" + isface + "&isVerify=" + isverify;
			}
		}
	);

});

function failed() {
	window.location.href = "/interact/signError";
}