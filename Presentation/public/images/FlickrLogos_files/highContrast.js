var HIGH_CONTRAST_STORAGE_KEY = 'enableHighContrast';

function restoreHighContrast() {
    var setting = localStorage.getItem(HIGH_CONTRAST_STORAGE_KEY);

    if (setting === "true") {
        document.body.classList.add('highContrast');
    }
}

restoreHighContrast();

// add click event for high contrast toggles
document.addEventListener("DOMContentLoaded", function(event) {
    var highContrastToggles = document.querySelectorAll('.js-toggleHighContrast');

    for (var i = 0; i < highContrastToggles.length; i++) {
        highContrastToggles[i].addEventListener('click', function(e) {
            e.preventDefault();
            document.body.classList.toggle('highContrast');
            localStorage.setItem(HIGH_CONTRAST_STORAGE_KEY, document.body.classList.contains('highContrast'));
        });
    }
});
