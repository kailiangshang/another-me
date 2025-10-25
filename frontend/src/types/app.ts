// 应用类型定义

export type TabKey = 'home' | 'chat' | 'knowledge' | 'memory' | 'config';

export interface AppState {
  currentTab: TabKey;
  setCurrentTab: (tab: TabKey) => void;
}
