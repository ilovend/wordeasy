import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocaleStore = defineStore('locale', () => {
  const locale = ref(localStorage.getItem('wordeasy_locale') || 'zh')

  function setLocale(newLocale) {
    locale.value = newLocale
    localStorage.setItem('wordeasy_locale', newLocale)
  }

  return {
    locale,
    setLocale
  }
})
