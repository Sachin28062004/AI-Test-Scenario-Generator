import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SettingsService {

  private backendUrl = environment.apiUrl;  // default for local dev

  setBackendUrl(url: string) {
    this.backendUrl = url;
  }

  getBackendUrl(): string {
    return this.backendUrl;
  }
}
