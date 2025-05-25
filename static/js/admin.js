document.addEventListener('DOMContentLoaded', function () {
    // --------------------------
    // 1. FUNCIONALIDAD DE BÚSQUEDA
    // --------------------------
    const initSearch = () => {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;

        searchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.trim().toLowerCase();
            const tables = document.querySelectorAll('.searchable-table');

            tables.forEach(table => {
                const rows = table.querySelectorAll('tbody tr');
                let hasMatches = false;
                const noResultsRow = table.querySelector('.no-results');

                rows.forEach(row => {
                    if (row.classList.contains('no-results')) return;

                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                        hasMatches = true;
                    } else {
                        row.style.display = 'none';
                    }
                });

                // Mostrar mensaje si no hay coincidencias
                if (noResultsRow) {
                    noResultsRow.style.display = hasMatches || searchTerm === '' ? 'none' : 'table-row';
                }
            });
        });
    };

    // --------------------------
    // 2. ACTUALIZACIÓN DE TIEMPOS
    // --------------------------
    const updateRelativeTimes = () => {
        const timeElements = document.querySelectorAll('[data-time]');
        const now = new Date();

        timeElements.forEach(el => {
            const timestamp = new Date(el.getAttribute('data-time'));
            const seconds = Math.floor((now - timestamp) / 1000);

            let interval = Math.floor(seconds / 31536000);
            if (interval >= 1) {
                el.textContent = `hace ${interval} año${interval > 1 ? 's' : ''}`;
                return;
            }

            interval = Math.floor(seconds / 2592000);
            if (interval >= 1) {
                el.textContent = `hace ${interval} mes${interval > 1 ? 'es' : ''}`;
                return;
            }

            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                el.textContent = `hace ${interval} día${interval > 1 ? 's' : ''}`;
                return;
            }

            interval = Math.floor(seconds / 3600);
            if (interval >= 1) {
                el.textContent = `hace ${interval} hora${interval > 1 ? 's' : ''}`;
                return;
            }

            interval = Math.floor(seconds / 60);
            if (interval >= 1) {
                el.textContent = `hace ${interval} minuto${interval > 1 ? 's' : ''}`;
                return;
            }

            el.textContent = `hace unos segundos`;
        });
    };

    // --------------------------
    // 3. NOTIFICACIONES EN TIEMPO REAL
    // --------------------------
    const initNotifications = () => {
        const notificationBell = document.querySelector('.notifications');
        if (!notificationBell) return;

        // Simular notificaciones (en producción sería con WebSockets)
        setInterval(() => {
            const badge = notificationBell.querySelector('.notification-badge');
            if (badge) {
                const currentCount = parseInt(badge.textContent) || 0;
                if (Math.random() > 0.7 && currentCount < 9) {
                    badge.textContent = currentCount + 1;
                    badge.classList.add('pulse');
                    setTimeout(() => badge.classList.remove('pulse'), 1000);
                }
            }
        }, 30000); // Cada 30 segundos

        // Mostrar/ocultar dropdown de notificaciones
        notificationBell.addEventListener('click', function (e) {
            e.stopPropagation();
            const dropdown = this.querySelector('.notification-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('show');

                // Marcar como leídas
                const badge = this.querySelector('.notification-badge');
                if (badge) badge.textContent = '0';
            }
        });

        // Cerrar dropdown al hacer clic fuera
        document.addEventListener('click', function () {
            const dropdowns = document.querySelectorAll('.notification-dropdown');
            dropdowns.forEach(dropdown => dropdown.classList.remove('show'));
        });
    };

    // --------------------------
    // 4. INTERACCIONES CON TABLAS
    // --------------------------
    const initTableInteractions = () => {
        // Ordenamiento de columnas
        document.querySelectorAll('.sortable th').forEach(header => {
            header.addEventListener('click', function () {
                const table = this.closest('table');
                const columnIndex = Array.from(this.parentElement.children).indexOf(this);
                const isAscending = !this.classList.contains('asc');

                // Resetear otros headers
                table.querySelectorAll('th').forEach(th => {
                    th.classList.remove('asc', 'desc');
                });

                // Aplicar clase al header actual
                this.classList.add(isAscending ? 'asc' : 'desc');

                // Ordenar la tabla
                sortTable(table, columnIndex, isAscending);
            });
        });

        // Paginación
        document.querySelectorAll('.pagination a').forEach(link => {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                // Implementar lógica de paginación aquí
                console.log('Cambiar a página:', this.textContent);
            });
        });
    };

    // Función auxiliar para ordenar tablas
    const sortTable = (table, columnIndex, ascending) => {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr:not(.no-results)'));

        rows.sort((a, b) => {
            const aText = a.children[columnIndex].textContent.trim();
            const bText = b.children[columnIndex].textContent.trim();

            // Intenta comparar como números si es posible
            if (!isNaN(aText) && !isNaN(bText)) {
                return ascending ?
                    parseFloat(aText) - parseFloat(bText) :
                    parseFloat(bText) - parseFloat(aText);
            }

            // Comparación de texto
            return ascending ?
                aText.localeCompare(bText) :
                bText.localeCompare(aText);
        });

        // Reinsertar filas ordenadas
        rows.forEach(row => tbody.appendChild(row));
    };

    // --------------------------
    // 5. INICIALIZACIÓN DE COMPONENTES
    // --------------------------
    const initComponents = () => {
        // Tooltips
        tippy('[data-tippy-content]', {
            arrow: true,
            animation: 'fade'
        });

        // Modales
        document.querySelectorAll('[data-modal]').forEach(trigger => {
            trigger.addEventListener('click', function () {
                const modalId = this.getAttribute('data-modal');
                const modal = document.getElementById(modalId);
                if (modal) modal.classList.add('show');
            });
        });

        // Cerrar modales
        document.querySelectorAll('.modal .close').forEach(closeBtn => {
            closeBtn.addEventListener('click', function () {
                this.closest('.modal').classList.remove('show');
            });
        });

        // Cerrar modales al hacer clic fuera
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function (e) {
                if (e.target === this) this.classList.remove('show');
            });
        });
    };

    // --------------------------
    // INICIALIZAR TODAS LAS FUNCIONALIDADES
    // --------------------------
    initSearch();
    updateRelativeTimes();
    initNotifications();
    initTableInteractions();
    initComponents();

    // Actualizar tiempos cada minuto
    setInterval(updateRelativeTimes, 60000);
});