jQuery(document).ready(function(){
	var didScroll;
	var taille_wnd = $(window).height();
	$("nav").toggle();
	var isHidden = true;
	
	$(window).scroll(function(event){
	    didScroll = true; //perf optimized
	});
	
	setInterval(function() {
	    if (didScroll) {
	        hasScrolled();
	        didScroll = false;
	    }
	}, 250);
	
	function hasScrolled() {
	    var user_position = $(this).scrollTop();
	    if((user_position>taille_wnd && isHidden) || (user_position<=taille_wnd && !isHidden)){
    		$("nav").toggle("slow");
    		isHidden = !isHidden;
	    }
	}
}); 