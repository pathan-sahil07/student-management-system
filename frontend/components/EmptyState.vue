<script setup lang="ts">
withDefaults(
  defineProps<{
    title?: string
    message?: string
  }>(),
  { title: 'No records found', message: 'There is nothing to show here yet.' }
)
</script>

<template>
  <div class="empty-state">
    <div class="empty-icon">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none"><path d="M9 12h6M9 16h6M9 8h6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h9l5 5v11a2 2 0 0 1-2 2Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
    </div>
    <h3>{{ title }}</h3>
    <p>{{ message }}</p>
    <slot />
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
}

.empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 16px;
  color: var(--color-text-primary);
  margin-bottom: 6px;
}

.empty-state p {
  font-size: 13.5px;
  max-width: 320px;
}
</style>
