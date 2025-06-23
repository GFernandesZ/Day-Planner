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

function setupMenuHandlers() {
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.addEventListener('click', function () {
            // Remove active class from all items
            menuItems.forEach(mi => mi.classList.remove('active'));

            // Add active class to clicked item
            this.classList.add('active');
        });
    });
}

function setupSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');

    if (sidebarToggle && sidebar && mainContent) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('hidden');
            mainContent.classList.toggle('sidebar-hidden');
        });
    }
}

// Optional: Add smooth scrolling for task cards
function setupTaskScrolling() {
    const taskContainer = document.querySelector('.task-cards-container');
    const arrowBtn = document.querySelector('.arrow-btn');

    if (arrowBtn && taskContainer) {
        arrowBtn.addEventListener('click', function () {
            taskContainer.scrollBy({
                left: 250,
                behavior: 'smooth'
            });
        });
    }
}
function deleteNote() {
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

function confirmDelete() {
    // Aqui você implementaria a lógica de exclusão
    alert('Anotação excluída com sucesso!');
    window.location.href = 'notes.html';
}

function deleteTask() {
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

function confirmDelete() {
    // Aqui você implementaria a lógica de exclusão
    alert('Tarefa excluída com sucesso!');
    window.location.href = 'tasks.html';
}

// Initialize task scrolling if needed
setupTaskScrolling();

document.addEventListener('DOMContentLoaded', function () {
    // ... (Suas funções existentes: updateCurrentDate, generateCalendar, setupMenuHandlers, setupSidebarToggle) ...

    // NOVO: Inicializar o Carrossel de Tarefas da Home
    setupHomeTaskCarousel();
});

// ... (Suas funções existentes) ...

function setupHomeTaskCarousel() {
    const carouselContainer = document.querySelector('.home-task-carousel-container');
    if (!carouselContainer) return;

    const carouselTrack = carouselContainer.querySelector('.home-task-carousel-track');
    const slides = carouselContainer.querySelectorAll('.home-task-carousel-slide');
    const prevArrow = carouselContainer.querySelector('.prev-arrow');
    const nextArrow = carouselContainer.querySelector('.next-arrow');

    if (!carouselTrack || slides.length === 0 || !prevArrow || !nextArrow) return;

    let currentIndex = 0;
    // Determine o número de slides visíveis baseado na largura da tela e do slide
    // É mais robusto ler o valor computado pelo CSS.
    function getSlidesPerView() {
        // Obter a largura total do wrapper (área visível do carrossel)
        const wrapperWidth = carouselContainer.querySelector('.home-task-carousel-wrapper').offsetWidth;
        if (slides.length === 0) return 1;

        // Obter a largura de um slide, incluindo a margem
        const slideWidthWithMargin = slides[0].offsetWidth + (parseFloat(window.getComputedStyle(slides[0]).marginRight) || 0);

        if (slideWidthWithMargin === 0) return 1; // Evitar divisão por zero

        // Calcula quantos slides cabem (arredonda para baixo)
        return Math.floor(wrapperWidth / slideWidthWithMargin);
    }

    const scrollStep = 2; // Rolar 2 slides por clique, como solicitado.

    // Oculta setas se não houver rolagem necessária
    function updateArrowVisibility() {
        const currentSlidesPerView = getSlidesPerView();

        if (slides.length <= currentSlidesPerView) {
            prevArrow.style.display = 'none';
            nextArrow.style.display = 'none';
        } else {
            prevArrow.style.display = 'block';
            nextArrow.style.display = 'block';
        }

        // Desabilita setas no início/fim
        prevArrow.disabled = currentIndex === 0;
        // nextArrow.disabled = currentIndex >= slides.length - currentSlidesPerView;
        // Correção para o nextArrow, precisa permitir rolar até que o último item esteja visível
        // Se a rolagem é de 2 em 2, o último clique pode não levar ao final exato da lista
        nextArrow.disabled = currentIndex + currentSlidesPerView >= slides.length;
    }

    function slideCarousel() {
        const currentSlidesPerView = getSlidesPerView();
        if (slides.length === 0 || currentSlidesPerView === 0) return;

        const slideWidthWithMargin = slides[0].offsetWidth + (parseFloat(window.getComputedStyle(slides[0]).marginRight) || 0);

        // Ajusta a posição do carrossel para mostrar o currentIndex
        // Multiplica pelo currentIndex para deslizar para a posição correta
        carouselTrack.style.transform = `translateX(-${currentIndex * slideWidthWithMargin}px)`;
        updateArrowVisibility();
    }

    prevArrow.addEventListener('click', () => {
        currentIndex = Math.max(0, currentIndex - scrollStep);
        slideCarousel();
    });

    nextArrow.addEventListener('click', () => {
        const currentSlidesPerView = getSlidesPerView();
        // Garante que não rolamos além do final da lista de slides
        currentIndex = Math.min(slides.length - currentSlidesPerView, currentIndex + scrollStep);
        slideCarousel();
    });

    // Inicializar carrossel ao carregar e ao redimensionar a janela
    slideCarousel();
    window.addEventListener('resize', slideCarousel); // Reajustar ao redimensionar
}