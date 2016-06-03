$("document").ready(function () {
	$("#searchForm").bind("submit", function(e){
    	text = $("#search_input").val();
		text = text.replace(/(^\s*)|(\s*$)/g, "");
		if (text != "")
			window.location.href = "/search?wd=" + text;
    	return false;  
	});
});