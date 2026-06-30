<script setup lang="ts">
const props = defineProps<{ title?: string }>()
const isMobileOpen = useState('sidebarOpen', () => false)

function toggleSidebar() {
  isMobileOpen.value = !isMobileOpen.value
}
</script>

<template>
  <header class="topbar">
    <button class="menu-btn" type="button" aria-label="Toggle navigation" @click="toggleSidebar">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
    <h2 class="topbar-title">{{ title }}</h2>
    <div class="topbar-spacer"></div>
    <div class="topbar-user">
      <div class="user-avatar">AD</div>
      <div class="user-meta">
        <p class="user-name">Admin</p>
        <p class="user-role">Administrator</p>
      </div>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  height: var(--topbar-height);
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 28px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 30;
}

.menu-btn {
  display: none;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 6px;
  border-radius: var(--radius-sm);
}
.menu-btn:hover {
  background: var(--color-bg);
}

.topbar-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.topbar-spacer {
  flex: 1;
}

.topbar-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
}

.user-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.user-role {
  font-size: 11.5px;
  color: var(--color-text-muted);
}

@media (max-width: 900px) {
  .menu-btn {
    display: flex;
  }
  .topbar {
    padding: 0 16px;
  }
  .user-meta {
    display: none;
  }
}
</style>
