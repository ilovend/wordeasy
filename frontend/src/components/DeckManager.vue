<template>
  <div class="deck-manager-modal fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="modal-content bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="modal-header bg-gradient-to-r from-purple-600 to-pink-600 p-6 rounded-t-2xl">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold text-white">
            {{ isEdit ? '✏️ 编辑词库' : '➕ 创建新词库' }}
          </h2>
          <button @click="$emit('close')" class="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <div class="modal-body p-6 space-y-6">
        <!-- 基本信息 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">📚</span>
            基本信息
          </h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">
                词库名称 <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.name"
                type="text"
                placeholder="例如：考研核心词汇"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">词库描述</label>
              <textarea
                v-model="form.description"
                rows="3"
                placeholder="简要描述这个词库的内容和用途"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              ></textarea>
            </div>
          </div>
        </div>

        <!-- 学习设置 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">🎯</span>
            学习设置
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">每日新学数量</label>
              <input
                v-model.number="form.daily_new_limit"
                type="number"
                min="1"
                max="1000"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              />
              <p class="text-xs text-gray-500 mt-1">建议：20-100个</p>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">新学批次数量</label>
              <input
                v-model.number="form.new_batch_size"
                type="number"
                min="1"
                max="100"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              />
              <p class="text-xs text-gray-500 mt-1">每次学习的单词数</p>
            </div>
          </div>
        </div>

        <!-- 语言设置 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">🌍</span>
            语言设置
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">目标语言</label>
              <select
                v-model="form.target_language"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                <option value="英语">英语</option>
                <option value="日语">日语</option>
                <option value="中文(普通话)">中文(普通话)</option>
                <option value="韩语">韩语</option>
                <option value="德语">德语</option>
                <option value="法语">法语</option>
                <option value="西班牙语">西班牙语</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">发音人</label>
              <select
                v-model="form.voice_type"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                <option value="默认">默认</option>
                <option value="美音" :disabled="form.target_language !== '英语'">美音</option>
                <option value="英音" :disabled="form.target_language !== '英语'">英音</option>
                <option value="母语">母语</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 词库类型 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">📖</span>
            词库类型
          </h3>
          <div class="grid grid-cols-3 gap-3">
            <button
              v-for="type in deckTypes"
              :key="type.value"
              @click="form.deck_type = type.value"
              :class="[
                'p-4 rounded-lg border-2 transition-all',
                form.deck_type === type.value
                  ? 'border-purple-600 bg-purple-50 text-purple-700'
                  : 'border-gray-300 hover:border-purple-300'
              ]"
            >
              <div class="text-2xl mb-2">{{ type.icon }}</div>
              <div class="font-semibold">{{ type.label }}</div>
            </button>
          </div>
        </div>

        <!-- 记忆算法 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">🧠</span>
            记忆算法
          </h3>
          <div class="space-y-3">
            <label
              v-for="algo in algorithms"
              :key="algo.value"
              class="flex items-start p-4 border-2 rounded-lg cursor-pointer transition-all hover:bg-gray-50"
              :class="form.algorithm === algo.value ? 'border-purple-600 bg-purple-50' : 'border-gray-300'"
            >
              <input
                type="radio"
                :value="algo.value"
                v-model="form.algorithm"
                class="mt-1 mr-3"
              />
              <div class="flex-1">
                <div class="font-semibold text-gray-800">{{ algo.label }}</div>
                <div class="text-sm text-gray-600 mt-1">{{ algo.description }}</div>
              </div>
            </label>
          </div>
        </div>

        <!-- 优先级设置 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">⚡</span>
            优先级设置
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">新学优先级</label>
              <select
                v-model="form.new_priority"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                <option value="默认">默认（按顺序）</option>
                <option value="随机">随机</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">复习优先级</label>
              <select
                v-model="form.review_priority"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500"
              >
                <option value="默认">默认（按遗忘曲线）</option>
                <option value="随机">随机</option>
              </select>
            </div>
          </div>
        </div>

        <!-- 重复过滤 -->
        <div class="section">
          <h3 class="text-lg font-bold text-gray-800 mb-4 flex items-center">
            <span class="text-2xl mr-2">🔄</span>
            重复过滤
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <button
              @click="form.duplicate_filter = '过滤'"
              :class="[
                'p-4 rounded-lg border-2 transition-all',
                form.duplicate_filter === '过滤'
                  ? 'border-purple-600 bg-purple-50'
                  : 'border-gray-300 hover:border-purple-300'
              ]"
            >
              <div class="font-semibold">🚫 过滤重复</div>
              <div class="text-sm text-gray-600 mt-1">自动跳过已存在的单词</div>
            </button>
            <button
              @click="form.duplicate_filter = '允许'"
              :class="[
                'p-4 rounded-lg border-2 transition-all',
                form.duplicate_filter === '允许'
                  ? 'border-purple-600 bg-purple-50'
                  : 'border-gray-300 hover:border-purple-300'
              ]"
            >
              <div class="font-semibold">✅ 允许重复</div>
              <div class="text-sm text-gray-600 mt-1">允许相同单词出现</div>
            </button>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="modal-footer bg-gray-50 p-6 rounded-b-2xl flex gap-3">
        <button
          @click="$emit('close')"
          class="flex-1 px-6 py-3 border-2 border-gray-300 rounded-lg font-semibold text-gray-700 hover:bg-gray-100 transition"
        >
          取消
        </button>
        <button
          @click="handleSubmit"
          :disabled="!form.name || saving"
          class="flex-1 px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
        >
          {{ saving ? '保存中...' : (isEdit ? '保存修改' : '创建词库') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  deck: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const isEdit = ref(!!props.deck)
const saving = ref(false)

const form = ref({
  name: '',
  description: '',
  daily_new_limit: 100,
  new_batch_size: 30,
  target_language: '英语',
  voice_type: '默认',
  deck_type: '单词库',
  algorithm: 'FSRS',
  new_priority: '默认',
  review_priority: '默认',
  duplicate_filter: '过滤'
})

const deckTypes = [
  { value: '单词库', label: '单词库', icon: '📚' },
  { value: '课程库', label: '课程库', icon: '📖' },
  { value: '自定义', label: '自定义', icon: '✨' }
]

const algorithms = [
  {
    value: 'FSRS',
    label: 'FSRS (推荐)',
    description: '自由间隔重复调度器，基于记忆遗忘规律动态调整复习时间'
  },
  {
    value: 'StepMaster',
    label: 'StepMaster',
    description: '阶梯式学习算法，固定间隔：1天→3天→7天→15天'
  },
  {
    value: 'SM-2',
    label: 'SM-2',
    description: 'SuperMemo 2算法，经典的间隔重复算法'
  }
]

// 如果是编辑模式，填充数据
if (props.deck) {
  Object.assign(form.value, props.deck)
}

// 监听目标语言变化，自动调整发音人
watch(() => form.value.target_language, (newLang) => {
  if (newLang !== '英语' && (form.value.voice_type === '美音' || form.value.voice_type === '英音')) {
    form.value.voice_type = '默认'
  }
})

async function handleSubmit() {
  if (!form.value.name) {
    alert('请输入词库名称')
    return
  }
  
  saving.value = true
  try {
    emit('submit', form.value)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.deck-manager-modal {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 滚动条样式 */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
