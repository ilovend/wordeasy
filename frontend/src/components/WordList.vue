<template>
  <div class="word-list-container min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
    <div class="max-w-4xl mx-auto">
      <!-- 标题 -->
      <h1 class="text-4xl font-bold text-center mb-8 text-purple-700">📚 词库管理</h1>

      <!-- 上传自定义词库 -->
      <div class="upload-section bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">📤 上传自定义词库</h2>
        <p class="text-gray-600 mb-4">
          支持TXT文件，每行一个单词，格式：英文|中文（如：abandon|放弃）
        </p>
        
        <div class="upload-area">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            accept=".txt"
            class="hidden"
          />
          <button
            @click="triggerFileInput"
            class="w-full border-2 border-dashed border-purple-300 hover:border-purple-500 rounded-lg p-8 text-center transition"
          >
            <div class="text-4xl mb-2">📁</div>
            <div class="text-lg font-semibold text-purple-600">
              {{ selectedFile ? selectedFile.name : '点击选择TXT文件' }}
            </div>
            <div class="text-sm text-gray-500 mt-2">
              或将文件拖放至此处
            </div>
          </button>
        </div>

        <button
          v-if="selectedFile"
          @click="uploadFile"
          :disabled="uploading"
          class="w-full mt-4 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition"
        >
          {{ uploading ? '上传中...' : '开始上传' }}
        </button>

        <!-- 上传结果提示 -->
        <div v-if="uploadResult" class="mt-4 p-4 rounded-lg" :class="uploadResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
          {{ uploadResult.message }}
        </div>
      </div>

      <!-- 内置词库统计 -->
      <div class="stats-section bg-white rounded-xl shadow-lg p-6 mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-800">📊 词库统计</h2>
          <div class="flex gap-3">
            <button
              @click="formatWords"
              :disabled="formatting"
              class="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
              title="删除所有单词数据"
            >
              {{ formatting ? '清空中...' : '🗑️ 清空词库' }}
            </button>
            <button
              @click="reclassifyWords"
              :disabled="reclassifying"
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
              title="重新智能分类所有自定义单词的难度"
            >
              {{ reclassifying ? '分类中...' : '🔀 智能分类' }}
            </button>
          </div>
        </div>
        <div v-if="initResult" class="mb-4 p-3 rounded-lg" :class="initResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
          {{ initResult.message }}
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="stat-card bg-green-50 p-4 rounded-lg text-center">
            <div class="text-3xl font-bold text-green-600">{{ stats.level1 || 0 }}</div>
            <div class="text-sm text-gray-600">初级单词</div>
          </div>
          <div class="stat-card bg-blue-50 p-4 rounded-lg text-center">
            <div class="text-3xl font-bold text-blue-600">{{ stats.level2 || 0 }}</div>
            <div class="text-sm text-gray-600">中级单词</div>
          </div>
          <div class="stat-card bg-red-50 p-4 rounded-lg text-center">
            <div class="text-3xl font-bold text-red-600">{{ stats.level3 || 0 }}</div>
            <div class="text-sm text-gray-600">高级单词</div>
          </div>
          <div class="stat-card bg-purple-50 p-4 rounded-lg text-center">
            <div class="text-3xl font-bold text-purple-600">{{ stats.total || 0 }}</div>
            <div class="text-sm text-gray-600">总单词数</div>
          </div>
        </div>
        <div class="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-gray-700">
          💡 <strong>功能说明</strong>：
          <span class="inline-block ml-2">🗑️清空词库=删除所有单词数据</span>
          <span class="inline-block ml-2">🔀智能分类=自动判断难度等级</span>
        </div>
      </div>

      <!-- 错词本 -->
      <div class="error-words-section bg-white rounded-xl shadow-lg p-6 mb-8">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-800">❌ 错词本</h2>
          <button
            v-if="errorWords.length > 0"
            @click="clearProgress"
            :disabled="clearingProgress"
            class="px-4 py-2 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
            title="清理所有学习进度和错误记录"
          >
            {{ clearingProgress ? '清理中...' : '🧹 清理进度' }}
          </button>
        </div>
        <p class="text-gray-600 mb-4">历史拼写错误的单词，重点复习</p>
        
        <button
          @click="loadErrorWords"
          :disabled="loadingErrors"
          class="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition mb-4"
        >
          {{ loadingErrors ? '加载中...' : '加载错词本' }}
        </button>

        <div v-if="errorWords.length > 0" class="error-list space-y-2">
          <div
            v-for="word in errorWords"
            :key="word.id"
            class="error-item flex justify-between items-center p-4 bg-red-50 rounded-lg hover:bg-red-100 transition"
          >
            <div>
              <div class="font-mono text-lg font-bold text-gray-800">{{ word.word }}</div>
              <div class="text-sm text-gray-600">{{ word.zh_definition }}</div>
            </div>
            <div class="text-right">
              <div class="text-red-600 font-bold">错误 {{ word.error_count }} 次</div>
              <div class="text-xs text-gray-500">{{ getDifficultyText(word.difficulty) }}</div>
            </div>
          </div>
        </div>
        <div v-else-if="errorWordsLoaded" class="text-center text-gray-500 py-8">
          暂无错词，继续加油！
        </div>
      </div>

      <!-- 待复习单词 -->
      <div class="review-words-section bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">📅 今日待复习</h2>
        <p class="text-gray-600 mb-4">基于遗忘曲线，智能推送待复习单词</p>
        
        <button
          @click="loadReviewWords"
          :disabled="loadingReview"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition mb-4"
        >
          {{ loadingReview ? '加载中...' : '查看待复习单词' }}
        </button>

        <div v-if="reviewWords.length > 0" class="review-list space-y-2">
          <div
            v-for="word in reviewWords"
            :key="word.id"
            class="review-item flex justify-between items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition"
          >
            <div>
              <div class="font-mono text-lg font-bold text-gray-800">{{ word.word }}</div>
              <div class="text-sm text-gray-600">{{ word.zh_definition }}</div>
            </div>
            <div class="text-right">
              <div class="mastery-badge px-3 py-1 rounded-full text-sm font-bold" :class="getMasteryClass(word.mastery_level)">
                {{ getMasteryText(word.mastery_level) }}
              </div>
              <div class="text-xs text-gray-500 mt-1">{{ word.category }}</div>
            </div>
          </div>
        </div>
        <div v-else-if="reviewWordsLoaded" class="text-center text-gray-500 py-8">
          今日无待复习单词，您已完成所有复习！
        </div>
      </div>

      <!-- 返回按钮 -->
      <div class="mt-8 text-center">
        <button
          @click="goBack"
          class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-lg transition"
        >
          ← 返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

// 状态
const fileInput = ref(null)
const selectedFile = ref(null)
const uploading = ref(false)
const uploadResult = ref(null)
const reclassifying = ref(false)
const formatting = ref(false)
const clearingProgress = ref(false)
const initResult = ref(null)
const stats = ref({ level1: 0, level2: 0, level3: 0, total: 0 })
const errorWords = ref([])
const reviewWords = ref([])
const loadingErrors = ref(false)
const loadingReview = ref(false)
const errorWordsLoaded = ref(false)
const reviewWordsLoaded = ref(false)

// 方法
function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file && file.name.endsWith('.txt')) {
    selectedFile.value = file
    uploadResult.value = null
  } else {
    alert('请选择TXT文件')
  }
}

async function uploadFile() {
  if (!selectedFile.value) return

  uploading.value = true
  uploadResult.value = null

  try {
    console.log('开始上传文件:', selectedFile.value.name, '大小:', selectedFile.value.size, 'bytes')
    const result = await api.uploadWords(selectedFile.value)
    console.log('上传成功:', result)
    uploadResult.value = {
      success: true,
      message: result.message || `成功导入 ${result.count} 个单词`
    }
    selectedFile.value = null
    fileInput.value.value = ''
    
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('上传失败:', error)
    let errorMsg = '上传失败'
    
    if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      errorMsg = '上传超时，请尝试：1）使用较小的文件 2）检查网络连接'
    } else if (error.code === 'ERR_NETWORK') {
      errorMsg = 'Network Error - 请确认：1）后端服务是否运行（http://localhost:8000） 2）刷新页面后重试'
    } else if (error.response) {
      errorMsg = `服务器错误 (${error.response.status}): ${error.response.data?.detail || error.message}`
    } else {
      errorMsg = error.message || '未知错误'
    }
    
    uploadResult.value = {
      success: false,
      message: errorMsg
    }
  } finally {
    uploading.value = false
  }
}

async function loadStats() {
  try {
    // 使用专门的统计API，返回准确的单词数量
    const stats_data = await api.getWordStats()
    stats.value = {
      level1: stats_data.level1,
      level2: stats_data.level2,
      level3: stats_data.level3,
      total: stats_data.total
    }
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
}

async function reclassifyWords() {
  if (!confirm('确定要重新分类所有自定义单词吗？系统会根据单词长度和词缀智能判断难度等级。')) {
    return
  }
  
  reclassifying.value = true
  initResult.value = null
  
  try {
    const result = await api.reclassifyWords()
    console.log('重新分类结果:', result)
    initResult.value = {
      success: true,
      message: result.message
    }
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('重新分类失败:', error)
    initResult.value = {
      success: false,
      message: '重新分类失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    reclassifying.value = false
  }
}

async function formatWords() {
  if (!confirm('⚠️ 警告：此操作将删除所有单词数据，无法恢复！\n\n确定要清空词库吗？')) {
    return
  }
  
  // 二次确认
  if (!confirm('再次确认：真的要删除所有单词数据吗？')) {
    return
  }
  
  formatting.value = true
  initResult.value = null
  
  try {
    const result = await api.formatWords()
    console.log('清空词库结果:', result)
    initResult.value = {
      success: true,
      message: result.message
    }
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('清空词库失败:', error)
    initResult.value = {
      success: false,
      message: '清空词库失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    formatting.value = false
  }
}

async function clearProgress() {
  if (!confirm('⚠️ 确定要清理所有学习进度吗？\n\n这将重置：\n1. 所有单词的学习记录\n2. 错词本内容\n3. 掌握度等级\n\n此操作不可恢复！')) {
    return
  }
  
  clearingProgress.value = true
  initResult.value = null
  
  try {
    const result = await api.clearProgress()
    console.log('清理进度结果:', result)
    initResult.value = {
      success: true,
      message: result.message
    }
    // 清空错词本显示
    errorWords.value = []
    errorWordsLoaded.value = false
    reviewWords.value = []
    reviewWordsLoaded.value = false
  } catch (error) {
    console.error('清理进度失败:', error)
    initResult.value = {
      success: false,
      message: '清理进度失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    clearingProgress.value = false
  }
}

async function loadErrorWords() {
  loadingErrors.value = true
  try {
    errorWords.value = await api.getErrorWords(20)
    errorWordsLoaded.value = true
  } catch (error) {
    console.error('Failed to load error words:', error)
    alert('加载错词本失败')
  } finally {
    loadingErrors.value = false
  }
}

async function loadReviewWords() {
  loadingReview.value = true
  try {
    reviewWords.value = await api.getReviewWords(20)
    reviewWordsLoaded.value = true
  } catch (error) {
    console.error('Failed to load review words:', error)
    alert('加载待复习单词失败')
  } finally {
    loadingReview.value = false
  }
}

function getDifficultyText(level) {
  const map = { 1: '初级', 2: '中级', 3: '高级' }
  return map[level] || '未知'
}

function getMasteryText(level) {
  const map = { 0: '陌生', 1: '熟悉', 2: '掌握' }
  return map[level] || '未知'
}

function getMasteryClass(level) {
  const classes = {
    0: 'bg-red-200 text-red-700',
    1: 'bg-yellow-200 text-yellow-700',
    2: 'bg-green-200 text-green-700'
  }
  return classes[level] || 'bg-gray-200 text-gray-700'
}

function goBack() {
  window.location.href = '/'
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.word-list-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
