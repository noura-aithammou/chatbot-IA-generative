document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // RTL support for Arabic language
    const currentLang = document.documentElement.lang;
    if (currentLang === 'ar') {
        document.body.setAttribute('dir', 'rtl');
    } else {
        document.body.setAttribute('dir', 'ltr');
    }

    // Language switcher
    const languageSwitchers = document.querySelectorAll('.language-switch');
    languageSwitchers.forEach(switcher => {
        switcher.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.getAttribute('data-lang');
            window.location.href = `/change_language/${lang}`;
        });
    });

    // Image gallery functionality
    const galleryImages = document.querySelectorAll('.gallery-img img');
    if (galleryImages.length > 0) {
        galleryImages.forEach(img => {
            img.addEventListener('click', function() {
                const modal = new bootstrap.Modal(document.getElementById('imageModal'));
                document.getElementById('modalImage').src = this.src;
                modal.show();
            });
        });
    }
});
