<script setup lang="ts">
/**
 * AppSidebar
 * Fixed-position navigation sidebar for desktop, collapsible drawer on mobile.
 */
const route = useRoute()
const isMobileOpen = useState('sidebarOpen', () => false)

const navItems = [
  { label: 'Dashboard', to: '/', icon: 'grid' },
  { label: 'Students', to: '/students', icon: 'users' },
  { label: 'Add Student', to: '/students/add', icon: 'plus' },
]

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function closeMobile() {
  isMobileOpen.value = false
}
</script>

<template>
  <transition name="fade">
    <div v-if="isMobileOpen" class="sidebar-backdrop" @click="closeMobile"></div>
  </transition>

  <aside class="sidebar" :class="{ 'sidebar-open': isMobileOpen }">
    <div class="sidebar-brand">
      <div class="brand-mark">SM</div>
      <div>
        <p class="brand-title">Student MS</p>
        <p class="brand-subtitle">Management System</p>
      </div>
    </div>

    <nav class="sidebar-nav">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="nav-item"
        :class="{ 'nav-item-active': isActive(item.to) }"
        @click="closeMobile"
      >
        <span class="nav-icon">
          <svg v-if="item.icon === 'grid'" width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="8" height="8" rx="2" stroke="currentColor" stroke-width="2"/><rect x="13" y="3" width="8" height="8" rx="2" stroke="currentColor" stroke-width="2"/><rect x="3" y="13" width="8" height="8" rx="2" stroke="currentColor" stroke-width="2"/><rect x="13" y="13" width="8" height="8" rx="2" stroke="currentColor" stroke-width="2"/></svg>
          <svg v-else-if="item.icon === 'users'" width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        </span>
        {{ item.label }}
      </NuxtLink>
    </nav>

    <div class="sidebar-footer">
      <p>Student Management System</p>
      <p class="sidebar-version">v1.0.0</p>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: 40;
  transition: transform 0.25s ease;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 22px 22px 18px;
}

.brand-mark {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--color-primary), #7c8cff);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 13px;
  flex-shrink: 0;
}

.brand-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.brand-subtitle {
  font-size: 11.5px;
  color: var(--color-text-muted);
  margin-top: 1px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 14px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 14px;
  font-weight: 500;
  transition: background 0.15s ease, color 0.15s ease;
}

.nav-item:hover {
  background: var(--color-bg);
  color: var(--color-text-primary);
}

.nav-item-active {
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-weight: 600;
}

.nav-icon {
  display: flex;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 18px 22px;
  border-top: 1px solid var(--color-border);
  font-size: 12px;
  color: var(--color-text-muted);
}

.sidebar-version {
  margin-top: 2px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.sidebar-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 20, 35, 0.4);
  z-index: 39;
  display: none;
}

@media (max-width: 900px) {
  .sidebar {
    transform: translateX(-100%);
  }
  .sidebar-open {
    transform: translateX(0);
  }
  .sidebar-backdrop {
    display: block;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
