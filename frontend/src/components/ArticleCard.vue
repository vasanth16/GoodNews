<script setup>
import { ref, computed } from 'vue'
import { ArrowTopRightOnSquareIcon, ShareIcon } from '@heroicons/vue/20/solid'
import Toast from './Toast.vue'
import HopeLevel from './HopeLevel.vue'

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
})

const categoryColors = {
  environment: 'bg-green-100 text-green-700',
  health: 'bg-red-100 text-red-700',
  technology: 'bg-blue-100 text-blue-700',
  social: 'bg-purple-100 text-purple-700',
  humanitarian: 'bg-orange-100 text-orange-700',
  general: 'bg-gray-100 text-gray-600',
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

  if (diffSeconds < 60) return 'now'
  if (diffMinutes < 60) return `${diffMinutes}m`
  if (diffHours < 24) return `${diffHours}h`
  if (diffDays < 7) return `${diffDays}d`

  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const relativeTime = computed(() => formatRelativeTime(props.article.published_at))

const fallbackImage = 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&q=80'

const cleanSummary = computed(() => {
  return props.article.summary?.replace(/<[^>]*>/g, '').substring(0, 150) || ''
})

// Share functionality
const showToast = ref(false)
const toastMessage = ref('')

async function handleShare() {
  const shareData = {
    title: props.article.headline,
    text: cleanSummary.value,
    url: props.article.source_url,
  }

  if (navigator.share) {
    try {
      await navigator.share(shareData)
    } catch (err) {
      if (err.name !== 'AbortError') {
        copyToClipboard()
      }
    }
  } else {
    copyToClipboard()
  }
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(props.article.source_url)
    toastMessage.value = 'Link copied!'
    showToast.value = true
  } catch {
    toastMessage.value = 'Failed to copy'
    showToast.value = true
  }
}
</script>

<template>
  <article
    class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-200 overflow-hidden flex"
  >
    <!-- Image -->
    <div class="relative w-28 h-28 sm:w-32 sm:h-32 shrink-0 bg-gray-100">
      <img
        :src="article.image_url || fallbackImage"
        :alt="article.headline"
        class="w-full h-full object-cover"
        loading="lazy"
        @error="(e) => e.target.src = fallbackImage"
      />
    </div>

    <!-- Content -->
    <div class="p-3 flex flex-col flex-1 min-w-0">
      <!-- Top row: hope level + category + time -->
      <div class="flex items-center gap-1.5 mb-1.5 flex-wrap">
        <HopeLevel :score="article.hopefulness_score" />
        <span
          v-if="article.category"
          :class="[categoryColor, 'px-1.5 py-0.5 text-[10px] font-medium rounded']"
        >
          {{ article.category }}
        </span>
        <span class="text-[10px] text-gray-400">{{ relativeTime }}</span>
      </div>

      <!-- Headline -->
      <h3 class="text-sm font-semibold text-gray-900 leading-tight line-clamp-2 mb-1">
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
      <p class="text-xs text-gray-500 line-clamp-2 flex-1">
        {{ cleanSummary }}
      </p>

      <!-- Footer -->
      <div class="flex items-center justify-between mt-2">
        <span class="text-[10px] text-gray-400">{{ article.source_name }}</span>
        <div class="flex items-center gap-2">
          <button
            @click="handleShare"
            class="text-gray-300 hover:text-primary-600 transition-colors"
            title="Share article"
          >
            <ShareIcon class="w-3.5 h-3.5" />
          </button>
          <a
            :href="article.source_url"
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-300 hover:text-primary-600 transition-colors"
            title="Open article"
          >
            <ArrowTopRightOnSquareIcon class="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>

    <!-- Toast notification -->
    <Toast
      :message="toastMessage"
      :visible="showToast"
      @close="showToast = false"
    />
  </article>
</template>
