<script setup lang="ts">
import type { StudentPayload } from '~/composables/useStudentsApi'

const { createStudent } = useStudentsApi()
const toast = useToast()
const router = useRouter()

const submitting = ref(false)
const showSuccess = ref(false)

const emptyForm: StudentPayload = {
  name: '',
  email: '',
  course: '',
  year: 1,
  phone: '',
}

async function handleSubmit(payload: StudentPayload) {
  submitting.value = true
  try {
    await createStudent(payload)
    toast.success(`${payload.name} was added successfully`)
    showSuccess.value = true
    setTimeout(() => router.push('/students'), 900)
  } catch (err: any) {
    toast.error(err.message || 'Failed to add student')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <AppTopbar title="Add Student" />
    <div class="app-content">
      <div class="page-header">
        <div>
          <h1>Add New Student</h1>
          <p>Fill in the details below to enroll a new student.</p>
        </div>
        <NuxtLink to="/students" class="btn btn-secondary">← Back to list</NuxtLink>
      </div>

      <div class="card form-card">
        <div v-if="showSuccess" class="success-banner">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M20 6 9 17l-5-5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Student added successfully! Redirecting to the students list...
        </div>

        <StudentForm
          :model-value="emptyForm"
          submit-label="Add Student"
          :loading="submitting"
          @submit="handleSubmit"
        >
          <template #actions-prepend>
            <NuxtLink to="/students" class="btn btn-secondary">Cancel</NuxtLink>
          </template>
        </StudentForm>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-card {
  max-width: 720px;
}

.success-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-success-light);
  color: var(--color-success);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 13.5px;
  font-weight: 600;
  margin-bottom: 20px;
}
</style>
