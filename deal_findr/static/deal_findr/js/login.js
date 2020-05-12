"use strict";

//for highlighting of nav-links
$(document).ready(function(){
    $("body").attr("data-offset", $('header').height());
});

//scroll to just below header
$("a[href^='#']").click(function(e) {
    e.preventDefault();
    let target = $(this).attr("href");
    let offset = $(target).offset();
    let scrollto = offset.top - $('header').height() + 1; // +1 for nav-link to get highlighted when scrolled
    $('html, body').animate({scrollTop:scrollto}, 500);
});

