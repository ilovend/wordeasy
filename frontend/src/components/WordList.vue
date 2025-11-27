<template>
  <div class="word-list-container min-h-screen bg-gradient-to-br from-purple-50 to-pink-100 p-8">
    <div class="max-w-6xl mx-auto">
      <!-- 标题 -->
      <h1 class="text-4xl font-bold text-center mb-8 text-purple-700">📚 词库管理中心</h1>

      <!-- 标签页导航 -->
      <div class="tabs-nav bg-white rounded-xl shadow-lg mb-8 p-2">
        <div class="flex gap-2">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'flex-1 py-3 px-4 rounded-lg font-semibold transition-all',
              activeTab === tab.id
                ? 'bg-purple-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ tab.icon }} {{ tab.name }}
          </button>
        </div>
      </div>

        <!-- 标签页内容 -->
      <div class="tab-content">
        <!-- 📝 添加单词 -->
        <div v-show="activeTab === 'add'" class="space-y-6">
          <!-- 快速添加单词 -->
          <div class="add-word-section bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-2xl font-bold mb-4 text-gray-800">✏️ 快速添加单词</h2>
        <p class="text-gray-600 mb-4">手动添加自己的单词，支持批量粘贴</p>
        
        <div class="add-word-form space-y-4">
          <!-- 单词输入 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">英文单词 *</label>
            <input
              v-model="newWord.word"
              type="text"
              placeholder="例如：hello"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              @keydown.enter="addSingleWord"
            />
          </div>
          
          <!-- 释义输入 -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">中文释义 *</label>
            <input
              v-model="newWord.meaning"
              type="text"
              placeholder="例如：你好"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              @keydown.enter="addSingleWord"
            />
          </div>
          
          <!-- 添加按钮 -->
          <button
            @click="addSingleWord"
            :disabled="!newWord.word || !newWord.meaning || adding"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition"
          >
            {{ adding ? '添加中...' : '➕ 添加单词' }}
          </button>
        </div>

        <!-- 批量添加区域 -->
        <div class="mt-6 pt-6 border-t">
          <h3 class="text-lg font-bold mb-3 text-gray-800">📋 批量添加</h3>
          <p class="text-sm text-gray-600 mb-3">
            每行一个单词，格式：<code class="bg-gray-100 px-2 py-1 rounded">单词 释义</code> 或 <code class="bg-gray-100 px-2 py-1 rounded">单词|释义</code>
          </p>
          <textarea
            v-model="batchWords"
            rows="6"
            placeholder="hello 你好&#10;world 世界&#10;study 学习"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent font-mono text-sm"
          ></textarea>
          <button
            @click="addBatchWords"
            :disabled="!batchWords.trim() || batchAdding"
            class="w-full mt-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 rounded-lg transition"
          >
            {{ batchAdding ? '添加中...' : '📝 批量添加' }}
          </button>
        </div>

            <!-- 添加结果 -->
            <div v-if="addResult" class="mt-4 p-4 rounded-lg" :class="addResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'">
              {{ addResult.message }}
            </div>
          </div>

          <!-- 上传文件（支持多种格式） -->
          <div class="upload-section bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">📤 导入词库文件</h2>
        <p class="text-gray-600 mb-4">
          支持多种格式：CSV、JSON、TXT（自动识别格式）
        </p>
        
        <!-- 格式说明 -->
        <div class="format-info mb-4 p-4 bg-blue-50 rounded-lg">
          <div class="text-sm text-gray-700">
            <div class="font-semibold mb-2">📌 支持的文件格式：</div>
            <ul class="list-disc list-inside space-y-1 ml-2">
              <li><strong>TXT</strong>: 每行 <code class="bg-white px-2 py-0.5 rounded">word|meaning</code> 或 <code class="bg-white px-2 py-0.5 rounded">word meaning</code></li>
              <li><strong>CSV</strong>: <code class="bg-white px-2 py-0.5 rounded">word,meaning</code></li>
              <li><strong>JSON</strong>: <code class="bg-white px-2 py-0.5 rounded">[{"word":"hello","meaning":"你好"}]</code></li>
            </ul>
          </div>
        </div>

        <!-- 格式转换提示 -->
        <div class="convert-tip mb-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
          <div class="flex items-start gap-2">
            <span class="text-yellow-600 text-lg">💡</span>
            <div class="text-sm text-gray-700">
              <strong>格式不匹配？</strong>使用我们的在线转换工具：
              <button @click="showConverter = !showConverter" class="ml-2 text-purple-600 font-semibold hover:underline">
                {{ showConverter ? '隐藏转换器' : '显示转换器' }}
              </button>
            </div>
          </div>
        </div>

        <!-- 在线格式转换器 -->
        <div v-if="showConverter" class="converter-box mb-6 p-4 bg-gray-50 rounded-lg border-2 border-purple-200">
          <h3 class="text-lg font-bold mb-3 text-gray-800">🔄 在线格式转换</h3>
          
          <div class="space-y-3">
            <!-- 选择格式 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">输入格式</label>
              <select v-model="converter.format" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500">
                <option value="auto">自动检测</option>
                <option value="csv">CSV (逗号分隔)</option>
                <option value="json">JSON</option>
                <option value="txt">TXT (空格分隔)</option>
              </select>
            </div>

            <!-- 输入文本 -->
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">粘贴您的词库内容</label>
              <textarea
                v-model="converter.input"
                rows="8"
                placeholder="粘贴词库内容，例如：&#10;hello,你好&#10;world,世界"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 font-mono text-sm"
              ></textarea>
            </div>

            <!-- 转换按钮 -->
            <button
              @click="convertFormat"
              :disabled="!converter.input.trim() || converting"
              class="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold py-2 rounded-lg transition"
            >
              {{ converting ? '转换中...' : '🔄 转换格式' }}
            </button>

            <!-- 转换结果 -->
            <div v-if="converter.output">
              <label class="block text-sm font-semibold text-gray-700 mb-2">转换结果（WordEasy格式）</label>
              <textarea
                :value="converter.output"
                rows="8"
                readonly
                class="w-full px-4 py-3 border border-gray-300 rounded-lg bg-white font-mono text-sm"
              ></textarea>
              <div class="flex gap-2 mt-2">
                <button
                  @click="copyConverted"
                  class="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded-lg transition"
                >
                  📋 复制结果
                </button>
                <button
                  @click="uploadConverted"
                  :disabled="uploadingConverted"
                  class="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-2 rounded-lg transition"
                >
                  {{ uploadingConverted ? '上传中...' : '⬆️ 直接上传' }}
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 文件上传区 -->
        <div class="upload-area">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            accept=".txt,.csv,.json"
            class="hidden"
          />
          <button
            @click="triggerFileInput"
            class="w-full border-2 border-dashed border-purple-300 hover:border-purple-500 rounded-lg p-8 text-center transition"
          >
            <div class="text-4xl mb-2">📁</div>
            <div class="text-lg font-semibold text-purple-600">
              {{ selectedFile ? selectedFile.name : '点击选择文件' }}
            </div>
            <div class="text-sm text-gray-500 mt-2">
              支持 TXT / CSV / JSON 格式
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
        </div>

        <!-- 📊 词库统计 -->
        <div v-show="activeTab === 'stats'" class="space-y-6">
          <!-- 内置词库统计 -->
          <div class="stats-section bg-white rounded-xl shadow-lg p-6">
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
        </div>

        <!-- 📖 学习记录 -->
        <div v-show="activeTab === 'review'" class="space-y-6">
          <!-- 错词本 -->
          <div class="error-words-section bg-white rounded-xl shadow-lg p-6">
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

// 标签页
const activeTab = ref('add')
const tabs = [
  { id: 'add', name: '添加单词', icon: '📝' },
  { id: 'stats', name: '词库管理', icon: '📊' }
]

// 新增：快速添加单词
const newWord = ref({ word: '', meaning: '' })
const adding = ref(false)
const batchWords = ref('')
const batchAdding = ref(false)
const addResult = ref(null)

// 新增：格式转换器
const showConverter = ref(false)
const converter = ref({
  format: 'auto',
  input: '',
  output: ''
})
const converting = ref(false)
const uploadingConverted = ref(false)

// 方法
function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) {
    const ext = file.name.split('.').pop().toLowerCase()
    if (['txt', 'csv', 'json'].includes(ext)) {
      selectedFile.value = file
      uploadResult.value = null
    } else {
      alert('请选择 TXT、CSV 或 JSON 文件')
    }
  }
}

// 新增：单个单词添加
async function addSingleWord() {
  if (!newWord.value.word || !newWord.value.meaning) return
  
  adding.value = true
  addResult.value = null
  
  try {
    const content = `${newWord.value.word.trim().toLowerCase()}|${newWord.value.meaning.trim()}`
    const blob = new Blob([content], { type: 'text/plain' })
    const file = new File([blob], 'single_word.txt', { type: 'text/plain' })
    
    const result = await api.uploadWords(file)
    addResult.value = {
      success: true,
      message: `✅ 成功添加单词：${newWord.value.word}`
    }
    
    // 清空输入
    newWord.value = { word: '', meaning: '' }
    
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('添加单词失败:', error)
    addResult.value = {
      success: false,
      message: '❌ 添加失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    adding.value = false
  }
}

// 新增：批量添加
async function addBatchWords() {
  if (!batchWords.value.trim()) return
  
  batchAdding.value = true
  addResult.value = null
  
  try {
    // 解析批量输入，支持多种格式
    const lines = batchWords.value.split('\n').filter(line => line.trim())
    const converted = []
    
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed) continue
      
      let word, meaning
      
      // 支持 | 分隔
      if (trimmed.includes('|')) {
        [word, meaning] = trimmed.split('|', 2)
      }
      // 支持空格或Tab分隔
      else if (trimmed.includes('\t')) {
        [word, meaning] = trimmed.split('\t', 2)
      }
      else if (trimmed.includes(' ')) {
        const parts = trimmed.split(/\s+/, 2)
        word = parts[0]
        meaning = parts[1]
      }
      
      if (word && meaning) {
        converted.push(`${word.trim().toLowerCase()}|${meaning.trim()}`)
      }
    }
    
    if (converted.length === 0) {
      addResult.value = {
        success: false,
        message: '❌ 未找到有效的单词，请检查格式'
      }
      return
    }
    
    // 创建文件并上传
    const content = converted.join('\n')
    const blob = new Blob([content], { type: 'text/plain' })
    const file = new File([blob], 'batch_words.txt', { type: 'text/plain' })
    
    const result = await api.uploadWords(file)
    addResult.value = {
      success: true,
      message: `✅ 成功添加 ${converted.length} 个单词`
    }
    
    // 清空输入
    batchWords.value = ''
    
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('批量添加失败:', error)
    addResult.value = {
      success: false,
      message: '❌ 批量添加失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    batchAdding.value = false
  }
}

// 新增：格式转换
function convertFormat() {
  converting.value = true
  converter.value.output = ''
  
  try {
    const input = converter.value.input.trim()
    if (!input) return
    
    const lines = input.split('\n').filter(line => line.trim())
    const converted = []
    
    for (const line of lines) {
      const trimmed = line.trim()
      if (!trimmed) continue
      
      let word, meaning
      
      // 自动检测格式
      if (converter.value.format === 'auto' || converter.value.format === 'csv') {
        // CSV格式: word,meaning
        if (trimmed.includes(',')) {
          const parts = trimmed.split(',')
          word = parts[0]
          meaning = parts.slice(1).join(',') // 支持释义中有逗号
        }
      }
      
      if (!word && (converter.value.format === 'auto' || converter.value.format === 'txt')) {
        // TXT格式: word [空格/Tab] meaning
        if (trimmed.includes('\t')) {
          [word, meaning] = trimmed.split('\t', 2)
        } else if (trimmed.includes(' ')) {
          const parts = trimmed.split(/\s+/, 2)
          word = parts[0]
          meaning = parts[1]
        }
      }
      
      if (!word && converter.value.format === 'auto') {
        // 已经是标准格式
        if (trimmed.includes('|')) {
          [word, meaning] = trimmed.split('|', 2)
        }
      }
      
      if (word && meaning) {
        converted.push(`${word.trim().toLowerCase()}|${meaning.trim()}`)
      }
    }
    
    // JSON格式需要特殊处理
    if (converter.value.format === 'json' || (converter.value.format === 'auto' && (input.startsWith('[') || input.startsWith('{')))) {
      try {
        const data = JSON.parse(input)
        converted.length = 0 // 清空之前的结果
        
        if (Array.isArray(data)) {
          // 数组格式
          for (const item of data) {
            const word = item.word || item.en || item.english || item.term || ''
            const meaning = item.meaning || item.zh || item.chinese || item.definition || ''
            if (word && meaning) {
              converted.push(`${word.trim().toLowerCase()}|${meaning.trim()}`)
            }
          }
        } else if (typeof data === 'object') {
          // 对象格式
          for (const [word, meaning] of Object.entries(data)) {
            if (word && meaning) {
              converted.push(`${word.trim().toLowerCase()}|${String(meaning).trim()}`)
            }
          }
        }
      } catch (e) {
        // JSON解析失败，继续使用之前的结果
        console.warn('JSON parse failed, using line-by-line parsing')
      }
    }
    
    converter.value.output = converted.join('\n')
    
    if (converted.length === 0) {
      alert('❌ 转换失败：未找到有效的单词数据\n\n请检查格式是否正确')
    }
  } catch (error) {
    console.error('转换失败:', error)
    alert('转换失败: ' + error.message)
  } finally {
    converting.value = false
  }
}

// 新增：复制转换结果
function copyConverted() {
  if (!converter.value.output) return
  
  navigator.clipboard.writeText(converter.value.output).then(() => {
    alert('✅ 已复制到剪贴板')
  }).catch(err => {
    console.error('复制失败:', err)
    alert('❌ 复制失败')
  })
}

// 新增：直接上传转换结果
async function uploadConverted() {
  if (!converter.value.output) return
  
  uploadingConverted.value = true
  uploadResult.value = null
  
  try {
    const blob = new Blob([converter.value.output], { type: 'text/plain' })
    const file = new File([blob], 'converted_words.txt', { type: 'text/plain' })
    
    const result = await api.uploadWords(file)
    uploadResult.value = {
      success: true,
      message: result.message || `成功导入 ${result.count} 个单词`
    }
    
    // 清空转换器
    converter.value.input = ''
    converter.value.output = ''
    
    // 刷新统计
    await loadStats()
  } catch (error) {
    console.error('上传失败:', error)
    uploadResult.value = {
      success: false,
      message: '上传失败: ' + (error.response?.data?.detail || error.message)
    }
  } finally {
    uploadingConverted.value = false
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

function goToReview(type) {
  if (type === 'error') {
    window.location.href = '/review?mode=error'
  } else {
    window.location.href = '/review'
  }
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
