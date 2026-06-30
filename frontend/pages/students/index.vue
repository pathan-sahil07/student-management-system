<script setup lang="ts">
import type { Student } from '~/composables/useStudentsApi'

const { fetchStudents, deleteStudent } = useStudentsApi()
const toast = useToast()

const loading = ref(true)
const deleting = ref(false)
const students = ref<Student[]>([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = 8

const confirmOpen = ref(false)
const studentPendingDelete = ref<Student | null>(null)

let searchDebounce: ReturnType<typeof setTimeout> | null = null

async function loadStudents() {
  loading.value = true
  try {
    const data = await fetchStudents(searchQuery.value || undefined)
    students.value = data.students
  } catch (err: any) {
    toast.error(err.message || 'Failed to load students')
  } finally {
    loading.value = false
  }
}

function onSearchInput() {
  currentPage.value = 1
  if (searchDebounce) clearTimeout(searchDebounce)
  searchDebounce = setTimeout(loadStudents, 350)
}

const totalPages = computed(() => Math.max(1, Math.ceil(students.value.length / pageSize)))

const paginatedStudents = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return students.value.slice(start, start + pageSize)
})

watch(totalPages, (val) => {
  if (currentPage.value > val) currentPage.value = val
})

function goToPage(page: number) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

function requestDelete(student: Student) {
  studentPendingDelete.value = student
  confirmOpen.value = true
}

function cancelDelete() {
  confirmOpen.value = false
  studentPendingDelete.value = null
}

async function confirmDelete() {
  if (!studentPendingDelete.value) return
  deleting.value = true
  try {
    await deleteStudent(studentPendingDelete.value.id)
    toast.success(`${studentPendingDelete.value.name} was deleted successfully`)
    confirmOpen.value = false
    studentPendingDelete.value = null
    await loadStudents()
  } catch (err: any) {
    toast.error(err.message || 'Failed to delete student')
  } finally {
    deleting.value = false
  }
}

onMounted(loadStudents)
</script>

<template>
  <div>
    <AppTopbar title="Students" />
    <div class="app-content">
      <div class="page-header">
        <div>
          <h1>Students</h1>
          <p>Manage all enrolled students in one place.</p>
        </div>
        <NuxtLink to="/students/add" class="btn btn-primary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>
          Add Student
        </NuxtLink>
      </div>

      <div class="card table-card">
        <div class="table-toolbar">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/><path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by name, email, or course..."
              @input="onSearchInput"
            />
          </div>
          <span class="result-count">{{ students.length }} student{{ students.length === 1 ? '' : 's' }} found</span>
        </div>

        <LoadingSpinner v-if="loading" message="Loading students..." />

        <EmptyState
          v-else-if="!students.length"
          title="No students found"
          :message="searchQuery ? 'Try a different search term.' : 'Get started by adding your first student.'"
        >
          <NuxtLink v-if="!searchQuery" to="/students/add" class="btn btn-primary btn-sm" style="margin-top: 12px;">
            Add Student
          </NuxtLink>
        </EmptyState>

        <template v-else>
          <div class="table-wrapper">
            <table class="students-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Course</th>
                  <th>Year</th>
                  <th>Phone</th>
                  <th class="actions-col">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in paginatedStudents" :key="student.id">
                  <td>
                    <div class="student-name-cell">
                      <div class="table-avatar">{{ student.name.charAt(0).toUpperCase() }}</div>
                      {{ student.name }}
                    </div>
                  </td>
                  <td class="text-muted">{{ student.email }}</td>
                  <td><span class="badge badge-primary">{{ student.course }}</span></td>
                  <td>Year {{ student.year }}</td>
                  <td class="text-muted">{{ student.phone }}</td>
                  <td>
                    <div class="row-actions">
                      <NuxtLink :to="`/students/edit/${student.id}`" class="btn btn-secondary btn-sm btn-icon" title="Edit student">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M12 20h9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
                      </NuxtLink>
                      <button class="btn btn-secondary btn-sm btn-icon" title="Delete student" @click="requestDelete(student)">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--color-danger)"><path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0-1 14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2L4 6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="totalPages > 1" class="pagination">
            <button class="btn btn-secondary btn-sm" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
              Previous
            </button>
            <div class="page-numbers">
              <button
                v-for="page in totalPages"
                :key="page"
                class="page-btn"
                :class="{ 'page-btn-active': page === currentPage }"
                @click="goToPage(page)"
              >
                {{ page }}
              </button>
            </div>
            <button class="btn btn-secondary btn-sm" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
              Next
            </button>
          </div>
        </template>
      </div>
    </div>

    <ConfirmDialog
      :open="confirmOpen"
      title="Delete this student?"
      :message="studentPendingDelete ? `This will permanently remove ${studentPendingDelete.name} from the system. This action cannot be undone.` : ''"
      confirm-label="Delete"
      :loading="deleting"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<style scoped>
.table-card {
  padding: 0;
  overflow: hidden;
}

.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 18px 22px;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 9px 14px;
  flex: 1;
  max-width: 360px;
  color: var(--color-text-muted);
}

.search-box input {
  border: none;
  outline: none;
  font-size: 13.5px;
  flex: 1;
  color: var(--color-text-primary);
}

.result-count {
  font-size: 13px;
  color: var(--color-text-muted);
  white-space: nowrap;
}

.table-wrapper {
  overflow-x: auto;
}

.students-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

.students-table th {
  text-align: left;
  padding: 12px 22px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}

.students-table td {
  padding: 14px 22px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-primary);
  white-space: nowrap;
}

.students-table tbody tr:last-child td {
  border-bottom: none;
}

.students-table tbody tr:hover {
  background: var(--color-bg);
}

.text-muted {
  color: var(--color-text-secondary);
}

.student-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.table-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12.5px;
  flex-shrink: 0;
}

.actions-col {
  text-align: right;
}

.row-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 22px;
  flex-wrap: wrap;
}

.page-numbers {
  display: flex;
  gap: 6px;
}

.page-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.page-btn:hover {
  background: var(--color-bg);
}

.page-btn-active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}
</style>
