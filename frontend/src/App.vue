<script setup>
import ArticleFeed from './components/ArticleFeed.vue'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-primary-600 text-white py-6 shadow-lg">
      <div class="container mx-auto px-4">
        <h1 class="text-3xl font-bold">Bright World News</h1>
        <p class="text-primary-100 mt-1">Good news from around the world</p>
      </div>
    </header>
    <main class="container mx-auto px-4 py-8">
      <ArticleFeed />
    </main>
  </div>
</template>
