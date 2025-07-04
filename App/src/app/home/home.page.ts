import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingController, ToastController, IonicModule } from '@ionic/angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { TaskItem, NoteItem, DateItem, MONTH_COLORS, DAILY_QUOTES } from '../interfaces/app-models';
import { arrowForward, arrowBack } from 'ionicons/icons';
import { addIcons } from 'ionicons';


const API_BASE_URL = 'http://127.0.0.1:8000';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule],
})
export class HomePage implements OnInit {
  currentDate = '';
  userName = 'Usuário';
  userInitials = 'U';

  processedHomeTasks: { task_obj: TaskItem; items_for_display: string[]; get_box_color_class: string }[] = [];
  allNotes: NoteItem[] = [];
  comemorativasHome: { obj: DateItem; month_color_class: string }[] = [];
  importantesGeralHome: DateItem[] = [];
  dailyQuoteText = '';
  monthYearDisplay = '';

  constructor(
    private http: HttpClient,
    private router: Router,
    private loadingController: LoadingController,
    private toastController: ToastController
  )
  
  { 


    addIcons({ arrowForward, arrowBack });
  }

  ngOnInit() {
    this.updateHeaderInfo();
    this.fetchData();
    this.getDailyQuote();
    this.setupHomeTaskCarousel();
  }
  
  updateHeaderInfo() {
    const now = new Date();
    this.currentDate = now.toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', hour: '2-digit', minute: '2-digit' });
    this.userName = localStorage.getItem('username') || 'Usuário';
    this.userInitials = this.userName[0]?.toUpperCase() || 'U';
  }

  getDailyQuote() {
    const day = new Date().getDate();
    this.dailyQuoteText = DAILY_QUOTES[(day - 1) % DAILY_QUOTES.length];
  }

  async fetchData() {
    const loading = await this.loadingController.create({ message: 'Carregando dados...' });
    await loading.present();

    const authToken = localStorage.getItem('authToken');
    if (!authToken) {
      this.presentToast('Você não está autenticado. Por favor, faça login.', 'danger');
      this.router.navigateByUrl('/login');
      loading.dismiss();
      return;
    }

    const headers = new HttpHeaders({ Authorization: `Token ${authToken}` });

    try {
      const tasks = await firstValueFrom(this.http.get<TaskItem[]>(`${API_BASE_URL}/Agenda/api/tasks/`, { headers }));
      this.processedHomeTasks = tasks.map(task => {
        const itemsForDisplay: string[] = [];
        for (let i = 1; i <= 9; i++) {
          const itemText = (task as any)[`item${i}_text`];
          if (itemText) itemsForDisplay.push(itemText);
        }
        return {
          task_obj: task,
          items_for_display: task.items_list_display || [],
          get_box_color_class: this.getTaskBoxColorClass(task.priority),
        };
      });

      const notes = await firstValueFrom(this.http.get<NoteItem[]>(`${API_BASE_URL}/Agenda/api/notes/`, { headers }));
      this.allNotes = notes;

      const dates = await firstValueFrom(this.http.get<DateItem[]>(`${API_BASE_URL}/Agenda/api/dates/`, { headers }));
      const today = new Date();
      const month = today.getMonth() + 1;
      const year = today.getFullYear();

      this.comemorativasHome = dates
        .filter(d => d.type === 'comemorativa' && d.is_fixed && new Date(d.date).getMonth() + 1 === month && new Date(d.date).getFullYear() === year)
        .map(d => ({ obj: d, month_color_class: MONTH_COLORS[new Date(d.date).getMonth() + 1] || 'bg-secondary' }));

      this.importantesGeralHome = dates.filter(d => d.type === 'importante').slice(0, 5);

    } catch (error: any) {
      console.error('Erro ao buscar dados:', error);
      const msg = (error.status === 401 || error.status === 403)
        ? 'Sessão expirada ou não autorizado. Por favor, faça login novamente.'
        : 'Erro ao carregar dados. Tente novamente mais tarde.';
      this.presentToast(msg, 'danger');
      if (error.status === 401 || error.status === 403) this.router.navigateByUrl('/login');
    } finally {
      loading.dismiss();
    }
  }

  getTaskBoxColorClass(priority: 'low' | 'medium' | 'high' | 'urgent'): string {
    const TASK_BOX_COLOR_MAP = {
      low: 'task-box-color-low',
      medium: 'task-box-color-medium',
      high: 'task-box-color-high',
      urgent: 'task-box-color-urgent',
    };
    return TASK_BOX_COLOR_MAP[priority] || 'task-box-color-medium';
  }

  async presentToast(message: string, color: string = 'primary') {
    const toast = await this.toastController.create({
      message,
      duration: 3000,
      color,
    });
    toast.present();
  }

  navigateTo(path: string) {
    this.router.navigateByUrl(path);
  }

  setupHomeTaskCarousel() {
    const container = document.querySelector('.home-task-carousel-container') as HTMLElement | null;
    if (!container) return;

    const track = container.querySelector('.home-task-carousel-track') as HTMLElement | null;
    const prevArrow = container.querySelector('.carousel-arrow.prev-arrow') as HTMLButtonElement | null;
    const nextArrow = container.querySelector('.carousel-arrow.next-arrow') as HTMLButtonElement | null;
    const wrapper = container.querySelector('.home-task-carousel-wrapper') as HTMLElement | null;

    if (!track || !prevArrow || !nextArrow || !wrapper) return;

    let currentIndex = 0;
    const scrollStep = 2;

    const updateArrowVisibility = () => {
      const slides = container.querySelectorAll('.home-task-carousel-slide');
      if (!slides.length) {
        prevArrow.style.display = 'none';
        nextArrow.style.display = 'none';
        return;
      }

      const slideWidth = slides[0].clientWidth + (parseFloat(getComputedStyle(slides[0] as HTMLElement).marginRight) || 0);
      const slidesPerView = Math.floor(wrapper.clientWidth / slideWidth);

      prevArrow.disabled = currentIndex === 0;
      nextArrow.disabled = currentIndex + slidesPerView >= slides.length;
    };

    const slideCarousel = () => {
      const slides = container.querySelectorAll('.home-task-carousel-slide');
      if (!slides.length) return;

      const slideWidth = slides[0].clientWidth + (parseFloat(getComputedStyle(slides[0] as HTMLElement).marginRight) || 0);
      track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
      updateArrowVisibility();
    };

    prevArrow.addEventListener('click', () => {
      currentIndex = Math.max(0, currentIndex - scrollStep);
      slideCarousel();
    });

    nextArrow.addEventListener('click', () => {
      const slides = container.querySelectorAll('.home-task-carousel-slide');
      const slideWidth = slides[0].clientWidth + (parseFloat(getComputedStyle(slides[0] as HTMLElement).marginRight) || 0);
      const slidesPerView = Math.floor(wrapper.clientWidth / slideWidth);
      currentIndex = Math.min(slides.length - slidesPerView, currentIndex + scrollStep);
      slideCarousel();
    });

    setTimeout(() => {
      slideCarousel();
      window.addEventListener('resize', slideCarousel);
    }, 500);
  }
  toggleSidebar() {
    const menu = document.querySelector('ion-menu');
    if (menu) {
      (menu as any).open();
    }
  }
  async deleteNote(noteId: number) {
    const confirm = window.confirm('Tem certeza que deseja deletar esta anotação?');
    if (!confirm) return;

    const authToken = localStorage.getItem('authToken');
    const headers = new HttpHeaders({ Authorization: `Token ${authToken}` });

    try {
      await firstValueFrom(this.http.delete(`${API_BASE_URL}/Agenda/api/notes/delete/${noteId}/`, { headers }));
      this.presentToast('Anotação deletada com sucesso!', 'success');
      this.allNotes = this.allNotes.filter(note => note.id !== noteId); // remove da UI
    } catch (error) {
      console.error('Erro ao deletar anotação:', error);
      this.presentToast('Erro ao deletar. Tente novamente.', 'danger');
    }
  }
}



