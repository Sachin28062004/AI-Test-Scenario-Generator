import { Injectable } from '@angular/core';
import axios from 'axios';

const TOKEN_KEY = 'ai-tsg-jwt-token';
const BACKEND_URL = localStorage.getItem('backendUrl') || 'http://localhost:8000';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private _token: string | null = null;

  constructor() {
    this._token = localStorage.getItem(TOKEN_KEY);
  }

  get token(): string | null {
    return this._token;
  }

  get isLoggedIn(): boolean {
    return !!this._token;
  }

  setToken(token: string): void {
    this._token = token;
    localStorage.setItem(TOKEN_KEY, token);
  }

  clearToken(): void {
    this._token = null;
    localStorage.removeItem(TOKEN_KEY);
  }

  getAuthHeader(): Record<string, string> {
    if (!this._token) return {};
    return { Authorization: `Bearer ${this._token}` };
  }

  async login(username: string, password: string): Promise<{ access_token: string }> {
    const res = await axios.post(`${BACKEND_URL}/api/auth/login`, { username, password });
    return res.data;
  }

  async register(username: string, email: string, password: string): Promise<{ access_token: string }> {
    const res = await axios.post(`${BACKEND_URL}/api/auth/register`, {
      username,
      email,
      password,
    });
    return res.data;
  }

  async getMe(): Promise<{ username: string; email: string }> {
    const res = await axios.get(`${BACKEND_URL}/api/auth/me`, {
      headers: this.getAuthHeader(),
    });
    return res.data;
  }
}
