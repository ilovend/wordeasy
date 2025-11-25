/**
 * Pinia状态管理 - 用户进度
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

export const useProgressStore = defineStore('progress', () => {
  // 状态
  const level = ref(1)
  const coins = ref(0)
  const mastery = ref({ 红: 0, 黄: 0, 绿: 0 })

  // 方法
  async function fetchProgress() {
    try {
      const data = await api.getProgress()
      level.value = data.level
      coins.value = data.coins
      mastery.value = data.mastery
    } catch (error) {
      console.error('Failed to fetch progress:', error)
    }
  }

  function updateCoins(amount) {
    coins.value += amount
  }

  return {
    level,
    coins,
    mastery,
    fetchProgress,
    updateCoins
  }
})
