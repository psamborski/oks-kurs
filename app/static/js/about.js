(function($){
  $(function(){

	$('.carousel').carousel({
		fullWidth: true,
		indicators: true
	});
	
	// $('.materialboxed').materialbox({
	// 	onOpenStart: (function(){$('.carousel-item.active').css({ 'z-index': '1000' }); }),
	// 	onCloseEnd: (function(){$('.carousel-item.active').css({ 'z-index': '0' }); }),
	// });
	
	// function for next slide
	$('.op-next').click(function(){
		$('.opinion.carousel').carousel('next');
	});
    
    // function for prev slide
	$('.op-prev').click(function(){
		$('.opinion.carousel').carousel('prev');
	});
	
	// function for next slide
	$('.gal-next').click(function(){
		$('.about-gallery').carousel('next');
	});
    
    // function for prev slide
	$('.gal-prev').click(function(){
		$('.about-gallery').carousel('prev');
	});
	
	carouselHeight();

	$(window).resize(function(){carouselHeight();});
	
  }); // end of document ready
  
  	// height of opinion carousel
	function carouselHeight() {
		let $highest_name = 0;
		let $highest_opinion = 0;
		let $opinion_carousel_item =  $('.opinion-carousel-item');
		// let $check = $opinion_carousel_item.first().height();
		$opinion_carousel_item.each(function() {

			let $name = $(this).find('h2').outerHeight();
			let $opinion = $(this).find('blockquote').outerHeight();

			if ( $name > $highest_name ) {
				$highest_name = $name;
			}
			if ( $opinion > $highest_opinion ) {
				$highest_opinion = $opinion;
			}
		});

		let $new_height = 300 + $highest_name + $highest_opinion;
		$('.opinion.carousel').attr('style', 'min-height: ' + $new_height + 'px !important');
	}
	
})(jQuery); // end of jQuery name space
