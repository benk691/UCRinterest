$(document).ready(function(){
	$('.main_container').masonry({
		itemSelector: '.pin',
		isAnimated: true,
		isFitWidth: true
	});

	$('.comment_tr').click(function () {
		$(this).toggleClass('disabled');
		$(this).parent().parent().parent().find('form').slideToggle(250, function () {
			$('.main_container').masonry();
		});
	});

	$(".ajax").colorbox({
		onComplete:function(){
			$(this).colorbox.resize();
		}
	});
});
