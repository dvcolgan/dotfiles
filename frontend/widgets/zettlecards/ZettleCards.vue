<template>
  <div
    ref="container"
    class="fixed inset-0 overflow-hidden bg-green-700"
    @mousedown="startPan"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @wheel.prevent="handleZoom">
    <div
      class="relative h-full w-full"
      :style="{
        transform: `translate(${viewX}px, ${viewY}px) scale(${zoom})`,
        transformOrigin: '0 0',
      }">
      <!-- Origin indicator (optional, for debugging) -->
      <div class="absolute top-0 left-0 h-2 w-2 rounded-full bg-red-500" />

      <ZettleCard
        v-for="card in cards"
        :key="card.uuid"
        :card="card"
        :isDragging="isDragging && activeCard?.uuid === card.uuid"
        @dragStart="startDrag($event, card)" />
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="fixed top-4 right-4 rounded-lg bg-white p-4 shadow-lg">
      <div
        class="h-5 w-5 animate-spin rounded-full border-2 border-green-900 border-t-transparent"></div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="fixed top-4 right-4 rounded-lg bg-red-100 p-4 text-red-900 shadow-lg">
      {{ error }}
    </div>

    <!-- Debug Info -->
    <div class="fixed right-4 bottom-4 rounded-lg bg-white p-4 text-sm shadow-lg">
      <div>Zoom: {{ zoom }}</div>
      <div>View: {{ Math.round(viewX) }}, {{ Math.round(viewY) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import ZettleCard from './ZettleCard.vue'

// State
const cards = ref<ZettleCard[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const container = ref<HTMLElement | null>(null)

// View state
const viewX = ref(0)
const viewY = ref(0)
const zoom = ref(1)
const ZOOM_LEVELS = [0.25, 0.5, 1, 2, 4]

// Dragging state
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragStartViewX = ref(0)
const dragStartViewY = ref(0)
const activeCard = ref<ZettleCard | null>(null)
const dragStartCardX = ref(0)
const dragStartCardY = ref(0)

// Pan handling
function startPan(e: MouseEvent) {
  if (activeCard.value) return

  isDragging.value = true
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  dragStartViewX.value = viewX.value
  dragStartViewY.value = viewY.value
}

// Card drag handling
function startDrag(e: MouseEvent, card: ZettleCard) {
  isDragging.value = true
  activeCard.value = card
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  dragStartCardX.value = card.x
  dragStartCardY.value = card.y
}

function handleMouseMove(e: MouseEvent) {
  if (!isDragging.value) return

  if (activeCard.value) {
    // Card dragging - scale movement by zoom level
    const dx = (e.clientX - dragStartX.value) / zoom.value
    const dy = (e.clientY - dragStartY.value) / zoom.value
    activeCard.value.x = dragStartCardX.value + dx
    activeCard.value.y = dragStartCardY.value + dy
  } else {
    // Canvas panning
    const dx = e.clientX - dragStartX.value
    const dy = e.clientY - dragStartY.value
    viewX.value = dragStartViewX.value + dx
    viewY.value = dragStartViewY.value + dy
  }
}

async function handleMouseUp() {
  if (activeCard.value) {
    try {
      const response = await fetch(`/api/cards/${activeCard.value.uuid}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': window.CSRF_TOKEN,
        },
        body: JSON.stringify({
          x: Math.round(activeCard.value.x),
          y: Math.round(activeCard.value.y),
        }),
      })

      if (!response.ok) throw new Error('Failed to update card position')
    } catch (e) {
      error.value = 'Failed to save card position'
      console.error(e)
    }
  }

  isDragging.value = false
  activeCard.value = null

  updateURLState()
}

function updateURLState() {
  const params = new URLSearchParams(window.location.search)
  params.set('x', viewX.value.toString())
  params.set('y', viewY.value.toString())
  params.set('zoom', zoom.value.toString())
  window.history.replaceState({}, '', `${window.location.pathname}?${params}`)
}

function handleZoom(e: WheelEvent) {
  if (!container.value) return

  const oldZoom = zoom.value

  // Calculate new zoom level
  const currentZoomIndex = ZOOM_LEVELS.indexOf(oldZoom)
  const newZoomIndex =
    e.deltaY > 0
      ? Math.max(0, currentZoomIndex - 1)
      : Math.min(ZOOM_LEVELS.length - 1, currentZoomIndex + 1)
  const newZoom = ZOOM_LEVELS[newZoomIndex]

  if (newZoom === oldZoom) return

  // Get mouse position relative to viewport
  const rect = container.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  // Calculate the point to zoom around (in world space)
  const worldX = (mouseX - viewX.value) / oldZoom
  const worldY = (mouseY - viewY.value) / oldZoom

  // Update zoom
  zoom.value = newZoom

  // Update view position to zoom around mouse point
  viewX.value = mouseX - worldX * newZoom
  viewY.value = mouseY - worldY * newZoom

  updateURLState()
}

function loadStateFromURL() {
  const params = new URLSearchParams(window.location.search)
  if (!params.has('x') && !params.has('y') && container.value) {
    const rect = container.value.getBoundingClientRect()
    viewX.value = rect.width / 2
    viewY.value = rect.height / 2
  } else {
    viewX.value = Number(params.get('x')) || 0
    viewY.value = Number(params.get('y')) || 0
  }
  zoom.value = Number(params.get('zoom')) || 1
  if (!ZOOM_LEVELS.includes(zoom.value)) zoom.value = 1
}

const fetchCards = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/cards/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    cards.value = data.results || data
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
    console.error('Error fetching cards:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadStateFromURL()
  fetchCards()
})
</script>
