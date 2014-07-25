$("#shelley").hover( handlerIn, handlerOut )


$('#shelley').hover(function() {
    $(this).stop(true).fadeTo("slow", 0.7);
}, function() {
    $(this).stop(true).fadeTo("slow", 1);
});