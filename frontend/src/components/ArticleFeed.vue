<script setup>
import { onMounted } from 'vue'
import { useArticles } from '../composables/useArticles.js'
import ArticleCard from './ArticleCard.vue'
import LoadingSpinner from './LoadingSpinner.vue'
import ErrorMessage from './ErrorMessage.vue'

const {
  articles,
  loading,
  error,
  hasMore,
  total,
  fetchArticles,
  loadMore,
} = useArticles()

onMounted(() => {
  if (articles.value.length === 0) {
    fetchArticles(true)
  }
})

function handleRetry() {
  fetchArticles(true)
}
</script>

<template>
  <div>
    <!-- Results count -->
    <p v-if="!loading && articles.length > 0" class="text-sm text-gray-500 mb-4">
      Showing {{ articles.length }} of {{ total }} articles
    </p>

    <!-- Error state -->
    <ErrorMessage
      v-if="error && !loading"
      :message="error"
      :retryable="true"
      @retry="handleRetry"
      class="mb-6"
    />

    <!-- Loading state (initial) -->
    <LoadingSpinner
      v-if="loading && articles.length === 0"
      text="Loading articles..."
    />

    <!-- Articles grid -->
    <TransitionGroup
      v-else-if="articles.length > 0"
      name="articles"
      tag="div"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </TransitionGroup>

    <!-- Empty state -->
    <div
      v-else-if="!loading && !error"
      class="text-center py-12"
    >
      <p class="text-gray-500 text-lg">No articles found</p>
      <p class="text-gray-400 text-sm mt-2">Try adjusting your filters or check back later</p>
    </div>

    <!-- Load more -->
    <div v-if="articles.length > 0" class="mt-8 text-center">
      <button
        v-if="hasMore && !loading"
        @click="loadMore"
        class="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
      >
        Load More
      </button>

      <LoadingSpinner
        v-else-if="loading"
        text="Loading more..."
      />

      <p v-else class="text-gray-400 text-sm">
        You've reached the end
      </p>
    </div>
  </div>
</template>

<style scoped>
.articles-enter-active {
  transition: all 0.3s ease-out;
}

.articles-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.articles-leave-active {
  transition: all 0.2s ease-in;
}

.articles-leave-to {
  opacity: 0;
}
</style>
