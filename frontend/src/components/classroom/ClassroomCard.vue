<template>
  <div :class="['classroom-card', !classroom.is_available && 'opacity-60']">
    <div class="h-48 bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
      <svg class="w-16 h-16 text-primary/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    </div>

    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <div>
          <h3 class="text-lg font-semibold text-gray-900">{{ classroom.name }}</h3>
          <p class="text-sm text-gray-500 mt-1">
            {{ classroom.building }}栋 {{ classroom.floor }}层 {{ classroom.room_number }}室
          </p>
        </div>
        <span v-if="!classroom.is_available" class="badge badge-warning">维护中</span>
        <span v-else class="badge badge-success">可用</span>
      </div>

      <div class="flex flex-wrap gap-2 mb-4">
        <span v-if="classroom.has_projector" class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600">📽️ 投影仪</span>
        <span v-if="classroom.has_computer" class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600">💻 电脑</span>
        <span v-if="classroom.has_microphone" class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600">🎤 麦克风</span>
        <span v-if="classroom.has_whiteboard" class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600">📝 白板</span>
        <span v-if="classroom.has_air_conditioning" class="inline-flex items-center px-2 py-1 bg-secondary-100 rounded text-xs text-gray-600">❄️ 空调</span>
      </div>

      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2 text-sm text-gray-600">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20H2a2 2 0 01-2-2v-2a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2zm2.5-8.25h.008v.008h-.008V9.75h.008zM12 14.5a.5.5 0 01-.5.5h-5a.5.5 0 010-1h5a.5.5 0 01.5.5zm5 0a.5.5 0 01-.5.5h-5a.5.5 0 010-1h5a.5.5 0 01.5.5z" />
          </svg>
          <span>{{ classroom.capacity }}人</span>
        </div>
        <div class="text-xs text-gray-500">{{ classroom.classroom_type_display }}</div>
      </div>

      <div class="flex space-x-3">
        <button type="button" class="flex-1 btn-secondary text-sm py-2" @click="$emit('detail', classroom)">详情</button>
        <button
          type="button"
          :disabled="!classroom.is_available"
          class="flex-1 btn-primary text-sm py-2"
          :class="{ 'opacity-50 cursor-not-allowed': !classroom.is_available }"
          @click="$emit('reserve', classroom)"
        >
          {{ classroom.is_available ? '预约' : '不可用' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  classroom: {
    type: Object,
    required: true
  }
})

defineEmits(['detail', 'reserve'])
</script>
