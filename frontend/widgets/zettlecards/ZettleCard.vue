<template>
  <div
    class="absolute w-80 transform overflow-hidden rounded-lg bg-white p-4 shadow-md hover:shadow-lg"
    :style="{
      transform: `translate(${card.x}px, ${card.y}px)`,
      cursor: isDragging ? 'grabbing' : 'grab',
    }"
    @mousedown.stop="$emit('dragStart', $event)">
    <!-- Card Type Badge -->
    <span
      class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize"
      :class="cardTypeClasses">
      {{ card.card_type }}
    </span>

    <!-- Card Title -->
    <h3 class="mt-2 text-lg font-medium text-gray-900">
      {{ card.title || 'Untitled Card' }}
    </h3>

    <!-- Card Content -->
    <div class="mt-3">
      <p v-if="card.text" class="line-clamp-3 text-gray-600">{{ card.text }}</p>
      <img
        v-if="card.image && !hasImageError"
        :src="card.image"
        class="h-48 w-full rounded object-cover"
        :alt="card.title || 'Card image'"
        @error="handleImageError" />
      <a v-if="card.url" :href="card.url" class="break-all text-blue-600 hover:text-blue-800">
        {{ card.url }}
      </a>
    </div>

    <!-- Card Footer -->
    <div class="mt-4 flex items-center text-sm text-gray-500">
      <span v-if="card.created_at" class="mr-4">
        {{ new Date(card.created_at).toLocaleDateString() }}
      </span>
      <span v-if="card.votes" class="flex items-center">
        <svg class="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z" />
        </svg>
        {{ card.votes }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

interface ZettleCard {
  uuid: string
  card_type: 'text' | 'image' | 'url' | 'model' | 'topic'
  title: string
  text?: string
  image?: string
  url?: string
  created_at?: string
  votes?: number
  x: number
  y: number
}

const props = defineProps<{
  card: ZettleCard
  isDragging?: boolean
}>()

defineEmits<{
  dragStart: [event: MouseEvent]
}>()

const hasImageError = ref(false)

const cardTypeClasses = computed(
  () =>
    ({
      text: 'bg-blue-100 text-blue-800',
      image: 'bg-green-100 text-green-800',
      url: 'bg-purple-100 text-purple-800',
      model: 'bg-yellow-100 text-yellow-800',
      topic: 'bg-red-100 text-red-800',
    })[props.card.card_type]
)

function handleImageError() {
  hasImageError.value = true
}
</script>
