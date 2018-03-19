var currentpage = 1;
var blogLoadCount = 5;

$(document).ready(function () {
	loadData();

	$('#load-more-blog').click(function (){
		loadData();
	});
});

function loadData() {
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/blogpost/get/"+currentpage+"/"+blogLoadCount
	}).done(function(o) {
		dataArr = JSON.parse(o)
		loadBlog(dataArr);
		currentpage = currentpage + 1;
		if(dataArr.length<blogLoadCount)
			$("#load-more-blog").addClass("invisible");
	});
}

