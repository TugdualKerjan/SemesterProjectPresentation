$('.scroll-top-link').click(function (e) {
    e.preventDefault();
    $('html').animate({scrollTop: 0}, 'slow');
});

// function printWindow() {
//     var w = window.open('', 'printwindow');
//     w.document.write('<head>' + $(document.head).html() + '</head><body>');
//     w.document.write($(document.body).html() + '</body></html>');
//     setTimeout(function () {
//         w.print();
//     }, 1500);
// }


$('.js-print').click(function (e) {
    e.preventDefault();
    // printWindow();
    window.print();
    return false;
});

function beforePrint() {
    $('body').addClass('highContrast');
}
function afterPrint() {
    $('body').removeClass('highContrast');
}

$(document).ready(function() {
    window.addEventListener('beforeprint', beforePrint, false);
    window.addEventListener('afterprint', afterPrint, false);
})