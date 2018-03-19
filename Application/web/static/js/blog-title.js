var btitle="";
var uniquetag = [];
var currentpage = 1;
var blogLoadCount = 5;
$(window).ready(function () {
	btitle = _title;
	loadData();
	$('#load-more-blog-title').click(function (){
		loadData();
	});
});

function loadData() {
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/blogpost/get/title/"+btitle+"/"+currentpage+"/"+blogLoadCount
	}).done(function(o) {
		dataArr = JSON.parse(o)
		loadBlog(dataArr);
		currentpage = currentpage + 1;
		if(dataArr.length<blogLoadCount)
			$("#load-more-blog-title").addClass("invisible");
	});
}