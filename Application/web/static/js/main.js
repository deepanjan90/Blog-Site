(function($) { 	

  $('.smoothscroll').on('click', function (e) {
   	e.preventDefault();

   	var target = this.hash,
    	$target = $(target);

    	$('html, body').stop().animate({
       	'scrollTop': $target.offset().top
      }, 800, 'swing', function () {
      	window.location.hash = target;
      });

  }); 
  	
	var pxShow = 300; 
	var fadeInTime = 400; 
	var fadeOutTime = 400; 
	var scrollSpeed = 300; 

	$(window).scroll(function() {

		if ($(window).scrollTop() >= pxShow) {
			$("#go-top").fadeIn(fadeInTime);
		} else {
			$("#go-top").fadeOut(fadeOutTime);
		}

	});  


})(jQuery);