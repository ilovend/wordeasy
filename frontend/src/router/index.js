import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Game from '@/views/Game.vue'
import WordLibrary from '@/views/WordLibrary.vue'
import Review from '@/views/Review.vue'
import SpeedChallenge from '@/views/SpeedChallenge.vue'
import Settings from '@/views/Settings.vue'
import Statistics from '@/views/Statistics.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/game',
    name: 'Game',
    component: Game
  },
  {
    path: '/library',
    name: 'WordLibrary',
    component: WordLibrary
  },
  {
    path: '/review',
    name: 'Review',
    component: Review
  },
  {
    path: '/speed',
    name: 'SpeedChallenge',
    component: SpeedChallenge
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
