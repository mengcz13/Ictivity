
$(document).ready(function() {
	var urlReg = new RegExp("codeurl=(.*)");
	var qrcodeurl = window.location.search.substr(1).match(urlReg)[1];
	$("#qrcodeDiv").html(
		"<div class='tab_image'><img src='" + qrcodeurl + "'></div>"
	);
});
