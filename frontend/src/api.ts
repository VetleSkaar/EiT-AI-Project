import axios from 'axios';
import type { Draft, DraftCreate, AnalysisResponse, AnalysisData } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Create a new draft
 */
export async function createDraft(data: DraftCreate): Promise<Draft> {
  const response = await api.post<Draft>('/drafts', data);
  return response.data;
}

/**
 * Get a draft by ID
 */
export async function getDraft(id: number): Promise<Draft> {
  const response = await api.get<Draft>(`/drafts/${id}`);
  return response.data;
}

/**
 * Trigger analysis for a draft
 */
export async function analyzeDraft(id: number): Promise<AnalysisResponse> {
  const response = await api.post<AnalysisResponse>(`/drafts/${id}/analyze`);
  return response.data;
}

/**
 * Get analysis results for a draft
 */
export async function getAnalysis(id: number): Promise<AnalysisData> {
  const response = await api.get<AnalysisData>(`/drafts/${id}/analysis`);
  return response.data;
}

export default api;
