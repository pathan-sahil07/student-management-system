<script setup lang="ts">
import type { StudentPayload } from '~/composables/useStudentsApi'

const route = useRoute()
const router = useRouter()
const { fetchStudent, updateStudent } = useStudentsApi()
const toast = useToast()

const studentId = route.params.id as string

const loading = ref(true)
const submitting = ref(false)
const notFound = ref(false)

const formData = reactive<StudentPayload>({
  name: '',
  email: '',
  course: '',
  year: 1,
  phone: '',
})

async function loadStudent() {
  loading.value = true
  try {
    const student = await fetchStudent(studentId)
    formData.name = student.name
    formData.email = student.email
    formData.course = student.course
    formData.year = student.year
    formData.phone = student.phone
  } catch (err: any) {
    notFound.value = true
    toast.error(err.message || 'Student not found')
  } finally {
    loading.value = false
  }
}

async function handleSubmit(payload: StudentPayload) {
  submitting.value = true
  try {
    await updateStudent(studentId, payload)
    toast.success(`${payload.name} was updated successfully`)
    router.push('/students')
  } catch (err: any) {
    toast.error(err.message || 'Failed to update student')
  } finally {
    submitting.value = false
  }
}

onMounted(loadStudent)
</script>

<template>
  <div>
    <AppTopbar title="Edit Student" />
    <div class="app-content">
      <div class="page-header">
        <div>
          <h1>Edit Student</h1>
          <p>Update the student's information below.</p>
        </div>
        <NuxtLink to="/students" class="btn btn-secondary">← Back to list</NuxtLink>
      </div>

      <LoadingSpinner v-if="loading" message="Loading student details..." />

      <EmptyState
        v-else-if="notFound"
        title="Student not found"
        message="The student you're looking for doesn't exist or may have been removed."
      >
        <NuxtLink to="/students" class="btn btn-primary btn-sm" style="margin-top: 12px;">Back to Students</NuxtLink>
      </EmptyState>

      <div v-else class="card form-card">
        <StudentForm
          :model-value="formData"
          submit-label="Update Student"
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
</style>
