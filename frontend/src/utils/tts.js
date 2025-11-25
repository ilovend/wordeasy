/**
 * TTS 发音工具（使用 Web Speech API）
 */

class TTSService {
  constructor() {
    this.synth = window.speechSynthesis
    this.voice = null
    this.initialized = false
    this.initVoice()
  }

  /**
   * 初始化英语语音
   */
  initVoice() {
    if (!this.synth) {
      console.warn('浏览器不支持 Web Speech API')
      return
    }

    // 等待语音列表加载
    const loadVoices = () => {
      const voices = this.synth.getVoices()
      
      // 优先选择美式英语
      this.voice = voices.find(v => v.lang === 'en-US') ||
                   voices.find(v => v.lang.startsWith('en-')) ||
                   voices[0]
      
      if (this.voice) {
        this.initialized = true
        console.log('TTS 初始化成功:', this.voice.name, this.voice.lang)
      }
    }

    // 有些浏览器需要异步加载语音列表
    if (this.synth.getVoices().length > 0) {
      loadVoices()
    } else {
      this.synth.addEventListener('voiceschanged', loadVoices)
    }
  }

  /**
   * 播放单词发音
   * @param {string} word - 要朗读的单词
   * @param {number} rate - 语速（0.5-2，默认0.9）
   * @param {number} pitch - 音调（0-2，默认1）
   */
  speak(word, rate = 0.9, pitch = 1) {
    if (!this.synth) {
      console.warn('浏览器不支持语音合成')
      return Promise.reject(new Error('不支持语音合成'))
    }

    // 停止当前播放
    this.synth.cancel()

    return new Promise((resolve, reject) => {
      const utterance = new SpeechSynthesisUtterance(word)
      
      if (this.voice) {
        utterance.voice = this.voice
      }
      
      utterance.lang = 'en-US'
      utterance.rate = rate
      utterance.pitch = pitch
      utterance.volume = 1

      utterance.onend = () => resolve()
      utterance.onerror = (e) => {
        console.error('TTS 错误:', e)
        reject(e)
      }

      this.synth.speak(utterance)
    })
  }

  /**
   * 停止当前播放
   */
  stop() {
    if (this.synth) {
      this.synth.cancel()
    }
  }

  /**
   * 检查是否支持 TTS
   */
  isSupported() {
    return !!this.synth && this.initialized
  }
}

// 导出单例
export default new TTSService()
