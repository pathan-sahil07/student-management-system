<script setup lang="ts">
import type { StudentPayload } from '~/composables/useStudentsApi'

const props = withDefaults(
  defineProps<{
    modelValue: StudentPayload
    submitLabel?: string
    loading?: boolean
  }>(),
  { submitLabel: 'Save', loading: false }
)

const emit = defineEmits<{
  submit: [payload: StudentPayload]
  'update:modelValue': [payload: StudentPayload]
}>()

// Local working copy so we don't mutate the parent's object directly.
const form = reactive<StudentPayload>({ ...props.modelValue })

// Keep local form in sync if the parent updates modelValue (e.g. after fetching
// the student to edit, which resolves asynchronously).
watch(
  () => props.modelValue,
  (val) => {
    Object.assign(form, val)
  },
  { deep: true }
)

const courseOptions = [
  'Computer Science',
  'Information Technology',
  'Electronics Engineering',
  'Mechanical Engineering',
  'Civil Engineering',
  'Electrical Engineering',
  'Business Administration',
  'Biotechnology',
]

interface FormErrors {
  name?: string
  email?: string
  course?: string
  year?: string
  phone?: string
}

const errors = reactive<FormErrors>({})
const touched = reactive<Record<string, boolean>>({})

function validateField(field: keyof StudentPayload): void {
  switch (field) {
    case 'name': {
      const value = form.name?.trim() ?? ''
      if (!value) errors.name = 'Name is required'
      else if (value.length < 2) errors.name = 'Name must be at least 2 characters'
      else if (value.length > 100) errors.name = 'Name must be under 100 characters'
      else delete errors.name
      break
    }
    case 'email': {
      const value = form.email?.trim() ?? ''
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value) errors.email = 'Email is required'
      else if (!emailRegex.test(value)) errors.email = 'Enter a valid email address'
      else delete errors.email
      break
    }
    case 'course': {
      if (!form.course || !form.course.trim()) errors.course = 'Course is required'
      else delete errors.course
      break
    }
    case 'year': {
      const value = Number(form.year)
      if (!form.year && form.year !== 0) errors.year = 'Year is required'
      else if (Number.isNaN(value) || value < 1 || value > 6) errors.year = 'Year must be between 1 and 6'
      else delete errors.year
      break
    }
    case 'phone': {
      const value = form.phone?.trim() ?? ''
      const cleaned = value.replace(/[\s\-+]/g, '')
      if (!value) errors.phone = 'Phone number is required'
      else if (!/^\d{7,15}$/.test(cleaned)) errors.phone = 'Enter a valid phone number (7-15 digits)'
      else delete errors.phone
      break
    }
  }
}

function validateAll(): boolean {
  ;(['name', 'email', 'course', 'year', 'phone'] as (keyof StudentPayload)[]).forEach((field) => {
    touched[field] = true
    validateField(field)
  })
  return Object.keys(errors).length === 0
}

function handleBlur(field: keyof StudentPayload) {
  touched[field] = true
  validateField(field)
}

function handleSubmit() {
  if (!validateAll()) return
  emit('submit', { ...form, year: Number(form.year) })
}

defineExpose({ validateAll })
</script>

<template>
  <form class="student-form" novalidate @submit.prevent="handleSubmit">
    <div class="form-row">
      <div class="form-group">
        <label class="form-label" for="name">Full Name <span class="required">*</span></label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          class="form-input"
          :class="{ 'has-error': touched.name && errors.name }"
          placeholder="e.g. Aarav Sharma"
          @blur="handleBlur('name')"
          @input="touched.name && validateField('name')"
        />
        <span v-if="touched.name && errors.name" class="form-error">{{ errors.name }}</span>
      </div>

      <div class="form-group">
        <label class="form-label" for="email">Email Address <span class="required">*</span></label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          class="form-input"
          :class="{ 'has-error': touched.email && errors.email }"
          placeholder="e.g. aarav.sharma@example.com"
          @blur="handleBlur('email')"
          @input="touched.email && validateField('email')"
        />
        <span v-if="touched.email && errors.email" class="form-error">{{ errors.email }}</span>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label class="form-label" for="course">Course <span class="required">*</span></label>
        <select
          id="course"
          v-model="form.course"
          class="form-select"
          :class="{ 'has-error': touched.course && errors.course }"
          @blur="handleBlur('course')"
          @change="touched.course && validateField('course')"
        >
          <option value="" disabled>Select a course</option>
          <option v-for="course in courseOptions" :key="course" :value="course">{{ course }}</option>
        </select>
        <span v-if="touched.course && errors.course" class="form-error">{{ errors.course }}</span>
      </div>

      <div class="form-group">
        <label class="form-label" for="year">Year of Study <span class="required">*</span></label>
        <select
          id="year"
          v-model.number="form.year"
          class="form-select"
          :class="{ 'has-error': touched.year && errors.year }"
          @blur="handleBlur('year')"
          @change="touched.year && validateField('year')"
        >
          <option value="" disabled>Select year</option>
          <option v-for="y in 6" :key="y" :value="y">Year {{ y }}</option>
        </select>
        <span v-if="touched.year && errors.year" class="form-error">{{ errors.year }}</span>
      </div>
    </div>

    <div class="form-group">
      <label class="form-label" for="phone">Phone Number <span class="required">*</span></label>
      <input
        id="phone"
        v-model="form.phone"
        type="tel"
        class="form-input"
        :class="{ 'has-error': touched.phone && errors.phone }"
        placeholder="e.g. 9876543210"
        @blur="handleBlur('phone')"
        @input="touched.phone && validateField('phone')"
      />
      <span v-if="touched.phone && errors.phone" class="form-error">{{ errors.phone }}</span>
      <span v-else class="form-hint">Digits only, 7-15 characters, may include + at the start</span>
    </div>

    <div class="form-actions">
      <slot name="actions-prepend" />
      <button type="submit" class="btn btn-primary" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        {{ submitLabel }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.student-form {
  max-width: 640px;
}

.required {
  color: var(--color-danger);
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  justify-content: flex-end;
}
</style>
