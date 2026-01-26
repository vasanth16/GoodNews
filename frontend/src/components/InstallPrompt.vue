<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePWA } from '../composables/usePWA.js'
import { XMarkIcon, ArrowDownTrayIcon } from '@heroicons/vue/20/solid'

const { isInstallable, isInstalled, install } = usePWA()

const dismissed = ref(false)
const STORAGE_KEY = 'pwa-install-dismissed'

onMounted(() => {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) {
    const { timestamp } = JSON.parse(stored)
    // Show again after 7 days
    if (Date.now() - timestamp < 7 * 24 * 60 * 60 * 1000) {
      dismissed.value = true
    }
  }
})

const shouldShow = computed(() => {
  return isInstallable.value && !isInstalled.value && !dismissed.value
})

function dismiss() {
  dismissed.value = true
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ timestamp: Date.now() }))
}

async function handleInstall() {
  const success = await install()
  if (success) {
    dismissed.value = true
  }
}
</script>

<template>
  <Transition name="slide">
    <div
      v-if="shouldShow"
      class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 shadow-lg z-50 safe-bottom"
    >
      <div class="container mx-auto px-4 py-3 max-w-5xl">
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center shrink-0">
              <ArrowDownTrayIcon class="w-5 h-5 text-white" />
            </div>
            <div class="min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">Install the app</p>
              <p class="text-xs text-gray-500 truncate">Quick access from your home screen</p>
            </div>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <button
              @click="handleInstall"
              class="px-4 py-2 bg-blue-500 text-white text-sm font-medium rounded-lg hover:bg-blue-600 transition-colors"
            >
              Install
            </button>
            <button
              @click="dismiss"
              class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Dismiss"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.safe-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateY(100%);
}
</style>
