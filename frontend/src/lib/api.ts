import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Functions
export const brandApi = {
  listBrands: () => api.get('/api/brands'),

  analyzeBrand: (brandId: string, includeCompetitors = true) =>
    api.post(`/api/analyze/${brandId}`, { include_competitors: includeCompetitors }),

  generatePlan: (brandId: string, budget?: number, timeframe = '12 months') =>
    api.post(`/api/generate-plan/${brandId}`, { budget, timeframe }),

  runScenario: (data: { brand_id?: string; brand_name?: string; scenario_question: string; current_context?: string }) =>
    api.post('/api/scenario', data),

  validateContent: (data: { content_type: string; content: string; validation_criteria?: string[] }) =>
    api.post('/api/validate', data),
};

export default api;
