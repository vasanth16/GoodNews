<script setup>
import { ref, onMounted } from 'vue'
import { SparklesIcon } from '@heroicons/vue/24/solid'
import { getStats } from '../services/api.js'

const todayCount = ref(null)

async function fetchStats() {
  try {
    const stats = await getStats()
    todayCount.value = stats.today
  } catch (e) {
    // Silently fail
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<template>
  <header class="bg-white border-b border-gray-100 sticky top-0 z-20 backdrop-blur-sm bg-white/95">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-14">
        <!-- Logo & Title -->
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
            <SparklesIcon class="w-5 h-5 text-white" />
          </div>
          <h1 class="text-base font-semibold text-gray-900 leading-tight">
            Something to be hopeful about
          </h1>
        </div>

        <!-- Right side - today's count -->
        <div v-if="todayCount !== null" class="flex items-center gap-2">
          <span class="text-[10px] text-primary-600 bg-primary-50 px-2 py-1 rounded-full font-medium">
            {{ todayCount }} today
          </span>
        </div>
      </div>
    </div>
  </header>
</template>
