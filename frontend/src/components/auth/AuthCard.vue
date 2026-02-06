<template>
  <div class="auth-container" :class="containerClass">
    <div class="auth-card" :class="cardClass">
      <div class="logo-section">
        <div class="logo-icon" :class="iconClass">
          <slot name="icon" />
        </div>
        <h1>{{ title }}</h1>
        <p class="subtitle">{{ subtitle }}</p>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  containerClass: {
    type: String,
    default: ''
  },
  cardClass: {
    type: String,
    default: ''
  },
  iconClass: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.auth-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 137, 123, 0.03) 0%, transparent 50%);
  animation: pulse 15s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(-5%, -5%) scale(1.05);
  }
}

.auth-card {
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  padding: 48px;
  width: 100%;
  position: relative;
  z-index: 1;
}

.logo-section {
  margin-bottom: 40px;
  text-align: center;
}

.logo-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #00897b 0%, #00796b 100%);
  border-radius: 16px;
  color: white;
  font-size: 32px;
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.2);
}

h1 {
  color: #1f2937;
  margin: 0 0 8px;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.subtitle {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
  font-weight: 500;
}

@media (max-width: 640px) {
  .auth-card {
    padding: 32px 24px;
    border-radius: 1.25rem;
  }

  h1 {
    font-size: 1.5rem;
  }

  .logo-icon {
    width: 56px;
    height: 56px;
    font-size: 28px;
  }
}
</style>
