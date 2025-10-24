import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { APIConfig } from '@/types';

interface ConfigState {
  config: APIConfig | null;
  isConfigured: boolean;
  setConfig: (config: APIConfig) => void;
  clearConfig: () => void;
}

export const useConfigStore = create<ConfigState>()(
  persist(
    (set) => ({
      config: null,
      isConfigured: false,
      setConfig: (config) => set({ config, isConfigured: true }),
      clearConfig: () => set({ config: null, isConfigured: false }),
    }),
    {
      name: 'another-me-config',
    }
  )
);
