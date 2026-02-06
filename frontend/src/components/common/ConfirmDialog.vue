<template>
  <div v-if="modelValue" class="confirm-overlay" @click.self="emit('update:modelValue', false)">
    <div class="confirm-card">
      <div class="confirm-icon-wrap">
        <div class="confirm-icon">!</div>
      </div>

      <h3 class="confirm-title">{{ title }}</h3>
      <p v-if="subtitle" class="confirm-subtitle">{{ subtitle }}</p>
      <p class="confirm-content">{{ content }}</p>

      <div class="confirm-actions">
        <button type="button" class="btn-secondary confirm-btn" @click="onCancel">
          {{ cancelText }}
        </button>
        <button type="button" class="btn-danger confirm-btn" @click="onConfirm">
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: '确认'
  },
  cancelText: {
    type: String,
    default: '取消'
  }
})

const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const onCancel = () => {
  emit('cancel')
  emit('update:modelValue', false)
}

const onConfirm = () => {
  emit('confirm')
}
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}

.confirm-card {
  width: 100%;
  max-width: 560px;
  background: #ffffff;
  border-radius: 24px;
  padding: 36px 32px 28px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.2);
  text-align: center;
}

.confirm-icon-wrap {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.confirm-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.confirm-title {
  margin: 0;
  font-size: 2rem;
  line-height: 1.2;
  font-weight: 700;
  color: #0f172a;
}

.confirm-subtitle {
  margin-top: 10px;
  font-size: 1rem;
  color: #334155;
  font-weight: 600;
}

.confirm-content {
  margin-top: 10px;
  font-size: 1rem;
  line-height: 1.6;
  color: #64748b;
}

.confirm-actions {
  margin-top: 26px;
  display: flex;
  gap: 12px;
}

.confirm-btn {
  flex: 1;
  min-height: 46px;
}

@media (max-width: 640px) {
  .confirm-card {
    border-radius: 18px;
    padding: 28px 20px 20px;
  }

  .confirm-title {
    font-size: 1.6rem;
  }

  .confirm-actions {
    flex-direction: column;
  }
}
</style>
