import { Injectable } from '@angular/core';

export interface TestScenario {
id: number;
title: string;
description: string;
preconditions?: string;
steps?: string;
expectedResult?: string;
}

export interface ExportHistoryItem {
id: number;
fileName: string;
jiraTicketId: string;
createdAt: Date;
scenariosCount: number;
}

@Injectable({
providedIn: 'root',
})
export class TestScenarioService {
private scenarios: TestScenario[] = [];
private history: ExportHistoryItem[] = [];
private nextScenarioId = 1;
private nextHistoryId = 1;

getScenarios(): TestScenario[] {
    return [...this.scenarios];
  }

  setScenarios(scenarios: Partial<TestScenario>[]) {
    this.scenarios = scenarios.map((s) => ({
      id: this.nextScenarioId++,
      title: s.title || '',
      description: s.description || '',
      preconditions: s.preconditions || '',
      steps: s.steps || '',
      expectedResult: s.expectedResult || '',
    }));
  }

  addScenario(scenario: Partial<TestScenario>): TestScenario {
    const newScenario: TestScenario = {
      id: this.nextScenarioId++,
      title: scenario.title || 'New Scenario',
      description: scenario.description || '',
      preconditions: scenario.preconditions || '',
      steps: scenario.steps || '',
      expectedResult: scenario.expectedResult || '',
    };
    this.scenarios.push(newScenario);
    return newScenario;
  }

  updateScenario(id: number, patch: Partial<TestScenario>) {
    const index = this.scenarios.findIndex((s) => s.id === id);
    if (index !== -1) {
      this.scenarios[index] = { ...this.scenarios[index], ...patch };
    }
  }

  deleteScenario(id: number) {
    this.scenarios = this.scenarios.filter((s) => s.id !== id);
  }

  clearScenarios() {
    this.scenarios = [];
  }

  addHistoryItem(item: Omit<ExportHistoryItem, 'id'>): ExportHistoryItem {
    const newItem: ExportHistoryItem = {
      id: this.nextHistoryId++,
      ...item,
    };
    this.history.unshift(newItem);
    return newItem;
  }

  getHistory(): ExportHistoryItem[] {
    return [...this.history];
  }
}
