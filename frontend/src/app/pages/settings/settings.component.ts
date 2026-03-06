import { Component } from '@angular/core';
import axios from 'axios';
import { AuthService } from '../../services/auth.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent {
  backendUrl = environment.apiUrl;
  grokApiKey = '';
  errorMessage = '';
  savedMessage = '';

  constructor(private auth: AuthService) {}

  async onSave(): Promise<void> {
    this.errorMessage = '';
    this.savedMessage = '';

    try {
      await axios.post(
        `${this.backendUrl}/api/settings/`,
        { grok_api_key: this.grokApiKey },
        { headers: this.auth.getAuthHeader() }
      );
      this.savedMessage = 'Settings saved.';
      this.grokApiKey = '';
      setTimeout(() => (this.savedMessage = ''), 3000);
    } catch (err: any) {
      this.errorMessage =
        err?.response?.data?.detail || err?.message || 'Failed to save settings';
    }
  }
}
