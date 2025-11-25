/**
 * Pinia状态管理 - 游戏状态
 * 优化：添加错误处理、重试机制、性能优化
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'
import { useSettingsStore } from './settings'

export const useGameStore = defineStore('game', () => {
  const settingsStore = useSettingsStore()
  
  // 状态
  const currentWords = ref([])
  const currentWordIndex = ref(0)
  const score = ref(0)
  const lives = ref(3)
  const difficulty = ref(1)
  const gameStarted = ref(false)
  const gameOver = ref(false)
  const timeLeft = ref(90)
  const correctCount = ref(0)
  const totalCount = ref(0)
  const loading = ref(false)
  const error = ref(null)
  const learningMode = ref(false) // 学习模式标志
  const challengeMode = ref(false) // 挑战模式标志
  const studiedWords = ref(new Set()) // 已学习的单词ID集合

  // 计算属性
  const currentWord = computed(() => {
    return currentWords.value[currentWordIndex.value] || null
  })

  const accuracy = computed(() => {
    if (totalCount.value === 0) return 0
    return Math.round((correctCount.value / totalCount.value) * 100)
  })

  const isGameOver = computed(() => {
    return lives.value <= 0 || currentWordIndex.value >= currentWords.value.length
  })

  // 方法
  async function startGame(selectedDifficulty, retryCount = 0) {
    loading.value = true
    error.value = null
    
    try {
      difficulty.value = selectedDifficulty
      const words = await api.getWords(selectedDifficulty, settingsStore.wordsPerRound)
      
      console.log(`[DEBUG] 请求 ${settingsStore.wordsPerRound} 个单词，实际收到 ${words.length} 个单词`)
      
      if (!words || words.length === 0) {
        throw new Error(`难度${selectedDifficulty}没有可用的单词，请先上传词库`)
      }
      
      currentWords.value = words
      currentWordIndex.value = 0
      score.value = 0
      lives.value = settingsStore.initialLives
      gameStarted.value = true
      gameOver.value = false
      timeLeft.value = settingsStore.timeLimit
      correctCount.value = 0
      totalCount.value = 0
      loading.value = false
      return true
    } catch (err) {
      console.error('Failed to start game:', err)
      error.value = err.message || '加载单词失败'
      loading.value = false
      
      // 重试机制（1次）
      if (retryCount < 1) {
        console.log('正在重试...')
        return startGame(selectedDifficulty, retryCount + 1)
      }
      return false
    }
  }

  async function submitAnswer(userInput) {
    if (!currentWord.value) return null

    try {
      const result = await api.checkSpelling(currentWord.value.id, userInput)
      totalCount.value++

      if (result.correct) {
        correctCount.value++
        score.value += settingsStore.pointsPerCorrect
      } else {
        lives.value--
      }

      return result
    } catch (err) {
      console.error('Failed to check spelling:', err)
      error.value = '检查拼写失败，请重试'
      return null
    }
  }

  function nextWord() {
    if (currentWordIndex.value < currentWords.value.length - 1) {
      currentWordIndex.value++
      error.value = null
    } else if (!learningMode.value) {
      // 只在挑战模式中自动结束游戏
      endGame()
    }
  }

  function prevWord() {
    // 返回上一个单词（学习模式专用）
    if (currentWordIndex.value > 0) {
      currentWordIndex.value--
      error.value = null
    }
  }

  function endGame() {
    gameStarted.value = false
    gameOver.value = true
  }

  function startLearning(selectedDifficulty) {
    // 启动学习模式
    return startGame(selectedDifficulty).then(success => {
      if (success) {
        learningMode.value = true
        challengeMode.value = false
        gameStarted.value = false // 学习模式不计入游戏开始
        studiedWords.value.clear()
      }
      return success
    })
  }

  function markWordAsStudied() {
    // 标记当前单词为已学习
    if (currentWord.value) {
      studiedWords.value.add(currentWord.value.id)
      
      // 同步到数据库
      api.markWordStudied(currentWord.value.id).catch(err => {
        console.error('标记学习失败:', err)
        // 不影响用户体验，静默失败
      })
    }
  }

  function startChallenge() {
    // 从学习模式切换到挑战模式
    learningMode.value = false
    challengeMode.value = true
    gameStarted.value = true
    currentWordIndex.value = 0
    score.value = 0
    lives.value = settingsStore.initialLives
    timeLeft.value = settingsStore.timeLimit
    correctCount.value = 0
    totalCount.value = 0
    error.value = null
  }

  function resetGame() {
    currentWords.value = []
    currentWordIndex.value = 0
    score.value = 0
    lives.value = 3
    gameStarted.value = false
    gameOver.value = false
    timeLeft.value = 90
    correctCount.value = 0
    totalCount.value = 0
    loading.value = false
    error.value = null
    learningMode.value = false
    challengeMode.value = false
    studiedWords.value.clear()
  }

  function decreaseTime() {
    if (timeLeft.value > 0) {
      timeLeft.value--
    } else {
      endGame()
    }
  }

  return {
    // 状态
    currentWords,
    currentWordIndex,
    score,
    lives,
    difficulty,
    gameStarted,
    gameOver,
    timeLeft,
    correctCount,
    totalCount,
    loading,
    error,
    learningMode,
    challengeMode,
    studiedWords,
    // 计算属性
    currentWord,
    accuracy,
    isGameOver,
    // 方法
    startGame,
    startLearning,
    startChallenge,
    markWordAsStudied,
    submitAnswer,
    nextWord,
    prevWord,
    endGame,
    resetGame,
    decreaseTime
  }
})
