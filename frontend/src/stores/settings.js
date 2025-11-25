/**
 * 游戏设置Store
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSettingsStore = defineStore('settings', () => {
  // 游戏设置
  const initialLives = ref(3) // 初始生命值
  const timeLimit = ref(90) // 时间限制（秒）
  const wordsPerRound = ref(10) // 每关单词数
  const pointsPerCorrect = ref(10) // 每题得分
  const enableSound = ref(true) // 是否启用音效
  const autoPlayAudio = ref(false) // 是否自动播放发音

  // 从localStorage加载设置
  function loadSettings() {
    const saved = localStorage.getItem('game_settings')
    if (saved) {
      try {
        const settings = JSON.parse(saved)
        initialLives.value = settings.initialLives || 3
        timeLimit.value = settings.timeLimit || 90
        wordsPerRound.value = settings.wordsPerRound || 10
        pointsPerCorrect.value = settings.pointsPerCorrect || 10
        enableSound.value = settings.enableSound !== false
        autoPlayAudio.value = settings.autoPlayAudio || false
      } catch (e) {
        console.error('加载设置失败:', e)
      }
    }
  }

  // 保存设置到localStorage
  function saveSettings() {
    const settings = {
      initialLives: initialLives.value,
      timeLimit: timeLimit.value,
      wordsPerRound: wordsPerRound.value,
      pointsPerCorrect: pointsPerCorrect.value,
      enableSound: enableSound.value,
      autoPlayAudio: autoPlayAudio.value
    }
    localStorage.setItem('game_settings', JSON.stringify(settings))
  }

  // 重置为默认设置
  function resetSettings() {
    initialLives.value = 3
    timeLimit.value = 90
    wordsPerRound.value = 10
    pointsPerCorrect.value = 10
    enableSound.value = true
    autoPlayAudio.value = false
    saveSettings()
  }

  // 初始化时加载设置
  loadSettings()

  return {
    initialLives,
    timeLimit,
    wordsPerRound,
    pointsPerCorrect,
    enableSound,
    autoPlayAudio,
    loadSettings,
    saveSettings,
    resetSettings
  }
})
