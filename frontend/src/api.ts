import type { FeedbackPayload, RecommendResponse, SceneFeedbackPayload, TaxonomyResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function recommendVoice(text: string): Promise<RecommendResponse> {
  return request<RecommendResponse>('/api/recommend', {
    method: 'POST',
    body: JSON.stringify({ text, task_type: 'voice', use_deepseek: true }),
  });
}

export function fetchTaxonomy(): Promise<TaxonomyResponse> {
  return request<TaxonomyResponse>('/api/taxonomy');
}

export function submitFeedback(payload: FeedbackPayload): Promise<{ feedback_id: string; status: string }> {
  return request('/api/feedback', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export function submitSceneFeedback(payload: SceneFeedbackPayload): Promise<{ feedback_id: string; status: string }> {
  return request('/api/scene-feedback', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
