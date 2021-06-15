function initImageSlider() {
    $('.imageSlider').not('.slick-initialized').slick({
        dots: true,
        arrows: true,
        prevArrow: '<div class="slick-prev"><span class="icon-arrow-left-slider"></span></div>',
        nextArrow: '<div class="slick-next"><span class="icon-arrow-right-slider"></span></div>',
        infinite: true,
        autoplay: true,
        autoplaySpeed: 8000,
        speed: 1000
    });
}
