<template>
  <div class="statistics-page min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">{{ $t('statistics.title') }}</h1>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-blue-500 border-solid"></div>
      </div>

      <!-- 统计卡片 -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
        <!-- 学习等级 -->
        <div class="stat-card bg-white rounded-2xl shadow-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-600 mb-2">{{ $t('statistics.level.title') }}</h3>
              <p class="text-4xl font-bold text-blue-600">{{ stats.level }}</p>
            </div>
            <div class="bg-blue-100 rounded-full p-4">
              <span class="text-2xl">🎓</span>
            </div>
          </div>
        </div>

        <!-- 金币数量 -->
        <div class="stat-card bg-white rounded-2xl shadow-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-600 mb-2">{{ $t('statistics.coins.title') }}</h3>
              <p class="text-4xl font-bold text-yellow-600">{{ stats.coins }}</p>
            </div>
            <div class="bg-yellow-100 rounded-full p-4">
              <span class="text-2xl">💰</span>
            </div>
          </div>
        </div>

        <!-- 总单词数 -->
        <div class="stat-card bg-white rounded-2xl shadow-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-600 mb-2">{{ $t('statistics.totalWords.title') }}</h3>
              <p class="text-4xl font-bold text-green-600">{{ stats.total_words }}</p>
            </div>
            <div class="bg-green-100 rounded-full p-4">
              <span class="text-2xl">📚</span>
            </div>
          </div>
        </div>

        <!-- 已复习单词 -->
        <div class="stat-card bg-white rounded-2xl shadow-xl p-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-semibold text-gray-600 mb-2">{{ $t('statistics.reviewedWords.title') }}</h3>
              <p class="text-4xl font-bold text-purple-600">{{ stats.reviewed_words }}</p>
            </div>
            <div class="bg-purple-100 rounded-full p-4">
              <span class="text-2xl">✅</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 掌握度统计 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ $t('statistics.mastery.title') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="mastery-item p-4 rounded-xl bg-red-50 border border-red-200">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-red-700">{{ $t('statistics.mastery.beginner') }}</h3>
              <span class="text-2xl">🔴</span>
            </div>
            <div class="text-3xl font-bold text-red-600">{{ stats.mastery.红 || 0 }}</div>
          </div>
          <div class="mastery-item p-4 rounded-xl bg-yellow-50 border border-yellow-200">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-yellow-700">{{ $t('statistics.mastery.intermediate') }}</h3>
              <span class="text-2xl">🟡</span>
            </div>
            <div class="text-3xl font-bold text-yellow-600">{{ stats.mastery.黄 || 0 }}</div>
          </div>
          <div class="mastery-item p-4 rounded-xl bg-green-50 border border-green-200">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-green-700">{{ $t('statistics.mastery.advanced') }}</h3>
              <span class="text-2xl">🟢</span>
            </div>
            <div class="text-3xl font-bold text-green-600">{{ stats.mastery.绿 || 0 }}</div>
          </div>
        </div>
      </div>

      <!-- 最近7天学习趋势 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ $t('statistics.recent.title') }}</h2>
        <div class="h-64">
          <canvas ref="recentChart"></canvas>
        </div>
      </div>

      <!-- 难度分布 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ $t('statistics.difficulty.title') }}</h2>
        <div class="h-64">
          <canvas ref="difficultyChart"></canvas>
        </div>
      </div>

      <!-- 错误率 -->
      <div class="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ $t('statistics.errorRate.title') }}</h2>
        <div class="flex items-center justify-center h-64">
          <div class="relative">
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="text-center">
                <div class="text-4xl font-bold text-red-600">{{ stats.error_rate }}%</div>
                <div class="text-gray-600">{{ $t('statistics.errorRate.label') }}</div>
              </div>
            </div>
            <canvas ref="errorChart" width="200" height="200"></canvas>
          </div>
        </div>
      </div>

      <!-- 返回按钮 -->
      <div class="text-center">
        <button
          @click="goBack"
          class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-xl transition"
        >
          ← {{ $t('common.back') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import api from '@/api'

const loading = ref(true)
const stats = ref({
  level: 1,
  coins: 0,
  mastery: {
    红: 0,
    黄: 0,
    绿: 0
  },
  difficulty_distribution: {
    level1: 0,
    level2: 0,
    level3: 0
  },
  total_words: 0,
  reviewed_words: 0,
  error_words: 0,
  error_rate: 0,
  recent_stats: []
})

// 图表引用
const recentChart = ref(null)
const difficultyChart = ref(null)
const errorChart = ref(null)

// 图表实例
let recentChartInstance = null
let difficultyChartInstance = null
let errorChartInstance = null

// 获取统计数据
async function fetchStats() {
  try {
    loading.value = true
    const data = await api.getProgress()
    stats.value = data
    initCharts()
  } catch (error) {
    console.error('Failed to fetch statistics:', error)
  } finally {
    loading.value = false
  }
}

// 初始化图表
function initCharts() {
  // 确保Chart.js已加载
  if (typeof Chart === 'undefined') {
    console.error('Chart.js is not loaded')
    return
  }

  // 销毁现有图表实例
  if (recentChartInstance) {
    recentChartInstance.destroy()
  }
  if (difficultyChartInstance) {
    difficultyChartInstance.destroy()
  }
  if (errorChartInstance) {
    errorChartInstance.destroy()
  }

  // 最近7天学习趋势图
  if (recentChart.value) {
    recentChartInstance = new Chart(recentChart.value, {
      type: 'line',
      data: {
        labels: stats.value.recent_stats.map(item => item.date),
        datasets: [{
          label: $t('statistics.recent.reviewed'),
          data: stats.value.recent_stats.map(item => item.reviewed),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }

  // 难度分布图
  if (difficultyChart.value) {
    difficultyChartInstance = new Chart(difficultyChart.value, {
      type: 'bar',
      data: {
        labels: [$t('statistics.difficulty.beginner'), $t('statistics.difficulty.intermediate'), $t('statistics.difficulty.advanced')],
        datasets: [{
          label: $t('statistics.difficulty.label'),
          data: [
            stats.value.difficulty_distribution.level1 || 0,
            stats.value.difficulty_distribution.level2 || 0,
            stats.value.difficulty_distribution.level3 || 0
          ],
          backgroundColor: ['#34d399', '#fbbf24', '#f87171']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    })
  }

  // 错误率环形图
  if (errorChart.value) {
    errorChartInstance = new Chart(errorChart.value, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [stats.value.error_rate, 100 - stats.value.error_rate],
          backgroundColor: ['#ef4444', '#e5e7eb'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '75%',
        plugins: {
          legend: {
            display: false
          }
        }
      }
    })
  }
}

// 返回首页
function goBack() {
  window.location.href = '/'
}

// 生命周期钩子
onMounted(() => {
  // 动态加载Chart.js
  const script = document.createElement('script')
  script.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js'
  script.onload = () => {
    fetchStats()
  }
  document.head.appendChild(script)
})

onUnmounted(() => {
  // 销毁图表实例
  if (recentChartInstance) {
    recentChartInstance.destroy()
  }
  if (difficultyChartInstance) {
    difficultyChartInstance.destroy()
  }
  if (errorChartInstance) {
    errorChartInstance.destroy()
  }
})
</script>

<style scoped>
.statistics-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stat-card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.mastery-item {
  transition: transform 0.2s ease-in-out;
}

.mastery-item:hover {
  transform: translateY(-3px);
}
</style>