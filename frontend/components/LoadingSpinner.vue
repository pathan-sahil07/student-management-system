<script setup lang="ts">
withDefaults(
  defineProps<{
    message?: string
    size?: 'sm' | 'lg'
  }>(),
  { message: 'Loading...', size: 'lg' }
)
</script>

<template>
  <div class="loading-overlay">
    <div class="spinner spinner-dark" :class="{ 'spinner-lg': size === 'lg' }"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>
