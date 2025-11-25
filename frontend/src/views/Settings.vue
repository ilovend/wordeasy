<template>
  <div class="settings-page min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 p-8">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-8 text-gray-800">{{ $t('settings.title') }}</h1>

      <!-- 语言设置 -->
      <div class="settings-card bg-white rounded-2xl shadow-xl p-8 mb-6">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">🌐 {{ $t('settings.language.title') }}</h2>
        
        <div class="setting-item flex justify-between items-center">
          <label class="text-lg font-semibold text-gray-700">{{ $t('settings.language.select') }}</label>
          <div class="flex gap-3">
            <button
              @click="changeLanguage('zh')"
              :class="[
                'px-6 py-2 rounded-full font-bold transition',
                locale === 'zh'
                  ? 'bg-indigo-500 text-white'
                  : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
              ]"
            >
              🇨🇳 中文
            </button>
            <button
              @click="changeLanguage('en')"
              :class="[
                'px-6 py-2 rounded-full font-bold transition',
                locale === 'en'
                  ? 'bg-indigo-500 text-white'
                  : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
              ]"
            >
              🇬🇧 English
            </button>
          </div>
        </div>
      </div>

      <div class="settings-card bg-white rounded-2xl shadow-xl p-8 mb-6">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">{{ $t('settings.gameParams') }}</h2>

        <!-- 生命值设置 -->
        <div class="setting-item mb-6">
          <div class="flex justify-between items-center mb-2">
            <label class="text-lg font-semibold text-gray-700">❤️ 初始生命值</label>
            <span class="text-2xl font-bold text-red-600">{{ settingsStore.initialLives }}</span>
          </div>
          <input
            v-model.number="settingsStore.initialLives"
            type="range"
            min="1"
            max="10"
            class="w-full h-3 bg-red-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>1 (困难)</span>
            <span>5 (普通)</span>
            <span>10 (简单)</span>
          </div>
        </div>

        <!-- 时间限制 -->
        <div class="setting-item mb-6">
          <div class="flex justify-between items-center mb-2">
            <label class="text-lg font-semibold text-gray-700">⏰ 时间限制（秒）</label>
            <span class="text-2xl font-bold text-blue-600">{{ settingsStore.timeLimit }}s</span>
          </div>
          <input
            v-model.number="settingsStore.timeLimit"
            type="range"
            min="30"
            max="300"
            step="30"
            class="w-full h-3 bg-blue-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>30s (快速)</span>
            <span>90s (标准)</span>
            <span>300s (悠闲)</span>
          </div>
        </div>

        <!-- 每关单词数 -->
        <div class="setting-item mb-6">
          <div class="flex justify-between items-center mb-2">
            <label class="text-lg font-semibold text-gray-700">📝 每关单词数</label>
            <span class="text-2xl font-bold text-purple-600">{{ settingsStore.wordsPerRound }}</span>
          </div>
          <input
            v-model.number="settingsStore.wordsPerRound"
            type="range"
            min="5"
            max="20"
            step="5"
            class="w-full h-3 bg-purple-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>5 (快速)</span>
            <span>10 (标准)</span>
            <span>20 (训练)</span>
          </div>
        </div>

        <!-- 每题得分 -->
        <div class="setting-item mb-6">
          <div class="flex justify-between items-center mb-2">
            <label class="text-lg font-semibold text-gray-700">⭐ 每题得分</label>
            <span class="text-2xl font-bold text-yellow-600">{{ settingsStore.pointsPerCorrect }}</span>
          </div>
          <input
            v-model.number="settingsStore.pointsPerCorrect"
            type="range"
            min="5"
            max="50"
            step="5"
            class="w-full h-3 bg-yellow-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>5</span>
            <span>10 (标准)</span>
            <span>50</span>
          </div>
        </div>
      </div>

      <!-- 音效设置 -->
      <div class="settings-card bg-white rounded-2xl shadow-xl p-8 mb-6">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">🔊 音效设置</h2>

        <div class="setting-item mb-4 flex justify-between items-center">
          <label class="text-lg font-semibold text-gray-700">启用音效</label>
          <button
            @click="settingsStore.enableSound = !settingsStore.enableSound"
            :class="[
              'px-6 py-2 rounded-full font-bold transition',
              settingsStore.enableSound
                ? 'bg-green-500 text-white'
                : 'bg-gray-300 text-gray-600'
            ]"
          >
            {{ settingsStore.enableSound ? '✓ 开启' : '✗ 关闭' }}
          </button>
        </div>

        <div class="setting-item flex justify-between items-center">
          <div>
            <label class="text-lg font-semibold text-gray-700">自动播放发音</label>
            <p class="text-sm text-gray-500">新单词出现时自动播放</p>
          </div>
          <button
            @click="settingsStore.autoPlayAudio = !settingsStore.autoPlayAudio"
            :class="[
              'px-6 py-2 rounded-full font-bold transition',
              settingsStore.autoPlayAudio
                ? 'bg-green-500 text-white'
                : 'bg-gray-300 text-gray-600'
            ]"
          >
            {{ settingsStore.autoPlayAudio ? '✓ 开启' : '✗ 关闭' }}
          </button>
        </div>
      </div>

      <!-- 按钮组 -->
      <div class="flex gap-4 mb-8">
        <button
          @click="saveSettings"
          class="flex-1 bg-green-600 hover:bg-green-700 text-white text-xl font-bold py-4 rounded-xl shadow-lg transition transform hover:scale-105"
        >
          ✓ 保存设置
        </button>
        <button
          @click="resetSettings"
          class="bg-orange-600 hover:bg-orange-700 text-white px-8 py-4 rounded-xl shadow-lg transition"
        >
          🔄 恢复默认
        </button>
      </div>

      <!-- 返回按钮 -->
      <div class="text-center">
        <button
          @click="goBack"
          class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-xl transition"
        >
          ← 返回首页
        </button>
      </div>

      <!-- 保存提示 -->
      <div v-if="showSaveSuccess" class="fixed bottom-8 right-8 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in">
        ✓ 设置已保存
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '@/stores/settings'

const { locale, t } = useI18n()
const settingsStore = useSettingsStore()
const showSaveSuccess = ref(false)

function changeLanguage(lang) {
  locale.value = lang
  localStorage.setItem('wordeasy_locale', lang)
  showSaveSuccess.value = true
  setTimeout(() => {
    showSaveSuccess.value = false
  }, 2000)
}

function saveSettings() {
  settingsStore.saveSettings()
  showSaveSuccess.value = true
  setTimeout(() => {
    showSaveSuccess.value = false
  }, 2000)
}

function resetSettings() {
  if (confirm(t('settings.confirm.reset'))) {
    settingsStore.resetSettings()
    showSaveSuccess.value = true
    setTimeout(() => {
      showSaveSuccess.value = false
    }, 2000)
  }
}

function goBack() {
  window.location.href = '/'
}
</script>

<style scoped>
.settings-page {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4f46e5;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

input[type="range"]::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #4f46e5;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
