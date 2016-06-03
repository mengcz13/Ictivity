$("document").ready(function () {

	$("#searchForm").bind("submit", function(e){
    	text = $("#search_input").val();
		text = text.replace(/(^\s*)|(\s*$)/g, "");
		if (text != "")
			window.location.href = "/search?wd=" + text;
    	return false;  
	});
	
	$("#search_input").val(decodeURIComponent(window.location.search.replace("\?wd=","")));
	
	$.post(
		"/api/search",
		{ wd: $("#search_input").val() },
		function(data) {
			data = eval(data);
			if (data.error_code == "200") {
				$("#count_text").text(data.ids.length);
				for (id in data.ids) {
					i = data.ids[id];
					item = '<div class="clearfix" id="item' + i + '"></div>';
					$("#resultView").append(item);
					$.post(
						"/api/activity/ginfo",
						{id : i},
						function(data) {
							data = eval(data);
							if (data.error_code == 200) {
								detail = '<h2><a href="/activity?id=' + data.id + '" hidefocus="true" ';
								detail += 'style="outline: none;">' + data.name + '</a></h2>';
								detail += '<div class="tab-text">';
								detail += '<p style="font-size:14px">' + data.description + '</p>';
								detail += "<div class='tagcloud'>";
								for (j in data.tags)
									detail += "<a href='#'><span>" + data.tags[j] + "</span></a>";
								detail += "</div>";
								detail += '<span> 参与人数：' + data.count + '</span>&nbsp;&nbsp;';
								detail += '<span>';
								if (data.isverify)
									detail += "加入需审核";
								else
									detail += "加入无需审核";
								detail += '</span>';
								detail += '</div>';
								detail += "<hr>";
								$("#item" + data.id).html(detail);
							}
						}
					)
				}
			}
		}
	)
});