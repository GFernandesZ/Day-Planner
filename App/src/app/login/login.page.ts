import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router'; // Importar RouterModule para o Link
import { FormsModule } from '@angular/forms'; // Necessário para [(ngModel)]
import { CommonModule } from '@angular/common'; // Necessário para diretivas como *ngIf, *ngFor
import { LoadingController, ToastController, IonicModule } from '@ionic/angular'; // Importar IonicModule

// Defina a URL base da sua API Django.
const API_BASE_URL = 'http://127.0.0.1:8000'; // Lembre-se de mudar para o IP real do seu PC se for testar em device/emulator

@Component({
    selector: 'app-login',
    templateUrl: './login.page.html',
    styleUrls: ['./login.page.scss'],
    standalone: true,
    imports: [
        IonicModule,
        CommonModule,
        FormsModule,
        RouterModule
    ],
})
export class LoginPage implements OnInit {

    username = '';
    password = '';
    showPassword = false;
    rememberMe = false;

    constructor(
        private router: Router,
        private toastController: ToastController,
        private loadingController: LoadingController
    ) { }

    ngOnInit() {
    }

    async presentToast(message: string, color: string) {
        const toast = await this.toastController.create({
            message,
            duration: 3000,
            color,
            position: 'bottom',
        });
        toast.present();
    }

    async handleLogin() {
        if (!this.username || !this.password) {
            this.presentToast('Por favor, preencha o usuário e a senha.', 'danger');
            return;
        }

        const loading = await this.loadingController.create({
            message: 'Entrando...',
        });
        await loading.present();

        try {
            const response = await fetch(`${API_BASE_URL}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: this.username, password: this.password }),
            });

            const data = await response.json();

            if (response.ok) {
                const token = data.token;
                const userName = data.username;
                localStorage.setItem('authToken', token);
                localStorage.setItem('username', userName);
                this.presentToast(`Bem-vindo, ${userName}!`, 'success');
                this.router.navigateByUrl('/home').then(success => {
                    console.log('Navegação para /home bem-sucedida:', success);
                  });
            } else {
                const errorMessage = data.non_field_errors?.[0] || data.detail || 'Credenciais inválidas.';
                this.presentToast(errorMessage, 'danger');
            }
        } catch (error) {
            console.error('Erro de rede ou servidor:', error);
            this.presentToast('Erro de conexão com o servidor. Tente novamente.', 'danger');
        } finally {
            loading.dismiss();
        }
    }

    togglePasswordVisibility() {
        this.showPassword = !this.showPassword;
    }

    irParaHome() {
        this.router.navigateByUrl('/home');
    }
}