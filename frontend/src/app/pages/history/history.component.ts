import { Component, OnInit } from '@angular/core';
import {
  ExportHistoryItem,
  TestScenarioService,
} from '../../services/test-scenario.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss'],
})
export class HistoryComponent implements OnInit {
  history: ExportHistoryItem[] = [];

  constructor(private testScenarioService: TestScenarioService) {}

  ngOnInit(): void {
    this.history = this.testScenarioService.getHistory();
  }

  formatDate(d: Date): string {
    return new Date(d).toLocaleString();
  }
}
