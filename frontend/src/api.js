import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export default {
  // Draft operations
  async createDraft(draft) {
    const response = await api.post('/drafts', draft)
    return response.data
  },

  async getDraft(id) {
    const response = await api.get(`/drafts/${id}`)
    return response.data
  },

  async listDrafts() {
    const response = await api.get('/drafts')
    return response.data
  },

  // Analysis operations
  async analyzeDraft(draftId) {
    const response = await api.post(`/drafts/${draftId}/analyze`)
    return response.data
  },

  async getAnalysis(draftId) {
    const response = await api.get(`/drafts/${draftId}/analysis`)
    return response.data
  },
}
