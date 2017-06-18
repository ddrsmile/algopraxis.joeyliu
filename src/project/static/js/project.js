

$(document).ready(function(){
    // hightlight active page
    $(function(){
        var matched = location.pathname.match(/([^/]*\/){2}/);
        var current = matched? matched[0]:location.pathname;
        $('.navbar-table td a').each(function () {
            if ($(this).attr('href') == current) {
                $(this).parent().addClass('td-active');
            }
        });
    })

    $('.navbar-table td a').hover(function () {
        $(this).parent().toggleClass('td-hover');
    });
});