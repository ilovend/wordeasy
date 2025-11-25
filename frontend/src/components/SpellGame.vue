<template>
  <div class="spell-game-container min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
    <!-- Loading 状态 -->
    <LoadingSpinner :loading="isLoading" message="加载单词中..." />
    
    <!-- 游戏头部信息 -->
    <div v-if="gameStarted" class="game-header mb-8 flex justify-between items-center">
      <div class="stats flex gap-6">
        <div class="stat-item bg-white px-4 py-2 rounded-lg shadow">
          <span class="text-gray-600">❤️ 生命值:</span>
          <span class="text-red-500 font-bold ml-2">{{ lives }}</span>
        </div>
        <div class="stat-item bg-white px-4 py-2 rounded-lg shadow">
          <span class="text-gray-600">⭐ 积分:</span>
          <span class="text-yellow-500 font-bold ml-2">{{ score }}</span>
        </div>
        <div class="stat-item bg-white px-4 py-2 rounded-lg shadow">
          <span class="text-gray-600">⏰ 时间:</span>
          <span class="text-blue-500 font-bold ml-2">{{ timeLeft }}s</span>
        </div>
        <div class="stat-item bg-white px-4 py-2 rounded-lg shadow">
          <span class="text-gray-600">📝 进度:</span>
          <span class="text-purple-500 font-bold ml-2">{{ currentWordIndex + 1 }}/{{ currentWords.length }}</span>
        </div>
      </div>
      <button
        @click="exitChallenge"
        class="px-6 py-2 bg-red-500 hover:bg-red-600 text-white font-bold rounded-lg transition shadow-lg"
      >
        🚪 退出闯关
      </button>
    </div>

    <!-- 难度选择界面 -->
    <div v-if="!gameStarted && !gameOver && !learningMode" class="difficulty-selection max-w-2xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-indigo-700">🎮 拼写攻防战</h1>
      <p class="text-center text-gray-600 mb-12">选择难度开始学习，掌握单词后再挑战！</p>
      
      <!-- 今日复习提醒 -->
      <div v-if="reviewCount > 0" class="review-reminder bg-gradient-to-r from-orange-50 to-red-50 border-2 border-orange-300 rounded-xl p-6 mb-8 shadow-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="text-5xl animate-bounce">📚</div>
            <div>
              <h3 class="text-2xl font-bold text-orange-700 mb-1">今日待复习</h3>
              <p class="text-orange-600">有 <span class="text-3xl font-bold text-red-600">{{ reviewCount }}</span> 个单词需要复习</p>
            </div>
          </div>
          <button
            @click="startReviewMode"
            class="px-8 py-4 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white text-xl font-bold rounded-xl shadow-lg transform hover:scale-105 transition"
          >
            <div class="flex items-center gap-2">
              <span>🔄</span>
              <span>开始复习</span>
            </div>
          </button>
        </div>
      </div>
      
      <div class="difficulty-options grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <button
          @click="selectDifficulty(1)"
          class="difficulty-btn bg-green-500 hover:bg-green-600 text-white p-8 rounded-xl shadow-lg transform hover:scale-105 transition"
        >
          <div class="text-3xl mb-3">🌱</div>
          <h3 class="text-2xl font-bold mb-2">初级</h3>
          <p class="text-sm opacity-90">3-5字母短单词</p>
          <p class="text-xs mt-2 opacity-75">适合入门学习</p>
        </button>

        <button
          @click="selectDifficulty(2)"
          class="difficulty-btn bg-blue-500 hover:bg-blue-600 text-white p-8 rounded-xl shadow-lg transform hover:scale-105 transition"
        >
          <div class="text-3xl mb-3">⚡</div>
          <h3 class="text-2xl font-bold mb-2">中级</h3>
          <p class="text-sm opacity-90">6-8字母考试词</p>
          <p class="text-xs mt-2 opacity-75">提升词汇量</p>
        </button>

        <button
          @click="selectDifficulty(3)"
          class="difficulty-btn bg-red-500 hover:bg-red-600 text-white p-8 rounded-xl shadow-lg transform hover:scale-105 transition"
        >
          <div class="text-3xl mb-3">🔥</div>
          <h3 class="text-2xl font-bold mb-2">高级</h3>
          <p class="text-sm opacity-90">长单词、易混词</p>
          <p class="text-xs mt-2 opacity-75">挑战拼写大师</p>
        </button>
      </div>

      <!-- 返回主页按钮 -->
      <div class="text-center">
        <button
          @click="goToHomePage"
          class="px-8 py-3 bg-gray-500 hover:bg-gray-600 text-white font-bold rounded-lg transition shadow-lg inline-flex items-center gap-2"
        >
          <span>🏠</span>
          <span>返回主页</span>
        </button>
      </div>
    </div>

    <!-- 学习模式界面 -->
    <div v-if="learningMode && currentWord" class="learning-mode max-w-4xl mx-auto">
      <div class="learning-header mb-6 flex justify-between items-center">
        <div class="flex items-center gap-4">
          <h2 class="text-2xl font-bold text-indigo-700">📚 学习模式</h2>
          <button
            @click="exitLearning"
            class="px-4 py-2 bg-gray-400 hover:bg-gray-500 text-white font-semibold rounded-lg transition text-sm"
          >
            ← 退出
          </button>
        </div>
        <div class="progress-info text-gray-600">
          当前: 第 {{ currentWordIndex + 1 }} 个 | 已学习: {{ studiedWords.size }} / {{ currentWords.length }}
        </div>
      </div>

      <!-- 快捷键提示 -->
      <div class="shortcuts-hint bg-indigo-50 border border-indigo-200 rounded-lg p-4 mb-6">
        <div class="flex items-center justify-center gap-6 text-sm text-indigo-700">
          <span class="font-semibold">⌨️ 快捷键：</span>
          <span><kbd class="kbd">←/A</kbd> 上一个</span>
          <span><kbd class="kbd">→/D</kbd> 下一个</span>
          <span><kbd class="kbd">空格</kbd> 标记已学</span>
          <span><kbd class="kbd">R</kbd> 复读</span>
          <span><kbd class="kbd">Enter</kbd> 开始挑战</span>
          <span><kbd class="kbd">ESC</kbd> 退出</span>
        </div>
      </div>

      <div class="word-card bg-white rounded-2xl shadow-2xl p-12">
        <!-- 单词展示 -->
        <div class="word-display text-center mb-8">
          <div class="english-word text-6xl font-bold text-indigo-600 mb-4 font-mono tracking-wide">
            {{ currentWord.word }}
          </div>
          <div class="chinese-def text-3xl text-gray-700 mb-2">
            {{ currentWord.zh_definition }}
          </div>
          <div class="word-meta text-sm text-gray-500 mt-4">
            分类: {{ currentWord.category }} | 难度: {{ getDifficultyText(currentWord.difficulty) }}
          </div>
        </div>

        <!-- 发音按钮 -->
        <div class="pronunciation-section mb-6">
          <button
            @click="playPronunciation(2)"
            :disabled="isPlaying"
            class="w-full py-4 bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-400 text-white text-xl font-bold rounded-xl shadow-lg transition flex items-center justify-center gap-3 hover:scale-105"
          >
            <span class="text-3xl">🔊</span>
            <span>{{ isPlaying ? '播放中...' : '点击听发音 (2次)' }}</span>
          </button>
        </div>

        <!-- 标记已学习按钮 -->
        <div class="mark-studied-section mb-6">
          <button
            @click="markCurrentWordStudied"
            :disabled="studiedWords.has(currentWord.id)"
            class="w-full py-3 transition-all duration-300"
            :class="studiedWords.has(currentWord.id) 
              ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
              : 'bg-green-500 hover:bg-green-600 text-white hover:scale-105 shadow-md'"
          >
            <div class="flex items-center justify-center gap-2 font-bold">
              <span class="text-2xl">{{ studiedWords.has(currentWord.id) ? '✅' : '☑️' }}</span>
              <span>{{ studiedWords.has(currentWord.id) ? '已标记为学习' : '标记为已学习 (空格)' }}</span>
            </div>
          </button>
        </div>

        <!-- 学习提示 -->
        <div class="learning-tips bg-blue-50 rounded-xl p-6 mb-6">
          <h3 class="text-lg font-bold text-blue-700 mb-3">💡 学习提示</h3>
          <ul class="text-gray-700 space-y-2">
            <li>✓ 仔细观察单词拼写</li>
            <li>✓ 多听几遍发音并跟读</li>
            <li>✓ 联想中文释义加深记忆</li>
            <li>✓ 在脑海中拼写一遍</li>
          </ul>
        </div>

        <!-- 操作按钮 -->
        <div class="actions space-y-4">
          <!-- 导航按钮 -->
          <div class="navigation-buttons grid grid-cols-2 gap-4">
            <button
              @click="prevLearningWord"
              :disabled="currentWordIndex === 0"
              class="py-4 bg-gradient-to-r from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 disabled:from-gray-300 disabled:to-gray-300 disabled:cursor-not-allowed text-white text-lg font-bold rounded-xl transition-all transform hover:scale-105 disabled:hover:scale-100 shadow-lg"
            >
              <div class="flex items-center justify-center gap-2">
                <span class="text-xl">←</span>
                <span>上一个</span>
                <span class="text-xs opacity-75">(A)</span>
              </div>
            </button>
            <button
              @click="nextLearningWord"
              :disabled="currentWordIndex >= currentWords.length - 1"
              class="py-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-green-300 disabled:to-green-300 disabled:cursor-not-allowed text-white text-lg font-bold rounded-xl transition-all transform hover:scale-105 disabled:hover:scale-100 shadow-lg"
            >
              <div class="flex items-center justify-center gap-2">
                <span>{{ currentWordIndex >= currentWords.length - 1 ? '已是最后一个' : '下一个' }}</span>
                <span v-if="currentWordIndex < currentWords.length - 1" class="text-xl">→</span>
                <span v-if="currentWordIndex < currentWords.length - 1" class="text-xs opacity-75">(D)</span>
              </div>
            </button>
          </div>

          <!-- 开始挑战按钮 -->
          <button
            v-if="studiedWords.size >= currentWords.length"
            @click="startChallengeMode"
            class="w-full py-4 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white text-xl font-bold rounded-xl transition-all transform hover:scale-105 shadow-lg animate-pulse"
          >
            <div class="flex items-center justify-center gap-2">
              <span class="text-2xl">🎯</span>
              <span>全部学完，开始挑战！</span>
              <span class="text-sm opacity-90">(Enter)</span>
            </div>
          </button>
          <button
            v-else
            @click="startChallengeMode"
            class="w-full py-4 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white text-xl font-bold rounded-xl transition-all transform hover:scale-105 shadow-lg"
          >
            <div class="flex items-center justify-center gap-2">
              <span class="text-2xl">⚡</span>
              <span>直接挑战 (建议学完 {{ currentWords.length }} 个单词)</span>
            </div>
          </button>
        </div>

        <!-- 学习进度条 -->
        <div class="learning-progress mt-6">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>学习进度</span>
            <span>{{ Math.round((studiedWords.size / currentWords.length) * 100) }}%</span>
          </div>
          <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-blue-400 to-indigo-600 transition-all duration-300"
              :style="{ width: `${(studiedWords.size / currentWords.length) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 游戏进行界面 -->
    <div v-if="gameStarted && currentWord && !isGameOver" class="game-play max-w-3xl mx-auto">
      <div class="word-card bg-white rounded-2xl shadow-2xl p-12">
        <!-- 单词信息 -->
        <div class="word-info text-center mb-8">
          <div class="chinese-def text-3xl font-bold text-gray-800 mb-4">
            {{ currentWord.zh_definition }}
          </div>
          <div class="word-category text-sm text-gray-500">
            分类: {{ currentWord.category }} | 难度: {{ getDifficultyText(currentWord.difficulty) }}
          </div>
          <!-- 发音按钮 -->
          <div class="pronunciation-btn mt-4">
            <button
              @click="playPronunciation(1)"
              :disabled="isPlaying"
              class="px-6 py-3 bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-400 text-white rounded-lg shadow transition flex items-center gap-2 mx-auto"
            >
              <span class="text-xl">🔊</span>
              <span>{{ isPlaying ? '播放中...' : '听发音' }}</span>
            </button>
          </div>
        </div>

        <!-- 拼写输入 -->
        <div class="spell-input mb-6">
          <input
            v-model="userInput"
            @keyup.enter="submitSpelling"
            type="text"
            placeholder="请输入英文拼写..."
            class="w-full text-2xl text-center px-6 py-4 border-4 border-indigo-300 rounded-xl focus:border-indigo-500 focus:outline-none"
            :class="{ 'border-green-500': showCorrect, 'border-red-500': showError }"
            :disabled="showFeedback && lastResult?.correct"
            ref="inputRef"
          />
        </div>

        <!-- 反馈信息 -->
        <div v-if="showFeedback" class="feedback mb-6 p-6 rounded-xl" :class="feedbackClass">
          <div v-if="lastResult && lastResult.correct" class="text-center">
            <div class="text-4xl mb-2">✅</div>
            <div class="text-xl font-bold">正确！干得好！</div>
            <div class="text-lg mt-2">+10 积分</div>
            <div class="text-sm mt-3 text-green-700">按 Enter 或点击按钮继续下一题</div>
          </div>
          <div v-else class="text-center">
            <div class="text-4xl mb-2">❌</div>
            <div class="text-xl font-bold">拼写错误,请重新输入正确拼写</div>
            <div class="text-lg mt-2">
              提示: <span class="font-mono text-2xl text-blue-600">{{ lastResult?.correct_word }}</span>
            </div>
            <!-- 差异对比显示 -->
            <div v-if="lastWrongInput" class="mt-4 p-4 bg-white rounded-lg">
              <div class="text-sm text-gray-600 mb-2">你刚才的输入:</div>
              <div class="font-mono text-xl mb-3">
                <span
                  v-for="(part, index) in wordDifference"
                  :key="index"
                  :class="{
                    'text-green-600': part.isCorrect,
                    'text-red-600 line-through': part.isError,
                    'text-blue-600 underline': part.isMissing
                  }"
                >{{ part.text }}</span>
              </div>
              <div class="text-xs text-gray-500">
                <span class="text-green-600">● 正确</span>
                <span class="text-red-600 ml-3">● 错误</span>
                <span class="text-blue-600 ml-3">● 缺少</span>
              </div>
            </div>
            <div class="text-sm mt-3 text-red-600">-1 生命值</div>
            <div class="text-sm mt-2 text-orange-600 font-bold animate-pulse">👇 清空输入框,重新拼写正确后才能继续</div>
          </div>
        </div>

        <!-- 提交按钮 - 正确答案后显示为"下一题" -->
        <button
          v-if="!showFeedback || (showFeedback && !lastResult?.correct)"
          @click="submitSpelling"
          :disabled="!userInput.trim()"
          class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-xl font-bold py-4 rounded-xl transition"
        >
          {{ showFeedback && !lastResult?.correct ? '重新提交' : '提交答案' }}
        </button>

        <!-- 下一题按钮 - 仅在答对后显示 -->
        <button
          v-if="showFeedback && lastResult?.correct"
          @click="goNextWord"
          class="w-full bg-green-600 hover:bg-green-700 text-white text-xl font-bold py-4 rounded-xl transition animate-pulse"
        >
          下一题 → (Enter)
        </button>
      </div>

      <!-- 怪物进度条（视觉效果） -->
      <div class="monster-progress mt-8 bg-white rounded-xl p-6 shadow-lg">
        <div class="flex justify-between items-center mb-3">
          <span class="text-gray-600">怪物进度</span>
          <span class="text-gray-600">{{ 3 - lives }} / 3</span>
        </div>
        <div class="progress-bar h-4 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="progress-fill h-full bg-gradient-to-r from-red-400 to-red-600 transition-all duration-500"
            :style="{ width: `${((3 - lives) / 3) * 100}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- 游戏结束界面 -->
    <div v-if="gameOver" class="game-over max-w-2xl mx-auto">
      <div class="result-card bg-white rounded-2xl shadow-2xl p-12 text-center">
        <div v-if="lives > 0" class="success-result">
          <div class="text-6xl mb-4">🎉</div>
          <h2 class="text-4xl font-bold text-green-600 mb-4">通关成功！</h2>
          <div class="badge text-2xl mb-6">🏆 拼写大师</div>
        </div>
        <div v-else class="fail-result">
          <div class="text-6xl mb-4">💔</div>
          <h2 class="text-4xl font-bold text-red-600 mb-4">挑战失败</h2>
          <div class="text-lg mb-6">不要气馁，继续加油！</div>
        </div>

        <!-- 统计信息 -->
        <div class="stats-summary grid grid-cols-3 gap-4 mb-8">
          <div class="stat bg-blue-50 p-4 rounded-lg">
            <div class="text-3xl font-bold text-blue-600">{{ score }}</div>
            <div class="text-sm text-gray-600">总积分</div>
          </div>
          <div class="stat bg-green-50 p-4 rounded-lg">
            <div class="text-3xl font-bold text-green-600">{{ correctCount }}</div>
            <div class="text-sm text-gray-600">正确数</div>
          </div>
          <div class="stat bg-purple-50 p-4 rounded-lg">
            <div class="text-3xl font-bold text-purple-600">{{ accuracy }}%</div>
            <div class="text-sm text-gray-600">正确率</div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="actions flex flex-col gap-4">
          <button
            @click="backToLearning"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold py-4 rounded-xl transition"
          >
            📚 返回学习模式
          </button>
          <div class="flex gap-4">
            <button
              @click="restartChallenge"
              class="flex-1 bg-green-600 hover:bg-green-700 text-white text-lg font-bold py-3 rounded-xl transition"
            >
              🔄 重新挑战
            </button>
            <button
              @click="backToHome"
              class="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-lg font-bold py-3 rounded-xl transition"
            >
              🏠 选择难度
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useGameStore } from '@/stores/game'
import { useSettingsStore } from '@/stores/settings'
import api from '@/api'
import tts from '@/utils/tts'
import toast from '@/utils/toast'
import { highlightDifferences } from '@/utils/stringDiff'
import LoadingSpinner from './LoadingSpinner.vue'

const gameStore = useGameStore()
const settingsStore = useSettingsStore()
const {
  currentWords,
  currentWordIndex,
  currentWord,
  score,
  lives,
  gameStarted,
  gameOver,
  timeLeft,
  correctCount,
  totalCount,
  accuracy,
  isGameOver,
  learningMode,
  studiedWords
} = storeToRefs(gameStore)

// 本地状态
const userInput = ref('')
const showFeedback = ref(false)
const lastResult = ref(null)
const lastWrongInput = ref('') // 保存错误的输入用于显示差异
const timer = ref(null)
const isPlaying = ref(false)
const autoPlayCount = ref(0) // 自动播放次数
const playQueue = ref([]) // 播放队列
const reviewCount = ref(0) // 待复习单词数量
const isLoading = ref(false) // 加载状态

// 计算属性
const showCorrect = computed(() => showFeedback.value && lastResult.value?.correct)
const showError = computed(() => showFeedback.value && !lastResult.value?.correct)
const feedbackClass = computed(() => {
  if (!showFeedback.value) return ''
  return lastResult.value?.correct ? 'bg-green-50 border-2 border-green-300' : 'bg-red-50 border-2 border-red-300'
})

const wordDifference = computed(() => {
  if (!lastWrongInput.value || !lastResult.value?.correct_word) return []
  return highlightDifferences(lastWrongInput.value, lastResult.value.correct_word)
})

// 方法
function getDifficultyText(level) {
  const map = { 1: '初级', 2: '中级', 3: '高级' }
  return map[level] || '未知'
}

async function playPronunciation(repeat = 1) {
  if (!currentWord.value || isPlaying.value) return
  
  isPlaying.value = true
  try {
    for (let i = 0; i < repeat; i++) {
      await tts.speak(currentWord.value.word)
      if (i < repeat - 1) {
        // 两次播放之间稍微停顿
        await new Promise(resolve => setTimeout(resolve, 500))
      }
    }
  } catch (error) {
    console.error('发音失败:', error)
    alert('发音功能暂不可用，请检查浏览器设置')
  } finally {
    isPlaying.value = false
  }
}

// 自动播放两次发音
async function autoPlayPronunciation() {
  if (learningMode.value && currentWord.value) {
    // 稍微延迟后自动播放
    setTimeout(() => {
      playPronunciation(2)
    }, 300)
  }
}

async function selectDifficulty(level) {
  isLoading.value = true
  try {
    const success = await gameStore.startLearning(level)
    if (!success) {
      toast.error('加载单词失败，请检查词库是否有该难度的单词')
    } else {
      toast.success('单词加载成功！开始学习吧')
    }
  } catch (error) {
    toast.error('加载失败：' + (error.message || '未知错误'))
  } finally {
    isLoading.value = false
  }
}

async function startReviewMode() {
  isLoading.value = true
  try {
    // 调用新的复习模式API
    const words = await api.getReviewWords(settingsStore.wordsPerRound || 10)
    
    if (!words || words.length === 0) {
      toast.warning('暂无需要复习的单词！')
      return
    }
    
    // 使用游戏store加载复习单词
    gameStore.currentWords = words
    gameStore.currentWordIndex = 0
    gameStore.learningMode = true
    gameStore.challengeMode = false
    gameStore.gameStarted = false
    gameStore.studiedWords.clear()
    gameStore.difficulty = 0 // 复习模式没有难度
    
    toast.success(`加载了 ${words.length} 个待复习单词`)
    console.log(`[复习模式] 加载了 ${words.length} 个待复习单词`)
  } catch (error) {
    console.error('加载复习单词失败:', error)
    toast.error('加载复习单词失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}

// 加载待复习单词数量
async function loadReviewCount() {
  try {
    const result = await api.getReviewCount()
    reviewCount.value = result.count
  } catch (error) {
    console.error('获取复习数量失败:', error)
    reviewCount.value = 0
  }
}

function nextLearningWord() {
  // 标记当前单词为已学习
  gameStore.markWordAsStudied()
  // 移动到下一个单词
  gameStore.nextWord()
  // 自动播放新单词的发音
  autoPlayPronunciation()
}

function prevLearningWord() {
  // 返回上一个单词
  gameStore.prevWord()
  // 自动播放发音
  autoPlayPronunciation()
}

function markCurrentWordStudied() {
  // 手动标记当前单词为已学习
  gameStore.markWordAsStudied()
}

// 快捷键处理
function handleKeyPress(event) {
  if (!learningMode.value && !gameStarted.value) return
  
  // 阻止默认行为
  const key = event.key.toLowerCase()
  
  // ESC键退出
  if (key === 'escape') {
    event.preventDefault()
    if (learningMode.value) {
      exitLearning()
    } else if (gameStarted.value) {
      exitChallenge()
    }
    return
  }
  
  if (!learningMode.value) return
  
  if (key === 'arrowright' || key === 'd') {
    // 右箭头或D键：下一个
    event.preventDefault()
    if (currentWordIndex.value < currentWords.value.length - 1) {
      nextLearningWord()
    }
  } else if (key === 'arrowleft' || key === 'a') {
    // 左箭头或A键：上一个
    event.preventDefault()
    if (currentWordIndex.value > 0) {
      prevLearningWord()
    }
  } else if (key === ' ') {
    // 空格键：标记已学习
    event.preventDefault()
    if (!studiedWords.value.has(currentWord.value.id)) {
      markCurrentWordStudied()
    }
  } else if (key === 'r') {
    // R键：复读发音
    event.preventDefault()
    playPronunciation(2)
  } else if (key === 'enter') {
    // Enter键：开始挑战
    event.preventDefault()
    if (studiedWords.value.size >= currentWords.value.length) {
      startChallengeMode()
    }
  }
}

function startChallengeMode() {
  if (studiedWords.value.size < currentWords.value.length) {
    const confirmed = confirm(`你只学习了 ${studiedWords.value.size}/${currentWords.value.length} 个单词，确定要开始挑战吗？`)
    if (!confirmed) return
  }
  
  gameStore.startChallenge()
  startTimer()
}

function exitLearning() {
  const confirmed = confirm('确定要退出学习模式吗？将返回难度选择界面。')
  if (!confirmed) return
  
  gameStore.resetGame()
}

function exitChallenge() {
  const confirmed = confirm('确定要退出挑战吗？将返回学习模式，当前成绩不会保存。')
  if (!confirmed) return
  
  stopTimer()
  // 退出到学习模式
  gameStore.startChallenge() // 先设置为challenge模式
  gameStore.resetGame() // 然后重置
  gameStore.startLearning(gameStore.difficulty) // 重新启动学习模式
}

function backToLearning() {
  // 从游戏结束界面返回学习模式
  stopTimer()
  gameStore.resetGame()
  gameStore.startLearning(gameStore.difficulty)
}

function restartChallenge() {
  // 重新开始挑战（使用相同难度）
  stopTimer()
  gameStore.resetGame()
  gameStore.startLearning(gameStore.difficulty).then(() => {
    startChallengeMode()
  })
}

function backToHome() {
  // 返回难度选择界面
  stopTimer()
  gameStore.resetGame()
}

function goToHomePage() {
  // 返回主页（根路径）
  window.location.href = '/'
}

async function submitSpelling() {
  if (!userInput.value.trim()) return
  
  // 如果已经显示反馈且答错了,说明用户在重新输入
  if (showFeedback.value && !lastResult.value?.correct) {
    // 检查新输入是否正确
    if (userInput.value.toLowerCase().trim() === currentWord.value.word.toLowerCase()) {
      // 拼写正确! 这次不扣分也不加分,直接进入下一题
      lastWrongInput.value = ''
      userInput.value = ''
      showFeedback.value = false
      lastResult.value = null
      gameStore.nextWord()
      
      if (isGameOver.value) {
        stopTimer()
      } else {
        // 自动播放新单词
        if (gameStarted.value && currentWord.value) {
          setTimeout(() => {
            playPronunciation(1)
          }, 300)
        }
      }
      return
    } else {
      // 还是错的,只更新差异显示,不扣生命值
      lastWrongInput.value = userInput.value
      userInput.value = ''
      return
    }
  }

  // 第一次提交答案
  if (!showFeedback.value) {
    const result = await gameStore.submitAnswer(userInput.value)
    if (result) {
      lastResult.value = result
      showFeedback.value = true

      // 如果答对了,保留输入供查看;如果答错了,保存错误输入并清空让用户重新输入
      if (result.correct) {
        // 答对了,不清空输入,保留用户答案供查看
      } else {
        // 答错了,保存错误输入用于差异显示,然后清空输入框
        lastWrongInput.value = userInput.value
        userInput.value = ''
      }

      // 检查游戏是否结束
      if (lives.value <= 0) {
        stopTimer()
        gameStore.endGame()
      }
    }
  }
}

function goNextWord() {
  showFeedback.value = false
  userInput.value = ''
  lastResult.value = null
  lastWrongInput.value = ''
  gameStore.nextWord()

  if (isGameOver.value) {
    stopTimer()
  } else {
    // 挑战模式下自动播放新单词
    if (gameStarted.value && currentWord.value) {
      setTimeout(() => {
        playPronunciation(1)
      }, 300)
    }
  }
}

function startTimer() {
  timer.value = setInterval(() => {
    gameStore.decreaseTime()
    if (timeLeft.value <= 0) {
      stopTimer()
    }
  }, 1000)
}

function stopTimer() {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

onMounted(() => {
  // 添加快捷键监听
  window.addEventListener('keydown', handleKeyPress)
  // 如果是学习模式，自动播放第一个单词
  if (learningMode.value && currentWord.value) {
    autoPlayPronunciation()
  }
  // 加载待复习单词数量
  loadReviewCount()
})

onUnmounted(() => {
  stopTimer()
  // 移除快捷键监听
  window.removeEventListener('keydown', handleKeyPress)
})

// 监听学习模式和挑战模式下的单词变化
import { watch } from 'vue'
watch(
  () => [learningMode.value, gameStarted.value, currentWordIndex.value],
  ([isLearning, isChallenge, index], [wasLearning, wasChallenge, oldIndex]) => {
    // 在学习模式下，单词变化时自动播放
    if (isLearning && currentWord.value && index !== oldIndex) {
      autoPlayPronunciation()
    }
    // 刚进入学习模式时播放第一个
    if (isLearning && !wasLearning && currentWord.value) {
      autoPlayPronunciation()
    }
    // 刚进入挑战模式时播放第一个单词
    if (isChallenge && !wasChallenge && currentWord.value) {
      setTimeout(() => {
        playPronunciation(1)
      }, 300)
    }
  }
)
</script>

<style scoped>
.spell-game-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.difficulty-btn {
  transition: all 0.3s ease;
}

.difficulty-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

input:focus {
  animation: pulse 0.5s ease-in-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

/* 快捷键按钮样式 */
.kbd {
  display: inline-block;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: bold;
  background: white;
  border: 2px solid #4f46e5;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Courier New', monospace;
}
</style>
