import { API_BASE_URL } from '../config.js'

class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    const data = await response.json().catch(() => null)

    if (!response.ok) {
      throw new ApiError(
        data?.detail || `Request failed with status ${response.status}`,
        response.status,
        data
      )
    }

    return data
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(
      error.message || 'Network error occurred',
      0,
      null
    )
  }
}

export async function getArticles({ limit = 20, offset = 0, category, region, minScore } = {}) {
  const params = new URLSearchParams()
  params.set('limit', limit)
  params.set('offset', offset)

  if (category) params.set('category', category)
  if (region) params.set('region', region)
  if (minScore !== undefined) params.set('min_score', minScore)

  return request(`/api/articles?${params}`)
}

export async function getArticle(id) {
  return request(`/api/articles/${id}`)
}

export async function getCategories() {
  return request('/api/articles/categories')
}

export async function getRegions() {
  return request('/api/articles/regions')
}

export async function triggerFetch() {
  return request('/api/articles/fetch', { method: 'POST' })
}
