(function($){
  $(function(){

    $('.parallax').parallax();
	
	$('.carousel').carousel({
		fullWidth: true,
		indicators: true
	});

	$(document).ready(function(){
		$('.modal').modal();
		$('.modal').modal('open');
	});
	
	// function for next slide
	$('.carousel-next').click(function(){
		$('.carousel').carousel('next');
	});
    
    // function for prev slide
	$('.carousel-prev').click(function(){
		$('.carousel').carousel('prev');
	});
	
	carouselHeight();

	$(window).resize(function(){carouselHeight();});
	
  }); // end of document ready
  
  	// height of carousel
	function carouselHeight() {
		var $highest_name = 0;
		var $highest_opinion = 0;
		$check = $('.carousel-item').first().height();
		$('.opinion-carousel-item').each(function() {
			
			$name = $(this).find('h2').outerHeight();
			$opinion = $(this).find('blockquote').outerHeight();

			if ( $name > $highest_name ) {
				$highest_name = $name;
			}
			if ( $opinion > $highest_opinion ) {
				$highest_opinion = $opinion;
			}
		});

		var $new_height = 300 + $highest_name + $highest_opinion;
		$('.opinion.carousel').attr('style', 'min-height: ' + $new_height + 'px !important');
	}
})(jQuery); // end of jQuery name space
	