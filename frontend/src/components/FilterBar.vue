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
  activeMinScore: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['filter-change'])

const categoryColors = {
  environment: 'bg-teal-100 text-teal-700 hover:bg-teal-200',
  health: 'bg-pink-100 text-pink-700 hover:bg-pink-200',
  technology: 'bg-indigo-100 text-indigo-700 hover:bg-indigo-200',
  social: 'bg-violet-100 text-violet-700 hover:bg-violet-200',
  humanitarian: 'bg-lime-100 text-lime-700 hover:bg-lime-200',
  general: 'bg-gray-100 text-gray-600 hover:bg-gray-200',
}

const categoryActiveColors = {
  environment: 'bg-teal-500 text-white',
  health: 'bg-pink-500 text-white',
  technology: 'bg-indigo-500 text-white',
  social: 'bg-violet-500 text-white',
  humanitarian: 'bg-lime-500 text-white',
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

function selectMinScore(value) {
  emit('filter-change', { type: 'minScore', value })
}

const ratingLevels = [
  { min: 90, label: 'Radiant', color: 'bg-amber-100 text-amber-700 hover:bg-amber-200', activeColor: 'bg-amber-500 text-white' },
  { min: 80, label: 'Inspiring', color: 'bg-rose-100 text-rose-700 hover:bg-rose-200', activeColor: 'bg-rose-500 text-white' },
  { min: 70, label: 'Uplifting', color: 'bg-sky-100 text-sky-700 hover:bg-sky-200', activeColor: 'bg-sky-500 text-white' },
  { min: 60, label: 'Hopeful', color: 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200', activeColor: 'bg-emerald-500 text-white' },
]

const hasFilters = computed(() => props.categories.length > 0 || props.regions.length > 0)
const hasActiveFilter = computed(() => props.activeCategory || props.activeRegion || props.activeMinScore)
</script>

<template>
  <div v-if="hasFilters" class="mb-4">
    <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
      <!-- Categories -->
      <template v-if="categories.length > 0">
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

        <span class="text-gray-300 shrink-0">|</span>
      </template>

      <!-- Rating Levels -->
      <span class="text-[10px] text-gray-400 uppercase tracking-wide shrink-0">Level</span>

      <button
        @click="selectMinScore(null)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          !activeMinScore
            ? 'bg-gray-800 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        ]"
      >
        All
      </button>

      <button
        v-for="level in ratingLevels"
        :key="level.min"
        @click="selectMinScore(level.min)"
        :class="[
          'px-2.5 py-1 text-xs font-medium rounded-full transition-colors shrink-0',
          activeMinScore === level.min ? level.activeColor : level.color
        ]"
      >
        {{ level.label }}+
      </button>

      <!-- Regions -->
      <template v-if="regions.length > 0">
        <span class="text-gray-300 shrink-0">|</span>
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
      </template>
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
