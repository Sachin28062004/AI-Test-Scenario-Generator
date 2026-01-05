import { Component } from '@angular/core';
import { JiraService } from '../../services/jira.service';
import {
  TestScenario,
  TestScenarioService,
} from '../../services/test-scenario.service';
import axios from 'axios';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  jiraTicketId = '';
  jiraData: any = null;
  scenarios: TestScenario[] = [];
  editingId: number | null = null;
  loading = false;
  isGenerating = false;
  errorMessage = '';
  formattedDescription = '';

  constructor(
      private jira: JiraService,
      private testScenarioService: TestScenarioService
    ) {}


  async fetch() {
      this.errorMessage = '';
      this.loading = true;

      try {
        const data = await this.jira.getJiraTicket(this.jiraTicketId);
        this.jiraData = data;
        this.formattedDescription = this.convertADFToHTML(data.description);

      } catch (err: any) {
        this.errorMessage = err?.message || 'Failed to fetch Jira Ticket';
      } finally {
        this.loading = false;
      }
    }

  convertADFToHTML(adf: any[]): string {
    if (!Array.isArray(adf)) return '';

    let html = '';

    adf.forEach(block => {
      if (block.type === 'paragraph') {
        let paragraphHTML = '';

        block.content?.forEach((item: any) => {
          let text = item.text || '';

          // Apply formatting
          if (item.marks) {
            item.marks.forEach((mark: any) => {
              if (mark.type === 'strong') text = `<strong>${text}</strong>`;
              if (mark.type === 'em') text = `<em>${text}</em>`;
              if (mark.type === 'underline') text = `<u>${text}</u>`;
            });
          }

          paragraphHTML += text;
        });

        html += `<p>${paragraphHTML}</p>`;
      }
    });

    return html;
  }


  refreshScenarios() {
    this.scenarios = this.testScenarioService.getScenarios();
  }

  async onGenerate() {
    this.errorMessage = '';

    if (!this.jiraTicketId.trim()) {
      this.errorMessage = 'Please enter a Jira Ticket ID.';
      return;
    }

    this.isGenerating = true;

    const backendUrl = 'http://localhost:8000';
//     const backendUrl = environment.backendUrl;
    const url = `${backendUrl}/api/ai/generate/${this.jiraTicketId}`;
    const response = await axios.post(url);
    const responseData = response.data;
    const backendScenarios = Array.isArray(responseData?.scenarios)
                ? responseData.scenarios
                : [];

    const formatted = backendScenarios.map((s: any) => ({
                title: s.title || 'Untitled Scenario',
                description: s.type ? `Type: ${s.type}` : '',
                preconditions: s.preconditions || '',
                steps: Array.isArray(s.steps) ? s.steps.join('\n') : (s.steps || ''),
                expectedResult: s.expected_result || '',
            }));

        this.testScenarioService.setScenarios(formatted);

//     this.http.post<any>(url, {}).subscribe({
//       next: (response) => {
        /**
         * Backend returns:
         * {
         *   enhanced_description: "...",
         *   scenarios_count: 5,
         *   export: { filename, filepath, record_id }
         * }
         *
         * Each scenario from Gemini has:
         * {
         *   id, type, title, steps[], expected_result
         * }
         */
         console.log(response)

//         const backendScenarios = Array.isArray(response?.scenarios) ? response.scenarios : [];
//
//         // Convert backend → frontend UI structure
//         const formatted = backendScenarios.map((s: any) => ({
//           title: s.title || 'Untitled Scenario',
//           description: s.type ? `Type: ${s.type}` : '',
//           preconditions: s.preconditions || '',
//           steps: Array.isArray(s.steps) ? s.steps.join('\n') : (s.steps || ''),
//           expectedResult: s.expected_result || '',
//         }));
//
//         this.testScenarioService.setScenarios(formatted);
        this.refreshScenarios();

        this.isGenerating = false;
//       },

      error: (err:any) => {
        this.isGenerating = false;

        this.errorMessage = err?.error?.detail
          || err?.message
          || 'Failed to generate test scenarios. Please try again.';
      }
//     });
  }


  onAddScenario() {
    const newScenario = this.testScenarioService.addScenario({
      title: 'New Test Scenario',
      description: 'Describe the scenario...',
    });
    this.refreshScenarios();
    this.editingId = newScenario.id;
  }

  onEditScenario(id: number) {
    this.editingId = id;
  }

  onDeleteScenario(id: number) {
    this.testScenarioService.deleteScenario(id);
    this.refreshScenarios();
    if (this.editingId === id) {
      this.editingId = null;
    }
  }

  onSaveScenario(scenario: TestScenario) {
    this.testScenarioService.updateScenario(scenario.id, scenario);
    this.refreshScenarios();
    this.editingId = null;
  }

  onCancelEdit() {
    this.refreshScenarios();
    this.editingId = null;
  }

  // Export as CSV and add to history
  onExport() {
    if (!this.scenarios.length) {
      this.errorMessage = 'No scenarios to export.';
      return;
    }

    const timestamp = new Date();
    const dateStr = timestamp
      .toISOString()
      .replace(/[:.]/g, '-')
      .slice(0, 19);
    const safeTicketId = this.jiraTicketId || 'no-ticket';
    const fileName = `${safeTicketId}-test-scenarios-${dateStr}.csv`;

    const csvContent = this.toCsv(this.scenarios);
    this.downloadFile(fileName, csvContent, 'text/csv;charset=utf-8;');

    this.testScenarioService.addHistoryItem({
      fileName,
      jiraTicketId: this.jiraTicketId || 'N/A',
      createdAt: timestamp,
      scenariosCount: this.scenarios.length,
    });
  }

  private toCsv(scenarios: TestScenario[]): string {
    const header = [
      'ID',
      'Title',
      'Description',
      'Preconditions',
      'Steps',
      'Expected Result',
    ];
    const rows = scenarios.map((s) => [
      s.id,
      this.escapeCsv(s.title),
      this.escapeCsv(s.description),
      this.escapeCsv(s.preconditions || ''),
      this.escapeCsv(s.steps || ''),
      this.escapeCsv(s.expectedResult || ''),
    ]);
    return [header, ...rows]
      .map((row) => row.join(','))
      .join('\n');
  }

  private escapeCsv(value: string): string {
    const shouldQuote = /[",\n]/.test(value);
    let escaped = value.replace(/"/g, '""');
    if (shouldQuote) {
      escaped = `"${escaped}"`;
    }
    return escaped;
  }

  private downloadFile(fileName: string, content: string, mimeType: string) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}
