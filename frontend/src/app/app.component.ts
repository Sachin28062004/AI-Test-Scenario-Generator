import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'AI Test Scenario Generator';

  constructor(
    public auth: AuthService,
    private router: Router
  ) {}

  onLogout(): void {
    this.auth.clearToken();
    this.router.navigate(['/login']);
  }
}