<template>
  <div class="min-h-screen bg-gray-500">
    <header class="bg-white shadow-sm">
      <div class="mx-auto max-w-7xl px-4 py-4 sm:px-6 lg:px-8">
        <h1 class="text-2xl font-semibold text-gray-900">Zettle Cards</h1>
      </div>
    </header>

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- Loading State -->
      <div v-if="loading" class="py-8 text-center">
        <div class="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-gray-900"></div>
        <p class="mt-2 text-gray-600">Loading cards...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading cards</h3>
            <p class="mt-1 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Cards Grid -->
      <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="card in cards"
          :key="card.uuid"
          class="overflow-hidden rounded-lg bg-white shadow transition-shadow duration-200 hover:shadow-md">
          <div class="px-4 py-5 sm:p-6">
            <!-- Card Type Badge -->
            <span
              class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize"
              :class="{
                'bg-blue-100 text-blue-800': card.card_type === 'text',
                'bg-green-100 text-green-800': card.card_type === 'image',
                'bg-purple-100 text-purple-800': card.card_type === 'url',
                'bg-yellow-100 text-yellow-800': card.card_type === 'model',
                'bg-red-100 text-red-800': card.card_type === 'topic',
              }">
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
                v-if="card.image"
                :src="card.image"
                class="h-48 w-full rounded object-cover"
                :alt="card.title" />
              <a
                v-if="card.url"
                :href="card.url"
                class="break-all text-blue-600 hover:text-blue-800">
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
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const cards = ref([])
const loading = ref(true)
const error = ref(null)

const fetchCards = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/cards/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    cards.value = data.results || data // handle both paginated and non-paginated responses
  } catch (e) {
    error.value = e.message
    console.error('Error fetching cards:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCards()
})
</script>
