import { Component } from '@angular/core';
import {
  TestScenario,
  TestScenarioService,
} from '../../services/test-scenario.service';
import { AuthService } from '../../services/auth.service';
import axios from 'axios';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  title = '';
  description = '';
  scenarios: TestScenario[] = [];
  editingId: number | null = null;
  isGenerating = false;
  errorMessage = '';

  private backendUrl = localStorage.getItem('backendUrl') || 'http://localhost:8000';

  constructor(
    private testScenarioService: TestScenarioService,
    private auth: AuthService
  ) {}

  refreshScenarios(): void {
    this.scenarios = this.testScenarioService.getScenarios();
  }

  async onGenerate(): Promise<void> {
    this.errorMessage = '';

    if (!this.description?.trim()) {
      this.errorMessage = 'Please enter a description.';
      return;
    }

    this.isGenerating = true;

    try {
      const res = await axios.post(
        `${this.backendUrl}/api/ai/generate`,
        { description: this.description, title: this.title },
        { headers: this.auth.getAuthHeader() }
      );
      const data = res.data;
      const backendScenarios = Array.isArray(data?.scenarios) ? data.scenarios : [];

      const formatted = backendScenarios.map((s: any) => ({
        title: s.title || 'Untitled Scenario',
        description: s.type ? `Type: ${s.type}` : '',
        preconditions: s.preconditions || '',
        steps: Array.isArray(s.steps) ? s.steps.join('\n') : (s.steps || ''),
        expectedResult: s.expected_result || '',
      }));

      this.testScenarioService.setScenarios(formatted);
      this.refreshScenarios();
    } catch (err: any) {
      this.errorMessage =
        err?.response?.data?.detail ||
        err?.message ||
        'Failed to generate test scenarios. Please try again.';
    } finally {
      this.isGenerating = false;
    }
  }

  onAddScenario(): void {
    const newScenario = this.testScenarioService.addScenario({
      title: 'New Test Scenario',
      description: 'Describe the scenario...',
    });
    this.refreshScenarios();
    this.editingId = newScenario.id;
  }

  onEditScenario(id: number): void {
    this.editingId = id;
  }

  onDeleteScenario(id: number): void {
    this.testScenarioService.deleteScenario(id);
    this.refreshScenarios();
    if (this.editingId === id) {
      this.editingId = null;
    }
  }

  onSaveScenario(scenario: TestScenario): void {
    this.testScenarioService.updateScenario(scenario.id, scenario);
    this.refreshScenarios();
    this.editingId = null;
  }

  onCancelEdit(): void {
    this.refreshScenarios();
    this.editingId = null;
  }

  onExport(): void {
    if (!this.scenarios.length) {
      this.errorMessage = 'No scenarios to export.';
      return;
    }

    const timestamp = new Date();
    const dateStr = timestamp.toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const fileName = `scenarios-${dateStr}.csv`;

    const csvContent = this.toCsv(this.scenarios);
    this.downloadFile(fileName, csvContent, 'text/csv;charset=utf-8;');

    this.testScenarioService.addHistoryItem({
      fileName,
      sourceId: 'Manual',
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
    return [header, ...rows].map((row) => row.join(',')).join('\n');
  }

  private escapeCsv(value: string): string {
    const shouldQuote = /[",\n]/.test(value);
    let escaped = value.replace(/"/g, '""');
    if (shouldQuote) {
      escaped = `"${escaped}"`;
    }
    return escaped;
  }

  private downloadFile(fileName: string, content: string, mimeType: string): void {
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
