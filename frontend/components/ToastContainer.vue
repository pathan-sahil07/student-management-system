<script setup lang="ts">
const { toasts, remove } = useToast()
</script>

<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="`toast-${toast.type}`">
        <span class="toast-icon">
          <svg v-if="toast.type === 'success'" width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <svg v-else-if="toast.type === 'error'" width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M12 8v5M12 16h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </span>
        <p class="toast-message">{{ toast.message }}</p>
        <button class="toast-close" type="button" aria-label="Dismiss notification" @click="remove(toast.id)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 360px;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px 14px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.toast-success {
  border-left: 4px solid var(--color-success);
}
.toast-success .toast-icon {
  color: var(--color-success);
}

.toast-error {
  border-left: 4px solid var(--color-danger);
}
.toast-error .toast-icon {
  color: var(--color-danger);
}

.toast-info {
  border-left: 4px solid var(--color-primary);
}
.toast-info .toast-icon {
  color: var(--color-primary);
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 1px;
}

.toast-message {
  flex: 1;
  font-size: 13.5px;
  color: var(--color-text-primary);
  line-height: 1.4;
}

.toast-close {
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 2px;
  flex-shrink: 0;
}
.toast-close:hover {
  color: var(--color-text-primary);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

@media (max-width: 480px) {
  .toast-container {
    left: 16px;
    right: 16px;
    max-width: none;
  }
}
</style>
