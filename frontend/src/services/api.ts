import axios from "axios"

// 创建axios实例
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000/api/v1",
  timeout: 30000,
  headers: {
    "Content-Type": "application/json"
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log("发送请求:", config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error("请求错误:", error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log("收到响应:", response.status, response.config.url)
    return response
  },
  (error) => {
    console.error("响应错误:", error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

// API接口定义
export interface TTSRequest {
  text: string
  model: string
}

export interface TTSResponse {
  success: boolean
  message: string
  data?: {
    audio_url: string
    duration: number
    file_size: number
  }
}

export interface Model {
  id: string
  name: string
  display_name: string
  language: string
  gender: string
  sample_rate: number
  available: boolean
}

export interface ModelsResponse {
  success: boolean
  message: string
  data: Model[]
}

export interface HistoryRecord {
  id: number
  text: string
  model: string
  audio_url: string
  duration: number
  file_size: number
  created_at: string
}

export interface HistoryResponse {
  success: boolean
  message: string
  data: {
    records: HistoryRecord[]
    total: number
    page: number
    per_page: number
    pages: number
  }
}

export interface SystemHealth {
  status: string
  timestamp: string
  version: string
  models_loaded: number
  total_requests: number
  uptime: string
}

export interface SystemHealthResponse {
  success: boolean
  message: string
  data: SystemHealth
}

// TTS相关API
export const ttsAPI = {
  // 文字转语音
  synthesize: async (data: TTSRequest): Promise<Blob> => {
    const response = await api.post("/tts/synthesize", data, {
      responseType: "blob"
    })
    return response.data
  },

  // 获取历史记录
  getHistory: async (page = 1, limit = 10): Promise<HistoryResponse> => {
    const response = await api.get(`/tts/history?page=${page}&limit=${limit}`)
    return response.data
  },

  // 删除历史记录
  deleteHistory: async (id: number): Promise<{ success: boolean; message: string }> => {
    const response = await api.delete(`/tts/history/${id}`)
    return response.data
  }
}

// 模型相关API
export const modelsAPI = {
  // 获取可用模型列表
  getModels: async (): Promise<ModelsResponse> => {
    const response = await api.get("/models")
    return response.data
  }
}

// 系统相关API
export const systemAPI = {
  // 健康检查
  getHealth: async (): Promise<SystemHealthResponse> => {
    const response = await api.get("/system/health")
    return response.data
  }
}

export default api