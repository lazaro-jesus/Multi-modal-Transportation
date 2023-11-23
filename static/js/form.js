document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('input[type="text"]').forEach(function (input) {
        input.addEventListener('keydown', function (event) {
            const charCode = event.key.charCodeAt(0);
            if (!isSpanishLetter(charCode) && !isSpace(charCode)) {
                event.preventDefault();
            }
        });
    });
});

function isSpanishLetter(charCode) {
    return (charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) ||
           (charCode >= 192 && charCode <= 255);
}

function isSpace(charCode) {
    return charCode === 32;
}
