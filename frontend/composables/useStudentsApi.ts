/**
 * useStudentsApi
 *
 * Centralizes all HTTP calls to the FastAPI backend for student records.
 * Uses Nuxt's built-in $fetch (ofetch) under the hood, which wraps the
 * native Fetch API with sensible defaults (auto JSON, error handling).
 *
 * Keeping all API calls here (rather than scattered across pages/components)
 * makes it trivial to change the base URL, add auth headers, or swap the
 * HTTP client later without touching UI code.
 */

export interface Student {
  id: number
  name: string
  email: string
  course: string
  year: number
  phone: string
}

export interface StudentListResponse {
  total: number
  students: Student[]
}

export interface StudentPayload {
  name: string
  email: string
  course: string
  year: number
  phone: string
}

/** Normalized error shape thrown by the composable's methods. */
export interface ApiError {
  message: string
  status?: number
}

function extractErrorMessage(error: any): ApiError {
  // ofetch puts the parsed response body on error.data
  const detail = error?.data?.detail
  if (typeof detail === 'string') {
    return { message: detail, status: error?.statusCode }
  }
  if (Array.isArray(detail)) {
    // Pydantic validation errors come back as a list of { msg, loc, ... }
    const messages = detail.map((d: any) => d.msg || JSON.stringify(d)).join(', ')
    return { message: messages, status: error?.statusCode }
  }
  return {
    message: error?.message || 'Something went wrong. Please try again.',
    status: error?.statusCode,
  }
}

export function useStudentsApi() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  /** Fetch all students, optionally filtered by a search term. */
  async function fetchStudents(search?: string): Promise<StudentListResponse> {
    try {
      return await $fetch<StudentListResponse>('/students', {
        baseURL,
        method: 'GET',
        query: search ? { search } : undefined,
      })
    } catch (error) {
      throw extractErrorMessage(error)
    }
  }

  /** Fetch a single student by ID. */
  async function fetchStudent(id: number | string): Promise<Student> {
    try {
      return await $fetch<Student>(`/students/${id}`, { baseURL, method: 'GET' })
    } catch (error) {
      throw extractErrorMessage(error)
    }
  }

  /** Create a new student record. */
  async function createStudent(payload: StudentPayload): Promise<Student> {
    try {
      return await $fetch<Student>('/students', {
        baseURL,
        method: 'POST',
        body: payload,
      })
    } catch (error) {
      throw extractErrorMessage(error)
    }
  }

  /** Update an existing student record (partial update supported). */
  async function updateStudent(id: number | string, payload: Partial<StudentPayload>): Promise<Student> {
    try {
      return await $fetch<Student>(`/students/${id}`, {
        baseURL,
        method: 'PUT',
        body: payload,
      })
    } catch (error) {
      throw extractErrorMessage(error)
    }
  }

  /** Delete a student record by ID. */
  async function deleteStudent(id: number | string): Promise<{ message: string }> {
    try {
      return await $fetch<{ message: string }>(`/students/${id}`, {
        baseURL,
        method: 'DELETE',
      })
    } catch (error) {
      throw extractErrorMessage(error)
    }
  }

  return {
    fetchStudents,
    fetchStudent,
    createStudent,
    updateStudent,
    deleteStudent,
  }
}
