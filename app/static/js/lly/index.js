var cnt = 0;

$("document").ready(function () {
	$("#searchForm").bind("submit", function(e){
    	text = $("#search_input").val();
		text = text.replace(/(^\s*)|(\s*$)/g, "");
		if (text != "")
			window.location.href = "/search?wd=" + text;
    	return false;  
	});
	commandInit();
});

function commandInit() {
	if (!loginInfoed) {
		setTimeout("commandInit()", 200);
		return;
	}
	var t = "";
	if (logined) t = accessToken;
	$.post(
		"/api/command",
		{
			access_token: t
		},
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				s = "";
				for (i in data.ids) {
					if (i % 4 == 0)
						s += "<div class='row'>";
					s += "<div class='col-md-3' id='act_" + i + "'></div>";
					if ((i % 4 == 3) || (i == data.ids.length - 1))
						s += "</div>";
				}
				$("#actView").html(s);
				for (i in data.ids) {
					$.post(
						"/api/activity/ginfo",
						{
							id: data.ids[i]
						},
						function(data) {
							data = eval(data);
							if (data.error_code == "200") {
								ts = "";
								ts += "<a href='/activity?id=" + data.id + "'>" + "<h4>" + data.name + "</h4></a>";
								ts += "<div class='tagcloud'>";
								for (j in data.tags)
									ts += "<a href='#'><span>" + data.tags[j] + "</span></a>";
								ts += "</div>";
								ts += "<span class='glyphicon glyphicon-user'></span>";
								ts += "<span>" + data.count + "</span><br>";
								ts += data.description + "<br><hr>";
								$("#act_" + cnt).html(ts);
								++cnt;
							}
						}
					);
				}
			}
		}
	);
}
