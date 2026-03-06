import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  isLoginMode = true;
  username = '';
  email = '';
  password = '';
  errorMessage = '';
  loading = false;

  constructor(
    private auth: AuthService,
    private router: Router
  ) {
    if (this.auth.isLoggedIn) {
      this.router.navigate(['/home']);
    }
  }

  toggleMode(): void {
    this.isLoginMode = !this.isLoginMode;
    this.errorMessage = '';
  }

  async onSubmit(): Promise<void> {
    this.errorMessage = '';
    this.loading = true;

    try {
      if (this.isLoginMode) {
        const data = await this.auth.login(this.username, this.password);
        this.auth.setToken(data.access_token);
      } else {
        if (!this.email.trim()) {
          this.errorMessage = 'Email is required for registration.';
          this.loading = false;
          return;
        }
        const data = await this.auth.register(this.username, this.email, this.password);
        this.auth.setToken(data.access_token);
      }
      this.router.navigate(['/home']);
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      this.errorMessage = (
        Array.isArray(detail) ? detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ') : detail
      ) || err?.message || 'Request failed';
    } finally {
      this.loading = false;
    }
  }
}
