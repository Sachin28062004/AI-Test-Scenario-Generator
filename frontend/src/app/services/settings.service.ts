import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {

  private backendUrl = 'http://localhost:8000';  // default for local dev

  setBackendUrl(url: string) {
    this.backendUrl = url;
  }

  getBackendUrl(): string {
    return this.backendUrl;
  }
}
