import { Component, OnInit } from '@angular/core';
import axios from 'axios';

interface JiraSettings {
  jira_token: string;
  jira_email: string;
  jira_domain: string;
  gemini_api_key: string;
}

const SETTINGS_KEY = 'ai-tsg-jira-settings';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
})
export class SettingsComponent {
    backendUrl = localStorage.getItem('backendUrl') || 'http://localhost:8000';
  jiraEmail = '';
  jiraDomain = '';
  jiraApiToken = '';
  geminiApiKey = '';

//   ngOnInit(): void {
//     const raw = localStorage.getItem(SETTINGS_KEY);
//     if (raw) {
//       const settings: JiraSettings = JSON.parse(raw);
//       this.jiraApiToken = settings.jiraApiToken;
//       this.jiraEmail = settings.jiraEmail;
//       this.jiraDomain = settings.jiraDomain;
//       this.geminiApiKey = settings.geminiApiKey;
//
//     }
//   }

  async onSave() {
    const payload: JiraSettings = {
          jira_token: this.jiraApiToken,
          jira_email: this.jiraEmail,
          jira_domain: this.jiraDomain,
          gemini_api_key: this.geminiApiKey
        };
    try {
        const res = await axios.post(`${this.backendUrl}/api/settings/`, payload);
        alert('Settings saved');
        this.jiraApiToken = '';
        this.geminiApiKey = '';
    } catch (err: any) {
        alert('Failed to save settings: ' + (err.response?.data?.detail || err.message));
    }
  }
}
