<template>
  <div v-if="loading" class="loading-overlay" :class="{ 'loading-fullscreen': fullscreen }">
    <div class="loading-spinner">
      <div class="spinner-circle"></div>
      <p v-if="message" class="loading-message">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: ''
  },
  fullscreen: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  border-radius: 0.5rem;
}

.loading-fullscreen {
  position: fixed;
  border-radius: 0;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-circle {
  width: 50px;
  height: 50px;
  border: 4px solid #e0e0e0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-message {
  color: #4b5563;
  font-size: 0.875rem;
  font-weight: 500;
}
</style>
