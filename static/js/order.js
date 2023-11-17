document.addEventListener('DOMContentLoaded', () => {
    "use strict";
    document.querySelectorAll('.btn-optimized').forEach((button) => {
        button.addEventListener('click', function() {
            this.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Optimizando...`;
            this.disabled = true;
        });
    });
});
