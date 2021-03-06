var joinData;

$("document").ready(function() {
	joinListInit();
});

function joinListInit() {
	if (!logined) {
		setTimeout(joinListInit, 200);
		return;
	}
	$.post("/api/activity/joinList",
		{access_token : accessToken},
		function(data) {
			joinData = eval(data);
			if (joinData.error_code == 200) {
				for (i in joinData.ids) {
					$.post("/api/activity/info",
					{
						access_token: accessToken,
						id: joinData.ids[i].id
					},
					function(data) {
						data = eval(data);
						if (data.error_code == 200) {
							var showData = "<tr><td>" + data.id + "</td>";
							showData += "<td>" + data.name + "</td>";
							showData += "<td><div class='tagcloud'>";
							for (j in data.tags)
								showData += "<a href='#'><span>" + data.tags[j] + "</span></a>";
							showData += "</div></td>";
							showData += "<td>"
							if (data.ispublic)
								showData += "公开";
							else
								showData += "非公开";
							showData += "</td>";
							showData += "<td>"
							showData += '<a href="/activity?id=' + data.id + '" class="btn btn-blue btn-small" style="outline:none"><span class="gradient">进入活动</span></a>';
							showData += "</td>"
							$("#joinList").append(showData);
						}
					});
				}				
			}
		});
}