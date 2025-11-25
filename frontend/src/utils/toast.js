/**
 * Toast 通知工具
 * 用于显示临时提示信息
 */

export const toast = {
  container: null,

  init() {
    if (this.container) return
    
    this.container = document.createElement('div')
    this.container.className = 'toast-container'
    this.container.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
      pointer-events: none;
    `
    document.body.appendChild(this.container)
  },

  show(message, type = 'info', duration = 3000) {
    this.init()

    const toast = document.createElement('div')
    toast.className = `toast toast-${type}`
    
    const colors = {
      success: 'bg-green-500',
      error: 'bg-red-500',
      warning: 'bg-orange-500',
      info: 'bg-blue-500'
    }

    const icons = {
      success: '✓',
      error: '✗',
      warning: '⚠',
      info: 'ℹ'
    }

    toast.innerHTML = `
      <div class="${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg flex items-center gap-3 animate-slide-in" style="pointer-events: auto; min-width: 250px; max-width: 500px;">
        <span class="text-xl font-bold">${icons[type]}</span>
        <span class="flex-1">${message}</span>
      </div>
    `

    this.container.appendChild(toast)

    // 添加动画样式
    if (!document.getElementById('toast-styles')) {
      const style = document.createElement('style')
      style.id = 'toast-styles'
      style.textContent = `
        @keyframes slide-in {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @keyframes slide-out {
          from {
            transform: translateX(0);
            opacity: 1;
          }
          to {
            transform: translateX(100%);
            opacity: 0;
          }
        }
        .animate-slide-in {
          animation: slide-in 0.3s ease-out;
        }
        .animate-slide-out {
          animation: slide-out 0.3s ease-out;
        }
      `
      document.head.appendChild(style)
    }

    // 自动移除
    setTimeout(() => {
      const inner = toast.querySelector('div')
      inner.classList.remove('animate-slide-in')
      inner.classList.add('animate-slide-out')
      
      setTimeout(() => {
        toast.remove()
        if (this.container.children.length === 0) {
          this.container.remove()
          this.container = null
        }
      }, 300)
    }, duration)
  },

  success(message, duration) {
    this.show(message, 'success', duration)
  },

  error(message, duration) {
    this.show(message, 'error', duration)
  },

  warning(message, duration) {
    this.show(message, 'warning', duration)
  },

  info(message, duration) {
    this.show(message, 'info', duration)
  }
}

export default toast
