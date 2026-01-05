import { Injectable } from '@angular/core';
import axios from 'axios';
import { SettingsService } from './settings.service';

@Injectable({
  providedIn: 'root'
})
export class JiraService {

  constructor(private settings: SettingsService) {}

  async getJiraTicket(jiraId: string): Promise<any> {
    const backendUrl = this.settings.getBackendUrl();

    if (!jiraId || jiraId.trim().length === 0) {
      throw new Error('Jira ID cannot be empty');
    }

    try {
      const response = await axios.get(`${backendUrl}/api/jira/${jiraId}`);
      console.log(response)
      return response.data;
    } catch (error: any) {
      console.error('Jira Fetch Error:', error);
      throw new Error(error?.response?.data?.detail || 'Failed to fetch Jira Ticket');
    }
  }
}
