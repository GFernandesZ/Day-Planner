document.addEventListener('DOMContentLoaded', function () {
    // Update current date in header
    updateCurrentDate();

    // Generate calendar
    generateCalendar();

    // Add click handlers for menu items
    setupMenuHandlers();

    // Setup sidebar toggle
    setupSidebarToggle();
});

function updateCurrentDate() {
    const now = new Date();
    const options = {
        day: 'numeric',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
    };

    const dateString = now.toLocaleDateString('pt-BR', options);
    document.getElementById('current-date').textContent = dateString;
}

function generateCalendar() {
    const now = new Date();
    const currentDay = now.getDate();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();

    // Update month/year display
    const monthYearOptions = { month: 'long', year: 'numeric' };
    const monthYearString = now.toLocaleDateString('pt-BR', monthYearOptions);
    document.getElementById('month-year').textContent = monthYearString;

    // Calculate calendar data
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

    const calendarDaysContainer = document.getElementById('calendar-days');
    calendarDaysContainer.innerHTML = '';

    // Add empty cells for days before the first day of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day';
        calendarDaysContainer.appendChild(emptyDay);
    }

    // Add all days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day small';
        dayElement.textContent = day;

        if (day === currentDay) {
            dayElement.classList.add('current');
        }

        calendarDaysContainer.appendChild(dayElement);
    }
}


// Initialize task scrolling if needed
setupTaskScrolling();