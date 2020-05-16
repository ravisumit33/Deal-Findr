"use strict";

let getOffset = function() {
    return $('header').outerHeight();
};

let updateOffset = function() {
    let data = $('body').data('bs.scrollspy');
    if(data._config.offset != getOffset()){
        data._config.offset = getOffset();
    }
    $('body').data('bs.scrollspy', data);
    $('body').scrollspy('refresh');
}

let bindScrollSpy = function() {
    $('body').scrollspy({
        target: '.navbar',
        offset: getOffset()
    });
}

$(document).ready(function(){
    initScrollSpy();

    //scroll to just below header
    $("a[href^='#']").click(function(e) {
        e.preventDefault();
        let target = $(this).attr("href");
        let offset = $(target).offset();
        let scrollto = offset.top - $('header').height() + 1; // +1 for nav-link to get highlighted when scrolled
        $('html, body').animate({scrollTop:scrollto}, 500);
    });

});


let initScrollSpy = function() {
    bindScrollSpy();
    $(window).resize(updateOffset); // react on resize event
    $('.alert').on('closed.bs.alert', updateOffset); // react on closing error alert
    $(".collapse").on('shown.bs.collapse', updateOffset); // react on BS4 menu shown event (only on mobile).
    $(".collapse").on('hidden.bs.collapse', updateOffset);
};

