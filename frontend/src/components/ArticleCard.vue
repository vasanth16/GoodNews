<script setup>
import { computed } from 'vue'
import { ArrowTopRightOnSquareIcon } from '@heroicons/vue/20/solid'

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
})

const categoryColors = {
  environment: 'bg-green-100 text-green-800',
  health: 'bg-red-100 text-red-800',
  technology: 'bg-blue-100 text-blue-800',
  social: 'bg-purple-100 text-purple-800',
  humanitarian: 'bg-orange-100 text-orange-800',
  general: 'bg-gray-100 text-gray-800',
}

const categoryColor = computed(() => {
  const cat = props.article.category?.toLowerCase() || 'general'
  return categoryColors[cat] || categoryColors.general
})

function formatRelativeTime(dateString) {
  if (!dateString) return ''

  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffSeconds = Math.floor(diffMs / 1000)
  const diffMinutes = Math.floor(diffSeconds / 60)
  const diffHours = Math.floor(diffMinutes / 60)
  const diffDays = Math.floor(diffHours / 24)
  const diffWeeks = Math.floor(diffDays / 7)

  if (diffSeconds < 60) return 'just now'
  if (diffMinutes < 60) return `${diffMinutes} minute${diffMinutes === 1 ? '' : 's'} ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`
  if (diffDays < 7) return `${diffDays} day${diffDays === 1 ? '' : 's'} ago`
  if (diffWeeks < 4) return `${diffWeeks} week${diffWeeks === 1 ? '' : 's'} ago`

  return date.toLocaleDateString()
}

const relativeTime = computed(() => formatRelativeTime(props.article.published_at))

const fallbackImage = 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80'
</script>

<template>
  <article
    class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden flex flex-col"
  >
    <!-- Image -->
    <div class="relative aspect-video bg-gray-100">
      <img
        :src="article.image_url || fallbackImage"
        :alt="article.headline"
        class="w-full h-full object-cover"
        loading="lazy"
        @error="(e) => e.target.src = fallbackImage"
      />
      <!-- Category badge -->
      <span
        v-if="article.category"
        :class="[categoryColor, 'absolute top-3 left-3 px-2 py-1 text-xs font-medium rounded-full']"
      >
        {{ article.category }}
      </span>
    </div>

    <!-- Content -->
    <div class="p-4 flex flex-col flex-1">
      <!-- Time -->
      <p class="text-xs text-gray-500 mb-2">
        {{ relativeTime }}
      </p>

      <!-- Headline -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 leading-snug">
        <a
          :href="article.source_url"
          target="_blank"
          rel="noopener noreferrer"
          class="hover:text-primary-600 transition-colors"
        >
          {{ article.headline }}
        </a>
      </h3>

      <!-- Summary -->
      <p class="text-sm text-gray-600 mb-4 line-clamp-3 flex-1">
        {{ article.summary?.replace(/<[^>]*>/g, '') }}
      </p>

      <!-- Footer -->
      <div class="flex items-center justify-between pt-3 border-t border-gray-100">
        <span class="text-xs text-gray-500">{{ article.source_name }}</span>
        <a
          :href="article.source_url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-gray-400 hover:text-primary-600 transition-colors"
          title="Open article"
        >
          <ArrowTopRightOnSquareIcon class="w-4 h-4" />
        </a>
      </div>
    </div>
  </article>
</template>
