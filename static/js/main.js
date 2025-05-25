document.addEventListener('DOMContentLoaded', function () {
    // Aquí puedes añadir cualquier funcionalidad adicional
    console.log('Panel de usuario cargado');
});
document.addEventListener('DOMContentLoaded', function () {
    // Elementos del DOM
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationBadge = document.getElementById('notificationBadge');
    const notificationsPanel = document.getElementById('notificationsPanel');
    const closeNotifications = document.getElementById('closeNotifications');
    const notificationsList = document.getElementById('notificationsList');
    const simulateAppointmentBtn = document.getElementById('simulateAppointment');

    // Cargar notificaciones almacenadas
    let notifications = JSON.parse(localStorage.getItem('notifications')) || [];
    let unreadNotifications = notifications.filter(n => !n.read).length;

    // Actualizar badge
    updateBadge();

    // Mostrar notificaciones
    renderNotifications();

    // Abrir panel de notificaciones
    notificationBtn.addEventListener('click', function () {
        notificationsPanel.classList.add('open');
        // Marcar todas como leídas cuando se abre el panel
        markAllAsRead();
    });

    // Cerrar panel de notificaciones
    closeNotifications.addEventListener('click', function () {
        notificationsPanel.classList.remove('open');
        // Eliminar notificaciones leídas
        removeReadNotifications();
    });

    // Simular nueva cita (para prueba)
    simulateAppointmentBtn.addEventListener('click', function () {
        const newAppointment = {
            id: Date.now(),
            type: 'new_appointment',
            title: 'Nueva Cita Programada',
            message: 'Tienes una nueva cita con el Dr. Pérez el ' +
                formatDate(new Date(Date.now() + 86400000 * 3)),
            time: new Date().toISOString(),
            read: false
        };

        addNotification(newAppointment);
    });

    // Función para añadir notificación
    function addNotification(notification) {
        notifications.unshift(notification);
        saveNotifications();
        unreadNotifications++;
        updateBadge();
        renderNotifications();
    }

    // Función para marcar todas como leídas
    function markAllAsRead() {
        if (unreadNotifications === 0) return;

        notifications = notifications.map(n => {
            n.read = true;
            return n;
        });

        unreadNotifications = 0;
        saveNotifications();
        updateBadge();
        renderNotifications();
    }

    // Función para eliminar notificaciones leídas
    function removeReadNotifications() {
        notifications = notifications.filter(n => !n.read);
        saveNotifications();
        renderNotifications();
    }

    // Función para guardar notificaciones en localStorage
    function saveNotifications() {
        localStorage.setItem('notifications', JSON.stringify(notifications));
    }

    // Función para actualizar el badge
    function updateBadge() {
        if (unreadNotifications > 0) {
            notificationBadge.style.display = 'flex';
            notificationBadge.textContent = unreadNotifications;
        } else {
            notificationBadge.style.display = 'none';
        }
    }

    // Función para renderizar notificaciones
    function renderNotifications() {
        if (notifications.length === 0) {
            notificationsList.innerHTML = '<div class="no-notifications">No hay notificaciones</div>';
            return;
        }

        notificationsList.innerHTML = '';

        notifications.forEach(notification => {
            const notificationElement = document.createElement('div');
            notificationElement.className = `notification ${notification.read ? '' : 'unread'}`;
            notificationElement.innerHTML = `
                <div class="notification-title">${notification.title}</div>
                <div class="notification-message">${notification.message}</div>
                <div class="notification-time">${formatTime(notification.time)}</div>
            `;

            notificationElement.addEventListener('click', () => {
                if (!notification.read) {
                    notification.read = true;
                    unreadNotifications--;
                    saveNotifications();
                    updateBadge();
                    notificationElement.classList.remove('unread');
                }
            });

            notificationsList.appendChild(notificationElement);
        });
    }

    // Funciones de formato
    function formatDate(date) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(date).toLocaleDateString('es-ES', options);
    }

    function formatTime(isoString) {
        const date = new Date(isoString);
        return date.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) +
            ' · ' + date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
    }
});