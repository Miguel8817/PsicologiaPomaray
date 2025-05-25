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

    // === 2. Funcionalidad de búsqueda en tablas ===
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            const tables = document.querySelectorAll('table');

            tables.forEach(table => {
                const rows = table.querySelectorAll('tbody tr');
                let hasMatches = false;

                rows.forEach(row => {
                    const text = row.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                        hasMatches = true;
                    } else {
                        row.style.display = 'none';
                    }
                });

                // Mostrar mensaje si no hay resultados
                const noResults = table.querySelector('.no-results');
                if (!noResults && !hasMatches && searchTerm) {
                    const noResultsRow = document.createElement('tr');
                    noResultsRow.className = 'no-results';
                    noResultsRow.innerHTML = `<td colspan="10" style="text-align: center;">No se encontraron resultados</td>`;
                    table.querySelector('tbody').appendChild(noResultsRow);
                } else if (noResults) {
                    noResults.style.display = hasMatches || !searchTerm ? 'none' : '';
                }
            });
        });
    }

    // === 3. Notificaciones ===
    const notificationBell = document.querySelector('.notifications');
    if (notificationBell) {
        notificationBell.addEventListener('click', function (e) {
            e.stopPropagation();
            const dropdown = this.querySelector('.notification-dropdown');
            if (dropdown) {
                dropdown.classList.toggle('show');
                const badge = this.querySelector('.notification-badge');
                if (badge) badge.textContent = '0';
            }
        });

        setInterval(() => {
            const badge = notificationBell.querySelector('.notification-badge');
            if (badge && Math.random() > 0.7) {
                const current = parseInt(badge.textContent) || 0;
                badge.textContent = current + 1;
                badge.classList.add('pulse');
                setTimeout(() => badge.classList.remove('pulse'), 1000);
            }
        }, 30000);
    }

    document.addEventListener('click', function () {
        document.querySelectorAll('.notification-dropdown.show').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    });

    // === 4. Chatbot de IA ===
    const chatbotToggler = document.querySelector('.chatbot-toggler');
    const chatbotContainer = document.querySelector('.chatbot-container');
    const closeChatbot = document.querySelector('.close-chatbot');

    if (chatbotToggler && chatbotContainer) {
        chatbotToggler.addEventListener('click', function () {
            chatbotContainer.classList.toggle('active');
        });

        if (closeChatbot) {
            closeChatbot.addEventListener('click', function () {
                chatbotContainer.classList.remove('active');
            });
        }

        const chatInput = chatbotContainer.querySelector('input');
        const chatSendBtn = chatbotContainer.querySelector('.chatbot-input button');
        const chatMessages = chatbotContainer.querySelector('.chatbot-messages');

        const addMessage = (text, isUser = false) => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
            messageDiv.textContent = text;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        const handleUserMessage = () => {
            const message = chatInput.value.trim();
            if (message) {
                addMessage(message, true);
                chatInput.value = '';

                setTimeout(() => {
                    const responses = [
                        "Entiendo tu consulta sobre psicología. ¿Necesitas ayuda con citas, usuarios o reportes?",
                        "Puedo ayudarte con la gestión del panel. ¿Qué necesitas saber?",
                        "Para programar una cita, ve a la sección correspondiente en el menú.",
                        "Los datos de usuarios se actualizan cada hora automáticamente.",
                        "¿Necesitas generar algún reporte especial?"
                    ];
                    addMessage(responses[Math.floor(Math.random() * responses.length)]);
                }, 1000);
            }
        };

        chatSendBtn.addEventListener('click', handleUserMessage);
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') handleUserMessage();
        });

        addMessage("¡Hola! Soy tu asistente de psicología. ¿En qué puedo ayudarte hoy?");
    }

    // === 5. Actualización de tiempos relativos ===
    function updateRelativeTimes() {
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
    }

    updateRelativeTimes();
    setInterval(updateRelativeTimes, 60000);

    // === 6. Ordenamiento de tablas ===
    document.querySelectorAll('.sortable th').forEach(header => {
        header.addEventListener('click', function () {
            const table = this.closest('table');
            const columnIndex = Array.from(this.parentElement.children).indexOf(this);
            const isAscending = !this.classList.contains('asc');

            table.querySelectorAll('th').forEach(th => th.classList.remove('asc', 'desc'));
            this.classList.add(isAscending ? 'asc' : 'desc');

            sortTable(table, columnIndex, isAscending);
        });
    });

    function sortTable(table, columnIndex, ascending) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr:not(.no-results)'));

        rows.sort((a, b) => {
            const aText = a.children[columnIndex].textContent.trim();
            const bText = b.children[columnIndex].textContent.trim();

            if (!isNaN(aText) && !isNaN(bText)) {
                return ascending ? parseFloat(aText) - parseFloat(bText) : parseFloat(bText) - parseFloat(aText);
            }

            return ascending ? aText.localeCompare(bText) : bText.localeCompare(aText);
        });

        rows.forEach(row => tbody.appendChild(row));
    }

    // === 7. Adaptación de sidebar y sideMenu ===
    const sideMenu = document.querySelector('.side-menu');
    const menuToggle = document.querySelector('.menu-toggle');

    if (menuToggle && sideMenu) {
        menuToggle.addEventListener('click', function () {
            sideMenu.classList.toggle('expanded');
        });

        document.addEventListener('click', function (e) {
            if (!sideMenu.contains(e.target) && e.target !== menuToggle && !menuToggle.contains(e.target)) {
                sideMenu.classList.remove('expanded');
            }
        });
    }

    // Redimensionamiento unificado
    function handleUnifiedResize() {
        if (window.innerWidth >= 768) {
            if (sidebar) sidebar.classList.add('active');
            if (sideMenu) sideMenu.classList.add('expanded');
            if (menuBtn) menuBtn.style.display = 'none';
        } else {
            if (sidebar) sidebar.classList.remove('active');
            if (sideMenu) sideMenu.classList.remove('expanded');
            if (menuBtn) menuBtn.style.display = 'flex';
        }

        if (menuBtn) {
            const icon = menuBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    }

    window.addEventListener('resize', handleUnifiedResize);
    handleUnifiedResize(); // Ejecutar al cargar
});


