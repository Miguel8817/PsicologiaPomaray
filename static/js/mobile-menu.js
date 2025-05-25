document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');

    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', function () {
            sidebar.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        if (closeSidebar) {
            closeSidebar.addEventListener('click', function () {
                sidebar.classList.remove('active');
                document.body.style.overflow = '';
            });
        }

        // Cerrar sidebar al hacer clic fuera
        document.addEventListener('click', function (e) {
            if (!sidebar.contains(e.target) && e.target !== mobileMenuBtn) {
                sidebar.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // Ajustar al cambiar tamaño de pantalla
    function handleResize() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    window.addEventListener('resize', handleResize);
});