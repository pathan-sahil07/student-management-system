<script setup lang="ts">
import type { Student } from '~/composables/useStudentsApi'

const { fetchStudents } = useStudentsApi()
const toast = useToast()

const loading = ref(true)
const students = ref<Student[]>([])
const total = ref(0)

const courseCount = computed(() => new Set(students.value.map((s) => s.course)).size)
const recentStudents = computed(() => students.value.slice(0, 5))

async function loadDashboard() {
  loading.value = true
  try {
    const data = await fetchStudents()
    students.value = data.students
    total.value = data.total
  } catch (err: any) {
    toast.error(err.message || 'Failed to load dashboard data')
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<template>
  <div>
    <AppTopbar title="Dashboard" />
    <div class="app-content">
      <div class="page-header">
        <div>
          <h1>Welcome back 👋</h1>
          <p>Here's a quick overview of your student records.</p>
        </div>
        <NuxtLink to="/students/add" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
          Add Student
        </NuxtLink>
      </div>

      <LoadingSpinner v-if="loading" message="Loading dashboard..." />

      <template v-else>
        <div class="stats-grid">
          <StatCard label="Total Students" :value="total" icon="users" accent="primary" />
          <StatCard label="Courses Offered" :value="courseCount" icon="book" accent="success" />
          <StatCard label="Average Year" :value="students.length ? (students.reduce((a, s) => a + s.year, 0) / students.length).toFixed(1) : '0'" icon="trend" accent="warning" />
        </div>

        <div class="card recent-card">
          <div class="recent-header">
            <h3>Recently Added Students</h3>
            <NuxtLink to="/students" class="view-all-link">View all →</NuxtLink>
          </div>

          <EmptyState
            v-if="!recentStudents.length"
            title="No students yet"
            message="Add your first student to see them appear here."
          />

          <div v-else class="recent-list">
            <div v-for="student in recentStudents" :key="student.id" class="recent-item">
              <div class="recent-avatar">{{ student.name.charAt(0).toUpperCase() }}</div>
              <div class="recent-info">
                <p class="recent-name">{{ student.name }}</p>
                <p class="recent-email">{{ student.email }}</p>
              </div>
              <span class="badge badge-primary">{{ student.course }}</span>
              <span class="badge badge-success">Year {{ student.year }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
  margin-bottom: 24px;
}

.recent-card {
  padding: 0;
  overflow: hidden;
}

.recent-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.recent-header h3 {
  font-size: 16px;
}

.view-all-link {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--color-primary);
}

.recent-list {
  display: flex;
  flex-direction: column;
}

.recent-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
}

.recent-item:last-child {
  border-bottom: none;
}

.recent-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.recent-info {
  flex: 1;
  min-width: 0;
}

.recent-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.recent-email {
  font-size: 12.5px;
  color: var(--color-text-muted);
  margin-top: 1px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 640px) {
  .recent-item {
    flex-wrap: wrap;
  }
}
</style>
