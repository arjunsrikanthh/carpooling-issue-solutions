import { expect } from 'vitest';
import {createHash} from 'node:crypto';
import {existsSync} from 'node:fs';
if(existsSync('.env'))process.loadEnvFile('.env');

try { process.loadEnvFile?.('.env'); } catch { /* caller-provided environment remains authoritative */ }

const configuredBaseUrl = process.env.CP_BASE_URL?.trim() ?? process.env.BASE_URL?.trim();
export const BASE_URL = (configuredBaseUrl && /^https?:\/\//i.test(configuredBaseUrl)
  ? configuredBaseUrl : 'http://127.0.0.1:3000').replace(/\/$/, '');
export const DEMO_PASSWORD = process.env.DEMO_PASSWORD ?? 'ChangeMe-Local-Only-123!';
export const ORIGIN = process.env.CP_ORIGIN ?? new URL(BASE_URL).origin;

export type ApiResult<T = unknown> = {
  response: Response;
  body: { data?: T; error?: { code?: string; message?: string; fields?: unknown } };
  cookie?: string;
};

export function setCookie(response: Response): string | undefined {
  // Node's undici exposes one combined header on some versions. The first
  // cookie pair is all the API needs; attributes must not be sent back.
  const raw = response.headers.get('set-cookie');
  if (!raw) return undefined;
  const first = raw.split(/,(?=[^;,]+=)/)[0];
  return first.split(';', 1)[0];
}

export async function api<T = unknown>(path: string, init: RequestInit = {}, cookie?: string): Promise<ApiResult<T>> {
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  if (init.method && init.method.toUpperCase() !== 'GET') headers.set('Origin', ORIGIN);
  if (cookie) headers.set('Cookie', cookie);
  const response = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  let body: ApiResult<T>['body'] = {};
  const text = await response.text();
  if (text) {
    try { body = JSON.parse(text) as ApiResult<T>['body']; } catch { body = { error: { message: text } }; }
  }
  return { response, body, cookie: setCookie(response) };
}

export async function login(email: string): Promise<string> {
  const result = await api<{ user: unknown }>('/api/auth/login', {
    method: 'POST',
    headers: { 'Idempotency-Key': `login-${email}-${Date.now()}-${Math.random()}` },
    body: JSON.stringify({ email, password: DEMO_PASSWORD }),
  });
  expect(result.response.status, JSON.stringify(result.body)).toBe(200);
  expect(result.cookie).toBeTruthy();
  return result.cookie!;
}

export async function expectError<T>(result: ApiResult<T>, statuses: number[] = [400, 401, 403, 409, 422]): Promise<void> {
  expect(statuses, `${result.response.status}: ${JSON.stringify(result.body)}`).toContain(result.response.status);
  expect(result.body.error).toBeTruthy();
}

export function json(method: string, payload: unknown, key: string): RequestInit {
  return { method, headers: { 'Idempotency-Key': createHash('sha256').update(key).digest('hex') }, body: JSON.stringify(payload) };
}

export function futureIso(minutes = 120): string {
  return new Date(Date.now() + minutes * 60_000).toISOString();
}

export function dayAndWindow(minutes = 120): { date: string; startTime: string; endTime: string } {
  const date = new Date(Date.now() + minutes * 60_000);
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit',
  }).formatToParts(date);
  const value = (type: string) => parts.find((part) => part.type === type)?.value ?? '';
  const time = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false,
  }).format(date);
  const [hour, minute] = time.split(':').map(Number);
  const start = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
  const endDate = new Date(date.getTime() + 30 * 60_000);
  const end = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false,
  }).format(endDate);
  return { date: `${value('year')}-${value('month')}-${value('day')}`, startTime: start, endTime: end };
}

