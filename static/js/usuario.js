document.addEventListener('DOMContentLoaded', function () {
    // === 1. Control del menú móvil ===
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.admin-sidebar');

    if (menuBtn && sidebar) {
        menuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.toggle('active');

            const icon = this.querySelector('i');
            icon.classList.toggle('fa-bars');
            icon.classList.toggle('fa-times');
        });

        document.addEventListener('click', function (e) {
            if (window.innerWidth < 768 &&
                !sidebar.contains(e.target) &&
                e.target !== menuBtn &&
                !menuBtn.contains(e.target)) {
                sidebar.classList.remove('active');
                const icon = menuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
});