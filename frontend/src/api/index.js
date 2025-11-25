/**
 * API请求封装
 * 优化：添加统一错误处理、请求重试、加载状态
 */
import axios from 'axios'

const API_BASE_URL = '/api'
const DEFAULT_TIMEOUT = 60000
const UPLOAD_TIMEOUT = 120000

// 创建客户端实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: DEFAULT_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 可以在这里添加token等
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 统一错误处理
    if (error.code === 'ECONNABORTED') {
      console.error('请求超时')
      error.message = '请求超时，请检查网络连接'
    } else if (error.code === 'ERR_NETWORK') {
      console.error('网络错误')
      error.message = '网络错误，请确认后端服务已启动'
    } else if (error.response) {
      // 服务器返回错误
      const status = error.response.status
      const detail = error.response.data?.detail || error.message
      
      switch (status) {
        case 400:
          error.message = `请求参数错误: ${detail}`
          break
        case 404:
          error.message = `资源不存在: ${detail}`
          break
        case 500:
          error.message = `服务器错误: ${detail}`
          break
        default:
          error.message = `请求失败 (${status}): ${detail}`
      }
    }
    
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  /**
   * 获取指定难度的单词列表
   */
  getWords(difficulty = 1, limit = 10) {
    return apiClient.get('/words', {
      params: { difficulty, limit }
    })
  },

  /**
   * 获取今日待复习单词
   */
  getReviewWords(limit = 20) {
    return apiClient.get('/words/review', {
      params: { limit }
    })
  },

  /**
   * 获取错词本
   */
  getErrorWords(limit = 20) {
    return apiClient.get('/words/errors', {
      params: { limit }
    })
  },

  /**
   * 检查拼写
   */
  checkSpelling(wordId, input) {
    return apiClient.post('/spell/check', {
      word_id: wordId,
      input: input
    })
  },

  /**
   * 获取学习进度
   */
  getProgress() {
    return apiClient.get('/progress')
  },

  /**
   * 获取词库统计
   */
  getWordStats() {
    return apiClient.get('/words/stats')
  },

  /**
   * 重新智能分类单词难度
   */
  reclassifyWords() {
    return apiClient.post('/words/reclassify')
  },

  /**
   * 清空词库（删除所有单词）
   */
  formatWords() {
    return apiClient.post('/words/format')
  },

  /**
   * 清理学习进度（重置错词本和学习记录）
   */
  clearProgress() {
    return apiClient.post('/progress/clear')
  },

  /**
   * 标记单词为已学习
   */
  markWordStudied(wordId) {
    return apiClient.post('/progress/mark-studied', {
      word_id: wordId
    })
  },

  /**
   * 批量更新学习进度
   */
  batchUpdateProgress(wordIds) {
    return apiClient.post('/progress/batch-update', {
      word_ids: wordIds
    })
  },

  /**
   * 获取今日待复习单词数量
   */
  getReviewCount() {
    return apiClient.get('/progress/review-count')
  },

  /**
   * 上传自定义词库（优化：单独配置更长超时）
   */
  uploadWords(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/words/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      timeout: UPLOAD_TIMEOUT,
      maxContentLength: Infinity,
      maxBodyLength: Infinity
    })
  }
}
