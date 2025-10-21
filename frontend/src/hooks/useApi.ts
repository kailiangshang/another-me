/**
 * API 调用 Hook
 * 统一处理加载状态、错误处理、缓存等
 */

import { useState, useCallback } from 'react'
import { useAppStore } from '@/store/useAppStore'

interface UseApiOptions {
  onSuccess?: (data: any) => void
  onError?: (error: Error) => void
  showGlobalError?: boolean
}

export function useApi<T = any>(
  apiFunction: (...args: any[]) => Promise<T>,
  options: UseApiOptions = {}
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  
  const { setError: setGlobalError, clearError } = useAppStore()
  const { onSuccess, onError, showGlobalError = true } = options
  
  const execute = useCallback(
    async (...args: any[]) => {
      setLoading(true)
      setError(null)
      if (showGlobalError) {
        clearError()
      }
      
      try {
        const result = await apiFunction(...args)
        setData(result)
        onSuccess?.(result)
        return result
      } catch (err) {
        const error = err as Error
        setError(error)
        
        if (showGlobalError) {
          setGlobalError(error.message)
        }
        
        onError?.(error)
        throw error
      } finally {
        setLoading(false)
      }
    },
    [apiFunction, onSuccess, onError, showGlobalError, setGlobalError, clearError]
  )
  
  return {
    data,
    loading,
    error,
    execute,
  }
}
