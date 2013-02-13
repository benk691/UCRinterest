//Built using this example: http://benholland.me/javascript/how-to-build-a-site-that-works-like-pinterest/

var colCount = 0;
var colWidth = 250;
var margin = 10;
var spaceLeft = 0;
var windowWidth = 0;
var blocks = [];
var vertStart = 40;

$(function(){
	$(window).resize(setupBlocks);
});

function setupBlocks() {
	windowWidth = $(window).width();
	blocks = [];

	// Calculate the margin so the blocks are evenly spaced within the window
	colCount = Math.floor(windowWidth/(colWidth+margin*2));
	spaceLeft = (windowWidth - ((colWidth*colCount)+(margin*(colCount-1)))) / 2;
	console.log(spaceLeft);
	
	for(var i=0;i<colCount;i++){
		blocks.push(margin + vertStart);
	}
	positionBlocks();
}

function positionBlocks() {
	$('.block').each(function(i){
		var min = Array.min(blocks);
		var index = $.inArray(min, blocks);
		var leftPos = margin+(index*(colWidth+margin));
		$(this).css({
			'left':(leftPos+spaceLeft)+'px',
			'top':min+'px'
		});
		blocks[index] = min+$(this).outerHeight()+margin;
	});	
}

// Function to get the Min value in Array
Array.min = function(array) {
    return Math.min.apply(Math, array);
};
