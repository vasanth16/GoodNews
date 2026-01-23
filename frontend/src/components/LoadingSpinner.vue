<script setup>
defineProps({
  text: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12">
    <div
      class="w-10 h-10 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"
    ></div>
    <p v-if="text" class="mt-4 text-sm text-gray-500">
      {{ text }}
    </p>
  </div>
</template>
