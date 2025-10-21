/**
 * 全局状态管理
 * 使用 Zustand 进行轻量级状态管理
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  // API 配置
  apiConfig: {
    apiKey: string
    baseUrl: string
    model: string
    isConfigured: boolean
  }
  
  // 数据统计
  stats: {
    totalDocuments: number
    lastUpdated: string | null
  }
  
  // UI 状态
  isLoading: boolean
  error: string | null
  
  // Actions
  setApiConfig: (config: Partial<AppState['apiConfig']>) => void
  setStats: (stats: Partial<AppState['stats']>) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  clearError: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // 初始状态
      apiConfig: {
        apiKey: '',
        baseUrl: 'https://api.openai.com/v1',
        model: 'gpt-3.5-turbo',
        isConfigured: false,
      },
      
      stats: {
        totalDocuments: 0,
        lastUpdated: null,
      },
      
      isLoading: false,
      error: null,
      
      // Actions
      setApiConfig: (config) =>
        set((state) => ({
          apiConfig: { ...state.apiConfig, ...config },
        })),
      
      setStats: (stats) =>
        set((state) => ({
          stats: { ...state.stats, ...stats },
        })),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setError: (error) => set({ error }),
      
      clearError: () => set({ error: null }),
    }),
    {
      name: 'another-me-storage',
      partialize: (state) => ({
        apiConfig: state.apiConfig,
        stats: state.stats,
      }),
    }
  )
)
