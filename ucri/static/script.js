$(document).ready(function(){
	$('.main_container').masonry({
		itemSelector: '.pin',
		isAnimated: true,
		isFitWidth: true
	});

	$('.comment_tr').click(function () {
		$(this).toggleClass('disabled');
		$(this).parent().parent().parent().find('.comment').slideToggle(250, function () {
			$('.main_container').masonry();
		});
	});

	$(".ajax").colorbox({
		onComplete:function(){
			$(this).colorbox.resize();
		}
	});
});

$(window).load(function(){
	$('.main_container').masonry({
		itemSelector: '.pin',
		isAnimated: true,
		isFitWidth: true
	});
});