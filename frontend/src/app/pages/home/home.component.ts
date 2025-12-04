import { Component } from '@angular/core';
import { JiraService } from '../../services/jira.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})
export class HomeComponent {
  jiraId = '';
  jiraData: any = null;
  scenarios: any[] = [];
  loading = false;
  error = '';

  constructor(private jira: JiraService) {}

  async fetch() {
    this.error = '';
    this.loading = true;

    try {
      const data = await this.jira.getJiraTicket(this.jiraId);
      this.jiraData = data;

      this.scenarios = [
        {
          id: Date.now(),
          text: 'Sample test scenario will appear here once AI generates it.'
        }
      ];

    } catch (err: any) {
      this.error = err?.message || 'Failed to fetch Jira Ticket';
    } finally {
      this.loading = false;
    }
  }

  addScenario() {
    this.scenarios.push({
      id: Date.now(),
      text: '',
    });
  }

  removeScenario(id: number) {
    this.scenarios = this.scenarios.filter((s) => s.id !== id);
  }

  rewriteScenario(id: number) {
    const item = this.scenarios.find((s) => s.id === id);
    if (!item) return;

    item.text = `Rewritten (AI coming soon): ${item.text}`;
  }
}
