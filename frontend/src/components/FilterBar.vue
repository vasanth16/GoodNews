<script setup>
import { computed } from 'vue'

const props = defineProps({
  categories: {
    type: Array,
    default: () => [],
  },
  regions: {
    type: Array,
    default: () => [],
  },
  activeCategory: {
    type: String,
    default: null,
  },
  activeRegion: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['filter-change'])

const categoryColors = {
  environment: 'bg-green-100 text-green-700 hover:bg-green-200',
  health: 'bg-red-100 text-red-700 hover:bg-red-200',
  technology: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
  social: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
  humanitarian: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
  general: 'bg-gray-100 text-gray-600 hover:bg-gray-200',
}

const categoryActiveColors = {
  environment: 'bg-green-500 text-white',
  health: 'bg-red-500 text-white',
  technology: 'bg-blue-500 text-white',
  social: 'bg-purple-500 text-white',
  humanitarian: 'bg-orange-500 text-white',
  general: 'bg-gray-500 text-white',
}

function getCategoryColor(name, isActive) {
  const key = name?.toLowerCase() || 'general'
  if (isActive) {
    return categoryActiveColors[key] || categoryActiveColors.general
  }
  return categoryColors[key] || categoryColors.general
}

function selectCategory(value) {
  emit('filter-change', { type: 'category', value })
}

function selectRegion(value) {
  emit('filter-change', { type: 'region', value })
}

const hasFilters = computed(() => props.categories.length > 0 || props.regions.length > 0)
const hasActiveFilter = computed(() => props.activeCategory || props.activeRegion)
</script>

<template>
  <div v-if="hasFilters" class="mb-4">
    <!-- Categories -->
    <div v-if="categories.length > 0" class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <span class="text-[10px] text-gray-400 uppercase tracking-wide shrink-0">Category</span>

      <button
        @click="selectCategory(null)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          !activeCategory
            ? 'bg-gray-800 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        ]"
      >
        All
      </button>

      <button
        v-for="cat in categories"
        :key="cat.name"
        @click="selectCategory(cat.name)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          getCategoryColor(cat.name, activeCategory === cat.name)
        ]"
      >
        {{ cat.name }}
        <span class="opacity-60 ml-1">{{ cat.count }}</span>
      </button>
    </div>

    <!-- Regions -->
    <div v-if="regions.length > 0" class="flex items-center gap-2 overflow-x-auto pb-2 mt-2 scrollbar-hide">
      <span class="text-[10px] text-gray-400 uppercase tracking-wide shrink-0">Region</span>

      <button
        @click="selectRegion(null)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          !activeRegion
            ? 'bg-gray-800 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        ]"
      >
        All
      </button>

      <button
        v-for="region in regions"
        :key="region.name"
        @click="selectRegion(region.name)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          activeRegion === region.name
            ? 'bg-gray-800 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        ]"
      >
        {{ region.name }}
        <span class="opacity-60 ml-1">{{ region.count }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
