import { ref, reactive } from 'vue'
import { getArticles } from '../services/api.js'

const articles = ref([])
const loading = ref(false)
const error = ref(null)
const hasMore = ref(true)
const total = ref(0)

const filters = reactive({
  category: null,
  region: null,
  minScore: null,
})

const PAGE_SIZE = 12

export function useArticles() {
  async function fetchArticles(reset = false) {
    if (loading.value) return

    if (reset) {
      articles.value = []
      hasMore.value = true
      error.value = null
    }

    loading.value = true
    error.value = null

    try {
      const offset = reset ? 0 : articles.value.length
      const response = await getArticles({
        limit: PAGE_SIZE,
        offset,
        category: filters.category,
        region: filters.region,
        minScore: filters.minScore,
      })

      if (reset) {
        articles.value = response.articles
      } else {
        articles.value = [...articles.value, ...response.articles]
      }

      total.value = response.total
      hasMore.value = response.has_more
    } catch (err) {
      error.value = err.message || 'Failed to load articles'
    } finally {
      loading.value = false
    }
  }

  async function loadMore() {
    if (!hasMore.value || loading.value) return
    await fetchArticles(false)
  }

  function setFilter(type, value) {
    if (filters[type] !== value) {
      filters[type] = value
      fetchArticles(true)
    }
  }

  function clearFilters() {
    filters.category = null
    filters.region = null
    filters.minScore = null
    fetchArticles(true)
  }

  return {
    articles,
    loading,
    error,
    hasMore,
    total,
    filters,
    fetchArticles,
    loadMore,
    setFilter,
    clearFilters,
  }
}
