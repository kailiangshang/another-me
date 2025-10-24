import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ChatMessage } from '@/types';

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;
  setLoading: (loading: boolean) => void;
  updateLastMessage: (content: string) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      messages: [],
      isLoading: false,
      addMessage: (message) =>
        set((state) => ({ messages: [...state.messages, message] })),
      clearMessages: () => set({ messages: [] }),
      setLoading: (loading) => set({ isLoading: loading }),
      updateLastMessage: (content) =>
        set((state) => {
          const messages = [...state.messages];
          if (messages.length > 0) {
            messages[messages.length - 1] = {
              ...messages[messages.length - 1],
              content
            };
          }
          return { messages };
        }),
    }),
    {
      name: 'chat-storage', // 本地存储键名
      partialize: (state) => ({ messages: state.messages }), // 只持久化 messages
    }
  )
);
