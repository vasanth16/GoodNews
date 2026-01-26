<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message: {
    type: String,
    default: '',
  },
  visible: {
    type: Boolean,
    default: false,
  },
  duration: {
    type: Number,
    default: 3000,
  },
})

const emit = defineEmits(['close'])

const isShowing = ref(false)
let timeoutId = null

watch(() => props.visible, (newVal) => {
  if (newVal) {
    isShowing.value = true
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      isShowing.value = false
      emit('close')
    }, props.duration)
  } else {
    isShowing.value = false
  }
}, { immediate: true })
</script>

<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="isShowing"
        class="toast"
      >
        <span>{{ message }}</span>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.toast {
  position: fixed;
  bottom: 5rem;
  left: 50%;
  transform: translateX(-50%);
  background-color: #1f2937;
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
}

.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.2s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translate(-50%, 1rem);
}

.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 1rem);
}
</style>
