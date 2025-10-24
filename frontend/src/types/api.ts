// API 类型定义

// ============ 通用类型 ============
export interface BaseResponse {
  success: boolean;
  message: string;
  data?: any;
}

// ============ 配置相关 ============
export interface APIConfig {
  api_key: string;
  base_url: string;
  model: string;
}

export interface ConfigTestResult {
  success: boolean;
  message: string;
  model_available?: boolean;
}

// ============ RAG 相关 ============
export interface DocumentInfo {
  id: string;
  filename: string;
  size: number;
  upload_time: string;
  chunk_count?: number;
}

export interface UploadResponse {
  success: boolean;
  document_id: string;
  filename: string;
  message: string;
}

export interface SearchResult {
  content: string;
  score: number;
  metadata: Record<string, any>;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total: number;
}

export interface RAGStats {
  document_count: number;
  total_chunks: number;
  total_size: number;
}

// ============ MEM 相关 ============
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  message: string;
  timestamp: string;
}

export interface Memory {
  id: string;
  content: string;
  timestamp: string;
  metadata: Record<string, any>;
}

export interface MemoryListResponse {
  memories: Memory[];
  total: number;
}

// ============ 健康检查 ============
export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}
