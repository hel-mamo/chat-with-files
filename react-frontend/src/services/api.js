import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export const askQuestion = async (question, fileId = null) => {
  const response = await api.post('/ask', { question, file_id: fileId })
  return response.data
}

export const getFiles = async () => {
  const response = await api.get('/files')
  return response.data.files
}

export const getFileHistory = async (fileId) => {
  const response = await api.get(`/files/${fileId}/history`)
  return response.data.history
}

export const downloadFile = async (fileId) => {
  const response = await api.get(`/files/${fileId}/download`, {
    responseType: 'blob',
  })
  return response.data
}

export const deleteFile = async (fileId) => {
  const response = await api.delete(`/files/${fileId}`)
  return response.data
}

export default api
