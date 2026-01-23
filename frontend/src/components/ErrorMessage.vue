<script setup>
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'

defineProps({
  message: {
    type: String,
    required: true,
  },
  retryable: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['retry'])
</script>

<template>
  <div class="rounded-lg bg-red-50 border border-red-200 p-4">
    <div class="flex items-start">
      <ExclamationTriangleIcon class="w-5 h-5 text-red-500 mt-0.5 shrink-0" />
      <div class="ml-3 flex-1">
        <p class="text-sm text-red-800">
          {{ message }}
        </p>
        <button
          v-if="retryable"
          @click="emit('retry')"
          class="mt-3 text-sm font-medium text-red-700 hover:text-red-800 underline underline-offset-2"
        >
          Try Again
        </button>
      </div>
    </div>
  </div>
</template>
