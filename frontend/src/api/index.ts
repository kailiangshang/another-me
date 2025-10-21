import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Upload API
export const uploadAPI = {
  uploadFiles: async (files: File[]) => {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })
    const response = await api.post('/api/v1/upload/files', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
  uploadText: async (text: string, source: string) => {
    const response = await api.post('/api/v1/upload/text', { text, source })
    return response.data
  },
  getStatus: async () => {
    const response = await api.get('/api/v1/upload/status')
    return response.data
  },
}

// Config API
export const configAPI = {
  updateApiKey: async (apiKey: string, baseUrl: string, model: string) => {
    const response = await api.post('/api/v1/config/api-key', {
      api_key: apiKey,
      base_url: baseUrl,
      model: model,
    })
    return response.data
  },
  getApiConfig: async () => {
    const response = await api.get('/api/v1/config/api-key')
    return response.data
  },
}

// Mimic Me API
export const mimicAPI = {
  chat: async (prompt: string, context?: string, temperature?: number) => {
    const response = await api.post('/api/v1/mimic/chat', {
      prompt,
      context,
      temperature,
    })
    return response.data
  },
  generatePost: async (prompt: string, context?: string) => {
    const response = await api.post('/api/v1/mimic/generate-post', {
      prompt,
      context,
    })
    return response.data
  },
}

// Analysis API
export const analysisAPI = {
  generateReport: async (
    startDate?: string,
    endDate?: string,
    analysisType?: string
  ) => {
    const response = await api.post('/api/v1/analysis/report', {
      start_date: startDate,
      end_date: endDate,
      analysis_type: analysisType,
    })
    return response.data
  },
  getEmotions: async () => {
    const response = await api.get('/api/v1/analysis/emotions')
    return response.data
  },
  getKeywords: async () => {
    const response = await api.get('/api/v1/analysis/keywords')
    return response.data
  },
  getRelationships: async () => {
    const response = await api.get('/api/v1/analysis/relationships')
    return response.data
  },
}

// Memory API
export const memoryAPI = {
  recall: async (query: string, timeContext?: string, limit?: number) => {
    const response = await api.post('/api/v1/memory/recall', {
      query,
      time_context: timeContext,
      limit,
    })
    return response.data
  },
  getTimeline: async (year?: number, month?: number) => {
    const params = new URLSearchParams()
    if (year) params.append('year', year.toString())
    if (month) params.append('month', month.toString())
    const response = await api.get(`/api/v1/memory/timeline?${params}`)
    return response.data
  },
  findSimilar: async (query: string, limit?: number) => {
    const response = await api.post('/api/v1/memory/similar', { query, limit })
    return response.data
  },
}
