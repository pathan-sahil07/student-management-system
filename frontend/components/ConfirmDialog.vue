<script setup lang="ts">
withDefaults(
  defineProps<{
    open: boolean
    title?: string
    message?: string
    confirmLabel?: string
    cancelLabel?: string
    loading?: boolean
    danger?: boolean
  }>(),
  {
    title: 'Are you sure?',
    message: 'This action cannot be undone.',
    confirmLabel: 'Confirm',
    cancelLabel: 'Cancel',
    loading: false,
    danger: true,
  }
)

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <transition name="dialog-fade">
    <div v-if="open" class="dialog-backdrop" @click.self="emit('cancel')">
      <div class="dialog-box" role="alertdialog" aria-modal="true">
        <div class="dialog-icon" :class="{ 'dialog-icon-danger': danger }">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
        </div>
        <h3 class="dialog-title">{{ title }}</h3>
        <p class="dialog-message">{{ message }}</p>
        <div class="dialog-actions">
          <button type="button" class="btn btn-secondary" :disabled="loading" @click="emit('cancel')">
            {{ cancelLabel }}
          </button>
          <button
            type="button"
            class="btn"
            :class="danger ? 'btn-danger' : 'btn-primary'"
            :disabled="loading"
            @click="emit('confirm')"
          >
            <span v-if="loading" class="spinner"></span>
            {{ confirmLabel }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.dialog-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 20, 35, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
  padding: 16px;
}

.dialog-box {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 28px;
  max-width: 380px;
  width: 100%;
  text-align: center;
}

.dialog-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.dialog-icon-danger {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.dialog-title {
  font-size: 17px;
  margin-bottom: 8px;
}

.dialog-message {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: 22px;
}

.dialog-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.dialog-actions .btn {
  flex: 1;
}

.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.2s ease;
}
.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}
</style>
