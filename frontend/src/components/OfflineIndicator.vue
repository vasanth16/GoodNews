<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { WifiIcon } from '@heroicons/vue/20/solid'

const isOffline = ref(!navigator.onLine)

function handleOnline() {
  isOffline.value = false
}

function handleOffline() {
  isOffline.value = true
}

onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>

<template>
  <Transition name="slide-down">
    <div
      v-if="isOffline"
      class="fixed top-0 left-0 right-0 bg-amber-500 text-white z-50 shadow-md"
    >
      <div class="container mx-auto px-4 py-2 max-w-5xl">
        <div class="flex items-center justify-center gap-2 text-sm font-medium">
          <WifiIcon class="w-4 h-4" />
          <span>You're offline — showing cached content</span>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: transform 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
}
</style>
