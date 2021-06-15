$(function() {

    // if browser does not support css grid
    if (!Modernizr.cssgrid) {
        // fill last row with empty columns
        var rows = $('.row').filter(function() {
            return $(this).css('column-fill') === 'auto';
        });
        rows.append(new Array(10).join('<div class="col" />'));
    }

});