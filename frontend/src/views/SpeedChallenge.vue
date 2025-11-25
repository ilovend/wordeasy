<template>
  <div class="speed-challenge min-h-screen bg-gradient-to-br from-orange-50 to-red-100 p-8">
    <!-- 开始界面 -->
    <div v-if="!gameStarted && !gameOver" class="start-screen max-w-2xl mx-auto">
      <h1 class="text-5xl font-bold text-center mb-6 text-orange-700">⚡ 速拼挑战</h1>
      <p class="text-center text-gray-700 text-lg mb-12">
        挑战你的极限！10个单词，60秒倒计时，看你能答对几个！
      </p>

      <div class="difficulty-select grid grid-cols-3 gap-4 mb-8">
        <button
          v-for="level in [1, 2, 3]"
          :key="level"
          @click="selectedDifficulty = level"
          :class="[
            'py-4 px-6 rounded-xl font-bold transition',
            selectedDifficulty === level
              ? 'bg-orange-600 text-white scale-105'
              : 'bg-white text-gray-700 hover:bg-orange-100'
          ]"
        >
          {{ ['初级', '中级', '高级'][level - 1] }}
        </button>
      </div>

      <button
        @click="startChallenge"
        class="w-full bg-orange-600 hover:bg-orange-700 text-white text-2xl font-bold py-6 rounded-xl shadow-lg transition transform hover:scale-105"
      >
        🚀 开始挑战
      </button>

      <div v-if="bestScore > 0" class="mt-8 text-center">
        <div class="inline-block bg-white px-8 py-4 rounded-xl shadow">
          <div class="text-sm text-gray-600">最高纪录</div>
          <div class="text-3xl font-bold text-orange-600">{{ bestScore }} / 10</div>
        </div>
      </div>
    </div>

    <!-- 游戏进行中 -->
    <div v-if="gameStarted && !gameOver" class="game-active max-w-3xl mx-auto">
      <!-- 顶部状态栏 -->
      <div class="stats-bar mb-8 flex justify-between items-center bg-white px-6 py-4 rounded-xl shadow-lg">
        <div class="text-2xl font-bold text-orange-600">
          ⏱️ {{ timeLeft }}s
        </div>
        <div class="text-2xl font-bold text-green-600">
          ✅ {{ correctCount }} / {{ currentIndex + 1 }}
        </div>
        <div class="text-xl text-gray-600">
          进度: {{ currentIndex + 1 }} / 10
        </div>
      </div>

      <!-- 单词卡片 -->
      <div class="word-card bg-white rounded-2xl shadow-2xl p-12">
        <div class="text-center mb-8">
          <div class="text-4xl font-bold text-gray-800 mb-4">
            {{ currentWord?.zh_definition }}
          </div>
          <button
            @click="playSound"
            :disabled="isPlaying"
            class="px-6 py-3 bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white rounded-lg transition"
          >
            🔊 {{ isPlaying ? '播放中...' : '听发音' }}
          </button>
        </div>

        <input
          ref="inputRef"
          v-model="userInput"
          @keyup.enter="submitAnswer"
          type="text"
          placeholder="快速输入英文..."
          class="w-full text-3xl text-center px-6 py-4 border-4 border-orange-300 rounded-xl focus:border-orange-500 focus:outline-none"
          :class="{ 'border-green-500 bg-green-50': showCorrect, 'border-red-500 bg-red-50': showError }"
        />

        <div class="mt-6 flex gap-4">
          <button
            @click="submitAnswer"
            :disabled="!userInput.trim()"
            class="flex-1 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-400 text-white text-xl font-bold py-4 rounded-xl transition"
          >
            提交答案
          </button>
          <button
            @click="skipWord"
            class="bg-gray-500 hover:bg-gray-600 text-white px-8 py-4 rounded-xl transition"
          >
            跳过
          </button>
        </div>

        <!-- 即时反馈 -->
        <div v-if="feedback" class="mt-6 text-center py-3 rounded-lg" :class="feedback.class">
          <span class="text-2xl">{{ feedback.icon }}</span>
          <span class="ml-2 text-xl font-bold">{{ feedback.text }}</span>
        </div>
      </div>
    </div>

    <!-- 结果界面 -->
    <div v-if="gameOver" class="result-screen max-w-2xl mx-auto">
      <div class="bg-white rounded-2xl shadow-2xl p-12 text-center">
        <div class="text-6xl mb-6">
          {{ correctCount >= 8 ? '🏆' : correctCount >= 5 ? '👍' : '💪' }}
        </div>
        <h2 class="text-4xl font-bold mb-4 text-gray-800">挑战完成！</h2>
        
        <div class="score-display mb-8">
          <div class="text-6xl font-bold text-orange-600 mb-2">
            {{ correctCount }} / 10
          </div>
          <div class="text-xl text-gray-600">
            正确率: {{ Math.round((correctCount / 10) * 100) }}%
          </div>
          <div class="text-lg text-gray-500 mt-2">
            用时: {{ 60 - timeLeft }} 秒
          </div>
        </div>

        <div v-if="isNewRecord" class="mb-6 py-3 bg-yellow-50 rounded-lg">
          <span class="text-2xl">🎉</span>
          <span class="ml-2 text-xl font-bold text-yellow-700">新纪录！</span>
        </div>

        <div class="flex gap-4">
          <button
            @click="restartChallenge"
            class="flex-1 bg-orange-600 hover:bg-orange-700 text-white text-xl font-bold py-4 rounded-xl transition"
          >
            🔄 再来一次
          </button>
          <button
            @click="goHome"
            class="flex-1 bg-gray-600 hover:bg-gray-700 text-white text-xl font-bold py-4 rounded-xl transition"
          >
            🏠 返回首页
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import api from '@/api'
import tts from '@/utils/tts'

const selectedDifficulty = ref(2)
const gameStarted = ref(false)
const gameOver = ref(false)
const words = ref([])
const currentIndex = ref(0)
const currentWord = ref(null)
const userInput = ref('')
const correctCount = ref(0)
const timeLeft = ref(60)
const timer = ref(null)
const inputRef = ref(null)
const isPlaying = ref(false)
const feedback = ref(null)
const showCorrect = ref(false)
const showError = ref(false)
const bestScore = ref(0)
const isNewRecord = ref(false)

onMounted(() => {
  // 从本地存储加载最高纪录
  const saved = localStorage.getItem('speedChallenge_bestScore')
  if (saved) {
    bestScore.value = parseInt(saved)
  }
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})

async function startChallenge() {
  try {
    const data = await api.getWords(selectedDifficulty.value, 10)
    if (data && data.length >= 10) {
      words.value = data.slice(0, 10)
      currentIndex.value = 0
      currentWord.value = words.value[0]
      correctCount.value = 0
      timeLeft.value = 60
      gameStarted.value = true
      gameOver.value = false
      isNewRecord.value = false
      
      startTimer()
      nextTick(() => {
        inputRef.value?.focus()
      })
    }
  } catch (error) {
    console.error('加载单词失败:', error)
    alert('加载单词失败，请稍后重试')
  }
}

function startTimer() {
  timer.value = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      endChallenge()
    }
  }, 1000)
}

function submitAnswer() {
  if (!userInput.value.trim()) return

  const isCorrect = userInput.value.trim().toLowerCase() === currentWord.value.word.toLowerCase()
  
  if (isCorrect) {
    correctCount.value++
    showCorrect.value = true
    feedback.value = { icon: '✅', text: '正确！', class: 'bg-green-100 text-green-700' }
  } else {
    showError.value = true
    feedback.value = { icon: '❌', text: `答案: ${currentWord.value.word}`, class: 'bg-red-100 text-red-700' }
  }

  setTimeout(() => {
    nextWord()
  }, 800)
}

function skipWord() {
  feedback.value = { icon: '⏭️', text: '已跳过', class: 'bg-gray-100 text-gray-700' }
  setTimeout(() => {
    nextWord()
  }, 500)
}

function nextWord() {
  userInput.value = ''
  showCorrect.value = false
  showError.value = false
  feedback.value = null
  currentIndex.value++

  if (currentIndex.value >= 10) {
    endChallenge()
  } else {
    currentWord.value = words.value[currentIndex.value]
    inputRef.value?.focus()
  }
}

function endChallenge() {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }

  gameStarted.value = false
  gameOver.value = true

  // 检查是否创造新纪录
  if (correctCount.value > bestScore.value) {
    bestScore.value = correctCount.value
    isNewRecord.value = true
    localStorage.setItem('speedChallenge_bestScore', bestScore.value.toString())
  }
}

function restartChallenge() {
  gameOver.value = false
  startChallenge()
}

function goHome() {
  window.location.href = '/'
}

async function playSound() {
  if (!currentWord.value || isPlaying.value) return
  
  isPlaying.value = true
  try {
    await tts.speak(currentWord.value.word)
  } catch (error) {
    console.error('发音失败:', error)
  } finally {
    isPlaying.value = false
  }
}
</script>

<style scoped>
.speed-challenge {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
