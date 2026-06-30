/**
 * useToast
 *
 * Lightweight global toast/notification system. State is shared across
 * the whole app via Nuxt's `useState`, and rendered by <ToastContainer />
 * (mounted once in app.vue).
 */

export interface Toast {
  id: number
  type: 'success' | 'error' | 'info'
  message: string
}

let idCounter = 0

export function useToast() {
  const toasts = useState<Toast[]>('toasts', () => [])

  function push(type: Toast['type'], message: string, duration = 4000) {
    const id = ++idCounter
    toasts.value.push({ id, type, message })
    setTimeout(() => remove(id), duration)
  }

  function remove(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    success: (message: string) => push('success', message),
    error: (message: string) => push('error', message),
    info: (message: string) => push('info', message),
    remove,
  }
}
