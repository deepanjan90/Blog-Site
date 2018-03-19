var currentpage = 1;
var commentLoadCount = 5;
var blogAuthorid = "";
var singleblogid = "";
var blogTags = [];
$(window).ready(function () {
	
	singleblogid = _blogid;

	loadBlogCall();

	$("body").on("click","#load-more-comment", function(){
		loadComment();
	});

	$("body").on("click","#blog-add-pop", function(){
		addBlogPop();
	});

	$("body").on("click","#edit-blog", function(){
		editBlogPop();
	});

	$("body").on("click","#delete-blog", function(){
		deleteBlog();
	});	

	$("body").on("click",".delete-comment", function(){
		commentauthor = $(this).parent().parent().parent().parent().attr("authorid");
		commentid = $(this).parent().parent().parent().parent().attr("id");
		deleteComment(commentauthor,commentid);      
  	});

	$("body").on("click",".edit-comment", function(){
      commentcontent = $(this).parent().parent().prev().children().text();
      commentauthor = $(this).parent().parent().parent().parent().attr("authorid");
      commentid = $(this).parent().parent().parent().parent().attr("id");
      editCommentPopUp(commentid,commentauthor,commentcontent);
  	});

	$("body").on("click","#commentEditbtn",function(){
  		editCommentSubmit();
  	});

  	$("body").on("click",".delete-comment", function(){
      console.log('awe deli');
  	});

	$('.submit').click(function () {
		addComment();
	});
	
});

function loadBlogCall(){
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/blogpost/single/"+singleblogid
	}).done(function(o) {
		dataArr = JSON.parse(o)
		loadBlogData(dataArr);
	});
}

function addBlogPop(){
	$("#blog-add-edit-title").text("Add Blog");
	$("#blog-add-edit-btn").text("Add Blog");
	$("#batitle").val("");
	$("#basummary").text("");
	$("#batags").val("");
	$("#bacontent").text("");
}

function editBlogPop(){
	$("#blog-add-edit-title").text("Edit Blog");
	$("#blog-add-edit-btn").text("Edit Blog");
	$("#batitle").val($("#title").text());
	$("#basummary").text($("#summary").text());
	$("#batags").val(blogTags.join(","));
	$("#bacontent").text($("#content").text());

	$("#blog-edit-pop").trigger("click");
}

function deleteComment(commentauthor,commentid){
	commentObj = {};
	commentObj.blogid = singleblogid;
	commentObj.commentid = commentid;

	$.ajax({
		type: "DELETE",
		url: "http://localhost:5000/blogpost/comment/"+commentauthor,
		data: JSON.stringify(commentObj),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function(data){onCommentDelete(data,commentid);},
		failure: function(errMsg) {}
	});
}

function deleteBlog(){
	blogObj = {};
	blogObj.id = singleblogid;

	$.ajax({
		type: "DELETE",
		url: "http://localhost:5000/blogpost/"+blogAuthorid,
		data: JSON.stringify(blogObj),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function(data){onBlogDelete(data);},
		failure: function(errMsg) {}
	});
}

function loadBlogData(data) {
	console.log("blog id - "+ singleblogid);
	blogAuthorid = data.author.$oid;
	authorid = data.author.$oid;
	title = data.title
	summary = data.summary;
	createdate = timeConverter(parseInt(data.created.$date));
	modifieddate = timeConverter(parseInt(data.modified.$date));
	like = data.like;
	dislike = data.dislike;
	commentcount = data.commentcount;
	authorhandle = data.authorhandle;
	tags = data.tags;
	blogTags = tags;
	content = data.content;

	$("#title").text(title);
	$("#created").text(createdate);
	$("#authorhandle").text(authorhandle);
	$("#summary").text(summary);
	$("#content").text(content);
	$("#like").text(like);
	$("#dislike").text(dislike);
	$("#commentcount").text(commentcount);

	for(i=0;i<tags.length;i++){
		$("#tagplace").append('<a href="/blog/tag/'+tags[i]+'">'+tags[i]+'</a>');
	}

	loadComment();
}

function loadComment(){
	$.ajax({
		type: "GET",
		url: "http://localhost:5000/blogpost/comment/get/"+singleblogid+"/"+currentpage+"/"+commentLoadCount
	}).done(function(o) {
		dataArr = JSON.parse(o)
		console.log(dataArr);
		loadCommentData(dataArr);
		currentpage = currentpage + 1;
	});
}

function loadCommentData(dataArr) {
	commentElement = $('#commentElementBluePrint').html();

	for (var i = 0; i < dataArr.length; i++) {		
		data = dataArr[i];
		$('.commentlist').append(getCommentElementObj(data));
	}

	if(dataArr.length<commentLoadCount)
		$("#load-more-comment").addClass("invisible");

	handleEditDelete();
}

function handleEditDelete(){
	console.log("inside");
	if(blogAuthorid==____userid)
		console.log("inside");
		$("#edit-delete-blog").removeClass("invisible");
	}

function addComment() {
	if($('#cMessage').val().trim()!=""){
		commentData = {};
		commentData.blogid = singleblogid;
		commentData.content = $('#cMessage').val().trim();

		$.ajax({
		    type: "POST",
		    url: "http://localhost:5000/blogpost/comment/"+____userid,
		    data: JSON.stringify(commentData),
		    contentType: "application/json; charset=utf-8",
		    dataType: "json",
		    success: function(data){addCommentSuccess(JSON.parse(data.comment));},
		    failure: function(errMsg) {
		        alert(errMsg);
		    }
		});
	}
}

function addCommentSuccess(data){
	
	$('.commentlist').append(getCommentElementObj(data));
	$("#commentcount").text(parseInt($('#commentcount').text()) + 1);
	$('#cMessage').val("");

}

function getCommentElementObj(data){
	commentElement = $('#commentElementBluePrint').html();
	
	authorid = data.author.$oid;
	commentid = data._id.$oid;
	author = data.author.$oid;
	content = data.content;
	createdate = timeConverter(parseInt(data.created.$date));
	modifieddate = timeConverter(parseInt(data.modified.$date));
	like = data.like;
	dislike = data.dislike;
	authorhandle = data.authorhandle;

	commentElementObj = commentElement.replace(
			"#commentid",commentid).replace(
			"#authorid",authorid).replace(
			"#createdate",createdate).replace(
			"#modifieddate",modifieddate).replace(
			"#author",authorhandle).replace(
			"#like",like).replace(
			"#content",content).replace(
			"#dislike",dislike);
	
	if(____userid.toString()!="" && authorid.toString()==____userid.toString()){
		commentElementObj = commentElementObj.replace(/none/g,"inline");
	}

	if(createdate==modifieddate){
		commentElementObj = commentElementObj.replace(/#edi/g,"none");
	}
	else{
		commentElementObj = commentElementObj.replace(/#edi/g,"inline");
	}
	

	return commentElementObj;
}

function editCommentPopUp(commentid,commentauthor,commentcontent){
	$("#cetext-valid-comment").addClass("invisible");
	$("#cetext-valid-gen").addClass("invisible");
	$("#comment-edit-author").text(commentauthor);
	$("#comment-edit-id").text(commentid);
	$("#comment-text-area").text(commentcontent);
	$("#comment-text-area").val(commentcontent);
	$("#commentpop").trigger("click");
}

function editCommentSubmit(){
	$("#cetext-valid-comment").addClass("invisible");
	$("#cetext-valid-gen").addClass("invisible");
	commentauthor = $("#comment-edit-author").text();
  	commentcontent = $("#comment-text-area").val();
  	commentid = $("#comment-edit-id").text();

  	if(commentcontent.trim().length<1){
  		$("#cetext-valid-comment").removeClass("invisible");
  		return;
  	}

  	commentObj = {};
  	commentObj.blogid = singleblogid;
  	commentObj.commentid = commentid;
  	commentObj.content = commentcontent;

  	$.ajax({
	    type: "PUT",
	    url: "http://localhost:5000/blogpost/comment/"+commentauthor,
	    data: JSON.stringify(commentObj),
	    contentType: "application/json; charset=utf-8",
	    dataType: "json",
	    success: function(data){onCommentEdit(data,commentid,commentcontent);},
	    failure: function(errMsg) {
	        $('#cetext-valid-gen').removeClass('invisible');
	    }
	});
}

function onCommentEdit(data,commentid,commentcontent){
	if(data.BlogPostComment=='success'){
		$("#"+commentid+" .comment-text p").text(commentcontent);
		$("#"+commentid+" .comment-meta span").next("span:first").css("display","inline");
		$("#"+commentid+" .comment-meta span").next("span:first").next("span:first").css("display","inline").html("Editted: "+timeConverter(JSON.parse(data.comment).modified.$date));


		$("#commentEditClose").trigger('click');
	}
	else{
		$('#cetext-valid-gen').removeClass('invisible');
	}
}

function onCommentDelete(data,commentid){
	if(data.BlogPostComment=='success'){
		$("#"+commentid).remove();
		$("#commentcount").text(parseInt($('#commentcount').text()) - 1);
	}
}

function onBlogDelete(data){
	if(data.BlogPost=='success'){
		window.location.href = "/home";
	}
}