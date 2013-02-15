//Built using this example: http://benholland.me/javascript/how-to-build-a-site-that-works-like-pinterest/

var colCount = 0;
var colWidth = 250;
var margin = 10;
var spaceLeft = 0;
var windowWidth = 0;
var pins = [];
var vertStart = 100;

$(function(){
	$(window).resize(setupPins);
});

function setupPins() {
	windowWidth = $(window).width();
	pins = [];

	// Calculate the margin so the pins are evenly spaced within the window
	colCount = Math.floor(windowWidth/(colWidth+margin*2));
	spaceLeft = (windowWidth - ((colWidth*colCount)+(margin*(colCount-1)))) / 2;
	console.log(spaceLeft);
	
	for(var i=0;i<colCount;i++){
		pins.push(margin + vertStart);
	}
	positionPins();
}

function positionPins() {
	$('.pin').each(function(i){
		var min = Array.min(pins);
		var index = $.inArray(min, pins);
		var leftPos = margin+(index*(colWidth+margin));
		$(this).css({
			'left':(leftPos+spaceLeft)+'px',
			'top':min+'px'
		});
		pins[index] = min+$(this).outerHeight()+margin;
	});	
}

// Function to get the Min value in Array
Array.min = function(array) {
    return Math.min.apply(Math, array);
};
