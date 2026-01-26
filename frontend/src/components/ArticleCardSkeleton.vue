<script setup>
</script>

<template>
  <div
    class="bg-white rounded-lg shadow-sm overflow-hidden flex animate-pulse"
  >
    <!-- Image placeholder -->
    <div class="relative w-28 h-28 sm:w-32 sm:h-32 shrink-0 bg-gray-200 skeleton-shimmer" />

    <!-- Content -->
    <div class="p-3 flex flex-col flex-1 min-w-0">
      <!-- Top row: category + time -->
      <div class="flex items-center gap-2 mb-1.5">
        <div class="h-4 w-16 bg-gray-200 rounded skeleton-shimmer" />
        <div class="h-3 w-8 bg-gray-200 rounded skeleton-shimmer" />
      </div>

      <!-- Headline placeholder (2 lines) -->
      <div class="space-y-1.5 mb-1">
        <div class="h-4 w-full bg-gray-200 rounded skeleton-shimmer" />
        <div class="h-4 w-3/4 bg-gray-200 rounded skeleton-shimmer" />
      </div>

      <!-- Summary placeholder (2 lines) -->
      <div class="space-y-1 flex-1">
        <div class="h-3 w-full bg-gray-100 rounded skeleton-shimmer" />
        <div class="h-3 w-5/6 bg-gray-100 rounded skeleton-shimmer" />
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between mt-2">
        <div class="h-3 w-20 bg-gray-200 rounded skeleton-shimmer" />
        <div class="h-3.5 w-3.5 bg-gray-200 rounded skeleton-shimmer" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeleton-shimmer {
  background: linear-gradient(
    90deg,
    rgb(229 231 235) 0%,
    rgb(243 244 246) 50%,
    rgb(229 231 235) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
