import axios, { AxiosInstance } from 'axios';
import type {
  APIConfig,
  ConfigTestResult,
  BaseResponse,
  UploadResponse,
  SearchResponse,
  RAGStats,
  DocumentInfo,
  ChatResponse,
  MemoryListResponse,
  HealthResponse,
} from '@/types';

class APIClient {
  private axios: AxiosInstance;
  private requestCache: Map<string, { data: any; timestamp: number }> = new Map();
  private readonly CACHE_TTL = 5 * 60 * 1000; // 5分钟缓存

  constructor() {
    this.axios = axios.create({
      baseURL: '/api/v1',
      timeout: 60000, // 增加超时时间
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // 添加响应拦截器
    this.axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // 服务器返回错误
          const detail = error.response.data?.detail || '请求失败';
          console.error('API Error:', detail);
        } else if (error.request) {
          // 请求已发出但没有响应
          console.error('Network Error:', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * 缓存GET请求结果
   */
  private getCached<T>(key: string): T | null {
    const cached = this.requestCache.get(key);
    if (cached && Date.now() - cached.timestamp < this.CACHE_TTL) {
      return cached.data as T;
    }
    return null;
  }

  private setCache(key: string, data: any): void {
    this.requestCache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  // ============ 健康检查 ============
  async healthCheck(): Promise<HealthResponse> {
    const cacheKey = 'health';
    const cached = this.getCached<HealthResponse>(cacheKey);
    if (cached) return cached;

    const response = await this.axios.get<HealthResponse>('/health');
    this.setCache(cacheKey, response.data);
    return response.data;
  }

  // ============ 配置管理 ============
  async saveConfig(config: APIConfig): Promise<BaseResponse> {
    const response = await this.axios.post<BaseResponse>('/config/save', config);
    return response.data;
  }

  async loadConfig(): Promise<APIConfig> {
    const response = await this.axios.get<APIConfig>('/config/load');
    return response.data;
  }

  async testConfig(config: APIConfig): Promise<ConfigTestResult> {
    const response = await this.axios.post<ConfigTestResult>('/config/test', config);
    return response.data;
  }

  // ============ RAG 知识库 ============
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.axios.post<UploadResponse>('/rag/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async searchKnowledge(query: string, top_k: number = 5): Promise<SearchResponse> {
    const response = await this.axios.post<SearchResponse>('/rag/search', {
      query,
      top_k,
    });
    return response.data;
  }

  async getDocuments(): Promise<DocumentInfo[]> {
    const response = await this.axios.get<DocumentInfo[]>('/rag/documents');
    return response.data;
  }

  async deleteDocument(docId: string): Promise<BaseResponse> {
    const response = await this.axios.delete<BaseResponse>(`/rag/documents/${docId}`);
    return response.data;
  }

  async getRAGStats(): Promise<RAGStats> {
    const response = await this.axios.get<RAGStats>('/rag/stats');
    return response.data;
  }

  // ============ MEM 对话 ============
  async chatSync(message: string): Promise<ChatResponse> {
    const response = await this.axios.post<ChatResponse>('/mem/chat-sync', {
      message,
    });
    return response.data;
  }

  /**
   * 流式对话 - 使用 EventSource 实现 SSE
   * @param message - 用户消息
   * @param onMessage - 消息回调
   * @param onError - 错误回调
   * @param onComplete - 完成回调
   */
  async chatStream(
    message: string,
    onMessage: (chunk: string) => void,
    onError?: (error: Error) => void,
    onComplete?: () => void
  ): Promise<void> {
    try {
      // 使用 POST 请求发送消息，但使用 fetch 获取流式响应
      const response = await fetch('/api/v1/mem/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          onComplete?.();
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') {
              onComplete?.();
              return;
            }
            if (data.startsWith('[ERROR]')) {
              onError?.(new Error(data.slice(8)));
              return;
            }
            onMessage(data);
          }
        }
      }
    } catch (error) {
      onError?.(error as Error);
    }
  }

  async learnFromConversation(message: string, context?: string): Promise<BaseResponse> {
    const response = await this.axios.post<BaseResponse>('/mem/learn', {
      message,
      context,
    });
    return response.data;
  }

  async getMemories(limit: number = 100): Promise<MemoryListResponse> {
    const response = await this.axios.get<MemoryListResponse>('/mem/memories', {
      params: { limit },
    });
    return response.data;
  }

  async deleteMemory(memoryId: string): Promise<BaseResponse> {
    const response = await this.axios.delete<BaseResponse>(`/mem/memories/${memoryId}`);
    return response.data;
  }
}

export const apiClient = new APIClient();
export default apiClient;
