import { createI18n } from 'vue-i18n'
import zh from './locales/zh.json'
import en from './locales/en.json'

// 获取浏览器语言或本地存储的语言设置
const getDefaultLocale = () => {
  const saved = localStorage.getItem('wordeasy_locale')
  if (saved) return saved
  
  const browserLang = navigator.language || navigator.userLanguage
  if (browserLang.startsWith('zh')) return 'zh'
  return 'en'
}

const i18n = createI18n({
  legacy: false, // 使用 Composition API 模式
  locale: getDefaultLocale(),
  fallbackLocale: 'en',
  messages: {
    zh,
    en
  }
})

export default i18n
