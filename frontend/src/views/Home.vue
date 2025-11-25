<template>
  <div class="home-container min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center p-8">
    <div class="home-content max-w-4xl mx-auto text-center">
      <!-- Logo和标题 -->
      <div class="hero mb-12">
        <div class="text-7xl mb-4">📖✨</div>
        <h1 class="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-4">
          WordEasy
        </h1>
        <p class="text-2xl text-gray-600 mb-2">拼写攻防战</p>
        <p class="text-lg text-gray-500">用游戏化的方式，轻松掌握英语拼写</p>
      </div>

      <!-- 用户进度卡片 -->
      <div class="progress-card bg-white rounded-2xl shadow-xl p-8 mb-12">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">🎯 我的进度</h2>
        <div class="grid grid-cols-3 gap-6">
          <div class="stat-item">
            <div class="text-4xl font-bold text-indigo-600">Lv.{{ level }}</div>
            <div class="text-sm text-gray-600 mt-2">当前等级</div>
          </div>
          <div class="stat-item">
            <div class="text-4xl font-bold text-yellow-600">{{ coins }}</div>
            <div class="text-sm text-gray-600 mt-2">金币数</div>
          </div>
          <div class="stat-item">
            <div class="text-4xl font-bold text-green-600">{{ mastery['绿'] || 0 }}</div>
            <div class="text-sm text-gray-600 mt-2">掌握单词</div>
          </div>
        </div>
        
        <!-- 掌握度分布 -->
        <div class="mastery-distribution mt-6 pt-6 border-t border-gray-200">
          <div class="flex justify-around text-center">
            <div>
              <div class="text-2xl font-bold text-red-500">🔴 {{ mastery['红'] || 0 }}</div>
              <div class="text-xs text-gray-500">陌生</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-yellow-500">🟡 {{ mastery['黄'] || 0 }}</div>
              <div class="text-xs text-gray-500">熟悉</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-green-500">🟢 {{ mastery['绿'] || 0 }}</div>
              <div class="text-xs text-gray-500">掌握</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能入口 -->
      <div class="features-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- 开始闯关 -->
        <router-link
          to="/game"
          class="feature-card bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">🎮</div>
          <h3 class="text-2xl font-bold mb-2">开始闯关</h3>
          <p class="text-sm opacity-90">挑战拼写攻防战，消灭怪物获得积分</p>
        </router-link>

        <!-- 速拼挑战 -->
        <router-link
          to="/speed"
          class="feature-card bg-gradient-to-br from-orange-500 to-red-600 text-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">⚡</div>
          <h3 class="text-2xl font-bold mb-2">速拼挑战</h3>
          <p class="text-sm opacity-90">60秒极限挑战，挑战你的反应速度</p>
        </router-link>

        <!-- 复习模式 -->
        <router-link
          to="/review"
          class="feature-card bg-gradient-to-br from-green-500 to-emerald-600 text-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">📚</div>
          <h3 class="text-2xl font-bold mb-2">复习模式</h3>
          <p class="text-sm opacity-90">智能复习计划，巩固已学单词</p>
        </router-link>

        <!-- 词库管理 -->
        <router-link
          to="/library"
          class="feature-card bg-gradient-to-br from-purple-500 to-pink-600 text-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transform hover:scale-105 transition"
        >
          <div class="text-5xl mb-4">📖</div>
          <h3 class="text-2xl font-bold mb-2">词库管理</h3>
          <p class="text-sm opacity-90">查看词库、上传自定义单词</p>
        </router-link>
      </div>

      <!-- 设置按钮（右下角） -->
      <div class="mt-8 flex justify-center">
        <router-link
          to="/settings"
          class="settings-btn bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-xl shadow-lg hover:shadow-2xl transition transform hover:scale-105 flex items-center gap-2"
        >
          <span class="text-2xl">⚙️</span>
          <span class="font-bold">游戏设置</span>
        </router-link>
      </div>

      <!-- 说明文字 -->
      <div class="info-text mt-8 text-gray-500 text-sm">
        <p>💡 基于科学的遗忘曲线算法，帮助您高效记忆单词</p>
        <p class="mt-2">🎯 每天坚持学习，轻松提升词汇量</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useProgressStore } from '@/stores/progress'

const progressStore = useProgressStore()
const { level, coins, mastery } = storeToRefs(progressStore)

onMounted(async () => {
  await progressStore.fetchProgress()
})
</script>

<style scoped>
.home-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.feature-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-8px) scale(1.02);
}
</style>
