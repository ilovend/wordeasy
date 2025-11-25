<template>
  <div class="review-view min-h-screen bg-gradient-to-br from-green-50 to-teal-100 p-8">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-green-700">📚 智能复习</h1>
      
      <!-- 复习说明 -->
      <div class="info-card bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">📅 复习计划</h2>
        <p class="text-gray-600 mb-3">
          基于遗忘曲线算法，系统会智能推送需要复习的单词：
        </p>
        <ul class="list-disc list-inside space-y-2 text-gray-600">
          <li>🔴 陌生词：当天复习3次（间隔1h/3h/6h）</li>
          <li>🟡 熟悉词：次日复习1次，之后按3天/7天/15天间隔</li>
          <li>🟢 掌握词：每周随机抽查1次</li>
        </ul>
      </div>

      <!-- 复习模式选择 -->
      <div class="modes-grid grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- 今日复习 -->
        <button
          @click="startReview('daily')"
          class="mode-card bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">📅</div>
          <h3 class="text-2xl font-bold mb-2">今日复习</h3>
          <p class="text-sm opacity-90">复习今天应该掌握的单词</p>
          <div class="mt-4 text-3xl font-bold">{{ reviewCount }}</div>
          <div class="text-xs opacity-75">待复习单词数</div>
        </button>

        <!-- 错词歼灭战 -->
        <button
          @click="startReview('errors')"
          class="mode-card bg-gradient-to-br from-red-500 to-red-600 text-white rounded-xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">❌</div>
          <h3 class="text-2xl font-bold mb-2">错词歼灭战</h3>
          <p class="text-sm opacity-90">专攻历史错误单词</p>
          <div class="mt-4 text-3xl font-bold">{{ errorCount }}</div>
          <div class="text-xs opacity-75">错词数量</div>
        </button>
      </div>

      <!-- 速拼挑战（可选） -->
      <div class="challenge-card bg-white rounded-xl shadow-lg p-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">⚡ 速拼挑战</h2>
        <p class="text-gray-600 mb-4">10个单词，60秒限时，挑战你的拼写速度！</p>
        <button
          @click="startSpeedChallenge"
          class="w-full bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-4 rounded-lg transition"
        >
          开始速拼挑战
        </button>
      </div>

      <!-- 返回按钮 -->
      <div class="mt-8 text-center">
        <router-link
          to="/"
          class="inline-block bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-lg transition"
        >
          ← 返回首页
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const reviewCount = ref(0)
const errorCount = ref(0)

async function loadCounts() {
  try {
    const [reviewWords, errorWords] = await Promise.all([
      api.getReviewWords(100),
      api.getErrorWords(100)
    ])
    reviewCount.value = reviewWords.length
    errorCount.value = errorWords.length
  } catch (error) {
    console.error('Failed to load counts:', error)
  }
}

function startReview(mode) {
  // 这里可以扩展为专门的复习游戏模式
  // 目前简化为跳转到游戏页面
  alert(`${mode === 'daily' ? '今日复习' : '错词歼灭战'}模式启动！`)
  router.push('/game')
}

function startSpeedChallenge() {
  alert('速拼挑战模式启动！60秒内完成10个单词拼写')
  router.push('/game')
}

onMounted(() => {
  loadCounts()
})
</script>

<style scoped>
.mode-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.mode-card:hover {
  transform: translateY(-5px);
}
</style>
