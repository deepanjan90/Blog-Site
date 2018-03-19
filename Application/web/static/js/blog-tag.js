var tag="";
var uniquetag = [];
var currentpage = 1;
var blogLoadCount = 5;

$(window).ready(function () {
	tag = _tag;
	loadData();

	$('#load-more-blog-tag').click(function (){
		loadData();
	});
});

function loadData() {
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/blogpost/get/tag/"+tag+"/"+currentpage+"/"+blogLoadCount
	}).done(function(o) {
		dataArr = JSON.parse(o)
		loadBlog(dataArr);
		currentpage = currentpage + 1;
		if(dataArr.length<blogLoadCount){
			$("#load-more-blog-tag").addClass("invisible");
		}
	});
}

