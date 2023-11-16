document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    document.querySelector('.btn-optimized').addEventListener('click', function() {
        let button = this;
        button.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        Optimizando...`;
        button.disabled = true;
    });
});