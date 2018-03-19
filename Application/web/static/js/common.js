var ____userid = "";
var ____handle = "";
$(document).ready(function () {
  
  loadPopularBlog();

  checkLoggedIn();

  $("body").on("click",".modal-reset", function(){
      $(".validation-label").addClass("invisble");
  });

  $("body").on("click","#loginbtn", function(){
      preLogin();
  });

  $("body").on("click","#registerbtn", function(){
      preRegister();
  });
  
  $("body").on("click","#blog-add-edit-btn", function(){
      preAddBlog($(this).text() == "Edit Blog");
  });

  $("body").on("click","#logoutbtn", function(){
      eraseCookie("USERID");
      eraseCookie("USERHANDLE");
      loggedOutMenu();
      window.location.reload();
  });

  $('#search-blog-input').keyup(function (e) {
    if (e.keyCode === 13)
       window.location.href="/blog/title/"+$("#search-blog-input").val(); 
  });

  $("body").on("click","#search-blog-btn", function(){
      window.location.href="/blog/title/"+$("#search-blog-input").val(); 
  });


});

function loggedInMenu(handle){
    $('.login-opt').hide();
    $('.logout-opt').show();
    $('#handle-name').text(handle);
}

function loggedOutMenu(){
  $('.login-opt').show();
  $('.logout-opt').hide();
  $('#handle-name').text("User");
}

function checkLoggedIn(){
  console.log(readCookie("USERID"));
  if(readCookie("USERID")!=null){
    ____userid = readCookie("USERID");
    ____handle = readCookie("USERHANDLE");
    loggedInMenu(____handle);
  }
  else{
    loggedOutMenu();
    ____userid = "";
    ____handle = "";
  }
}

function resetRegistrationValidationLabel(){
  $('#regi-valid-email').addClass('invisble');
  $('#regi-valid-fname').addClass('invisble');
  $('#regi-valid-lname').addClass('invisble');
  $('#regi-valid-pass').addClass('invisble');
  $('#regi-valid-handle').addClass('invisble');
  $('#regi-valid-gen').addClass('invisble');
  $('#regi-valid-email-exist').addClass('invisble');
}

function preRegister(){
  resetRegistrationValidationLabel();

  email = $('#remail').val();
  fname = $('#rfname').val();
  lname = $('#rlname').val();
  password = $('#rpass').val();
  handle = $('#rhandle').val();
  
  //handle validation

  invalid = false;
  if(!validateEmail(email)){
    $('#regi-valid-email').removeClass('invisble');
    invalid = true;
  }

  if(fname.trim().length<1){
    $('#regi-valid-fname').removeClass('invisble');
    invalid = true;
  }

  if(lname.trim().length<1){
    $('#regi-valid-lname').removeClass('invisble');
    invalid = true;
  }

  if(password.trim().length<1){
    $('#regi-valid-pass').removeClass('invisble');
    invalid = true;
  }

  if(handle.trim().length<1){
    $('#regi-valid-handle').removeClass('invisble');
    invalid = true;
  }

  if(invalid)
    return;

  userObj = {};
  userObj.email = email;
  userObj.first_name = fname;
  userObj.last_name = lname;
  userObj.password = password;
  userObj.handle = handle;

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/register",
    data: JSON.stringify(userObj),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){onRegistration(data);},
    failure: function(errMsg) {
        $('#regi-valid-gen').removeClass('invisble');
    }
  });
}

function onRegistration(data){
    //handle cookie
    isSuccess = (data.registration == 'success');
    if(isSuccess){
        onRegistrationSuccess(data.userid,data.handle);
    }
    else{
      onRegistrationFailure(data.message);
    }
}

function onRegistrationSuccess(userid,handle){
    //handle cookie
    createCookie("USERID", userid,2);
    createCookie("USERHANDLE", handle,2);
    //handle cookie  
    loggedInMenu(handle);
    ____userid = userid;
    ____handle = handle;

    window.location.reload();   
}

function onRegistrationFailure(message){
  console.log(message);
  if(message == "user alread exists")
    $('#regi-valid-email-exist').removeClass('invisble');
  else
    $('#regi-valid-gen').removeClass('invisble');
}

function resetLoginValidationLabel(){
  $('#login-valid-email').addClass('invisble');
  $('#login-valid-pass').addClass('invisble');
  $('#login-valid-gen').addClass('invisble');
}

function preLogin(){
  
  resetLoginValidationLabel();
  email = $('#lemail').val();
  password = $('#lpass').val();
  
  //handle validation
  invalid = false;
  if(!validateEmail(email)){
    $('#login-valid-email').removeClass('invisble');
    invalid = true;
  }

  if(password.trim().length<1){
    $('#login-valid-pass').removeClass('invisble');
    invalid = true;
  }

  if(invalid)
    return;

  userObj = {};
  userObj.email = email;
  userObj.password = password;

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/login",
    data: JSON.stringify(userObj),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){ onLogin(data);},
    failure: function(errMsg) {
        $('#login-valid-gen').removeClass('invisble');
    }
  });

}

function onLogin(data){
    //handle cookie
    isSuccess = (data.login == 'success');
    if(isSuccess){
        onLoginSuccess(data.userid,data.handle);
    }
    else{
      $('#login-valid-pass').removeClass('invisble');
    }
}

function onLoginSuccess(userid,handle){
    //handle cookie
    createCookie("USERID", userid,2);
    createCookie("USERHANDLE", handle,2);

    console.log("at login - "+document.cookie);
    //handle cookie  
    loggedInMenu(handle);

    window.location.reload();  
}

function resetAddBlogFormValidation(){
  $('#batext-valid-title').addClass("invisble");
  $('#batext-valid-tags').addClass('invisble');
  $('#batext-valid-summary').addClass('invisble');
  $('#batext-valid-content').addClass('invisble');
  $('#batext-valid-gen').addClass('invisble');
}

function resetAddBlogFormData(){
  
  $('#batitle').val("");
  $('#batags').val("");
  $('#basummary').val("");
  $('#bacontent').val("");

}

function preAddBlog(isEdit){
  resetAddBlogFormValidation();
  ba_title = $('#batitle').val();
  ba_tags = $('#batags').val();
  ba_summary = $('#basummary').val();
  ba_content = $('#bacontent').val();

  //Validation
  invalid = false;
  if(ba_title.trim().length<1){
    $('#batext-valid-title').removeClass('invisble');
    invalid = true;
  }

  if(ba_tags.trim().length<1){
    $('#batext-valid-tags').removeClass('invisble');
    invalid = true;
  }
  else{
    tempArr = ba_tags.trim().split(",");
    tagArr = [];
    for (var i = 0; i < tempArr.length; i++) {
      if(tempArr[i].trim().length<1){
        $('#batext-valid-tags').removeClass('invisble');
        invalid = true;
        break;
      }
      else
        tagArr.push(tempArr[i].trim());
    }

    ba_tags = tagArr;

  }
  
  if(ba_summary.trim().length<1){
    $('#batext-valid-summary').removeClass('invisble');
    invalid = true;
  }
  
  if(ba_content.trim().length<1){
    $('#batext-valid-content').removeClass('invisble');
    invalid = true;
  }

  if(invalid)
    return;

  blogObj = {};
  blogObj.title = ba_title;
  blogObj.tags = ba_tags;
  blogObj.summary = ba_summary;
  blogObj.content = ba_content;

  if(isEdit){
    requestType = "PUT";
    blogObj.id = singleblogid;
  }
  else
    requestType = "POST";

  $.ajax({
    type: requestType,
    url: "http://localhost:5000/blogpost/"+____userid,
    data: JSON.stringify(blogObj),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(data){onBlogCreate(data);},
    failure: function(errMsg) {
        $('#batext-valid-gen').removeClass('invisble');
    }
  });
  
}

function onBlogCreate(data){
  console.log("Call BAck");
  if(data.BlogPost == 'success'){
      console.log("Sucess");
      resetAddBlogFormData();
      $("#blogAddClose").trigger("click");
      window.location.reload();
  }
  else{
    console.log(data);
    $('#batext-valid-gen').removeClass('invisble');
  }
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours().toString().length==1 ? "0"+a.getHours().toString() : a.getHours().toString();
  var min = a.getMinutes().toString().length==1 ? "0"+a.getMinutes().toString() : a.getMinutes().toString();
  var sec = a.getSeconds().toString().length==1 ? "0"+a.getSeconds().toString() : a.getSeconds().toString();


  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min/* + ':' + sec */;
  return time;
}

function createCookie(name,value,days) {
  if (days) {
    var date = new Date();
    date.setTime(date.getTime()+(days*24*60*60*1000));
    var expires = "; expires="+date.toGMTString();
  }
  else var expires = "";
  document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
    var c = ca[i];
    while (c.charAt(0)==' ') c = c.substring(1,c.length);
    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

function eraseCookie(name) {
  createCookie(name,"",-1);
}

function loadPopularBlog(){
  $.ajax({
    type: "GET",
    url: "http://localhost:5000/blogpost/popular"
  }).done(function(o) {
    dataArr = JSON.parse(o)
    renderPopularBlog(dataArr);
  });
}

function renderPopularBlog(dataArr) {

  popularBlogElement = '<li><a href="/blog/#blogid">#title</a></li>';
  tagElement = $('#tagElementBluePrint').html();
  for(var i=0;i<dataArr.length;i++){
    data = dataArr[i];
    blogid = data._id.$oid;
    title = data.title.substring(0, 30);
    if(data.title>30)
      title = title + " ...";

    $('.link-list').append(popularBlogElement.replace("#blogid",blogid).replace("#title",title));
  }
}

function loadBlog(dataArr) {
  blogElement = $('#blogElementBluePrint').html();
  tagElement = $('#tagElementBluePrint').html();

  if(dataArr.length>0){
    $('#blognotfound').hide();
    uniquetag = [];
    for(var i=0;i<dataArr.length;i++){
      data = dataArr[i];
      blogid = data._id.$oid;
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
      tagElementObj = ''
      for (var j = 0; j < tags.length; j++) {
        tagElementObj = tagElementObj + tagElement.replace("#tag",tags[j]).replace("#place",'/blog/tag/'+tags[j]) + ",";
        if(uniquetag.indexOf(tags[j])<0){
          uniquetag.push(tags[j]);
        }
      }

      blogElementObj = blogElement.replace(
        /#blogid/g,blogid).replace(
        "#title",title).replace(
        "#createdate",createdate).replace(
        "#modifieddate",modifieddate).replace(
        "#author",authorhandle).replace(
        "#like",like).replace(
        "#summary",summary).replace(
        "#dislike",dislike).replace(
        "#comment",commentcount).replace(
        "#tag",tagElementObj.substring(0,tagElementObj.length-1));

      $('#main').append(blogElementObj);
    }

    for(var i=0;i<uniquetag.length;i++){
      $("#tagplace").append('<a href="/blog/tag/'+uniquetag[i]+'">'+uniquetag[i]+'</a>');
    }
  }

}
