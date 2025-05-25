document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const body = document.body;

    // Función para abrir el sidebar
    function openSidebar() {
        sidebar.classList.add('active');
        sidebarOverlay.classList.add('active');
        body.style.overflow = 'hidden';
        sidebar.style.transform = 'translateX(0)';
    }

    // Función para cerrar el sidebar
    function closeSidebarFunc() {
        sidebar.style.transform = 'translateX(-100%)';
        sidebarOverlay.classList.remove('active');
        body.style.overflow = '';

        // Remover la clase active después de la transición
        setTimeout(() => {
            sidebar.classList.remove('active');
        }, 300);
    }

    // Abrir sidebar
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            openSidebar();
        });
    }

    // Cerrar sidebar
    if (closeSidebar) {
        closeSidebar.addEventListener('click', closeSidebarFunc);
    }

    // Cerrar al hacer clic en el overlay
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebarFunc);
    }

    // Cerrar al presionar ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebarFunc();
        }
    });

    // Ajustar al cambiar tamaño de pantalla
    function handleResize() {
        if (window.innerWidth > 768) {
            // Resetear estilos en desktop
            sidebar.style.transform = '';
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            body.style.overflow = '';
        }
    }

    window.addEventListener('resize', handleResize);

    // Mejorar el scroll en móviles
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.addEventListener('click', function () {
            if (window.innerWidth <= 768) {
                closeSidebarFunc();
            }
        });
    });
});