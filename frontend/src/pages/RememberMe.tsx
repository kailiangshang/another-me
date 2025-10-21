import { useState } from 'react'
import { Clock, Search, Loader } from 'lucide-react'
import { memoryAPI } from '@/api'

export default function RememberMe() {
  const [query, setQuery] = useState('')
  const [timeContext, setTimeContext] = useState('')
  const [loading, setLoading] = useState(false)
  const [memories, setMemories] = useState<any>(null)
  const [error, setError] = useState('')

  const handleRecall = async () => {
    if (!query.trim()) return

    setLoading(true)
    setError('')
    setMemories(null)

    try {
      const data = await memoryAPI.recall(query, timeContext || undefined, 5)
      setMemories(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || '回溯失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">记忆回溯对话</h1>
        <p className="text-gray-600">唤醒你遗忘的记忆，实现"时空对话"</p>
      </div>

      {/* 搜索区域 */}
      <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            你想回忆什么？
          </label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleRecall()}
            placeholder="例如：去年这个时候我在想什么？"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            时间上下文（可选）
          </label>
          <input
            type="text"
            value={timeContext}
            onChange={(e) => setTimeContext(e.target.value)}
            placeholder="例如：2020-03、去年、这个时候"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={handleRecall}
          disabled={!query.trim() || loading}
          className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              回溯中...
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              开始回忆
            </>
          )}
        </button>

        {error && (
          <div className="p-3 bg-red-50 text-red-600 rounded">
            {error}
          </div>
        )}
      </div>

      {/* 记忆结果 */}
      {memories && (
        <div className="space-y-6">
          {/* AI 总结 */}
          {memories.summary && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Clock className="w-6 h-6 text-primary-600" />
                记忆总结
              </h2>
              <p className="text-gray-700 whitespace-pre-wrap">{memories.summary}</p>
            </div>
          )}

          {/* 记忆片段 */}
          {memories.memories && memories.memories.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">📝 相关记忆片段</h2>
              <div className="space-y-4">
                {memories.memories.map((memory: any, idx: number) => (
                  <div key={idx} className="p-4 bg-gray-50 rounded-lg border-l-4 border-primary-500">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-gray-500">
                        {new Date(memory.timestamp).toLocaleString('zh-CN')}
                      </span>
                      {memory.similarity && (
                        <span className="text-xs text-primary-600">
                          相关度: {(memory.similarity * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>
                    <p className="text-gray-700">{memory.content}</p>
                    {memory.source && (
                      <p className="text-xs text-gray-500 mt-2">来源: {memory.source}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {memories.memories && memories.memories.length === 0 && (
            <div className="bg-white rounded-lg shadow-md p-6 text-center text-gray-500">
              没有找到相关记忆
            </div>
          )}
        </div>
      )}

      {/* 快捷查询示例 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="font-semibold text-gray-800 mb-3">🔍 快捷查询示例</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {[
            '去年这个时候我在想什么？',
            '上次我遇到类似问题是怎么解决的？',
            '我2020年的计划是什么？',
            '我最近提到最多的话题是什么？',
          ].map((example, idx) => (
            <button
              key={idx}
              onClick={() => setQuery(example)}
              className="p-3 text-left bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* 使用提示 */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 使用提示</h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• 支持自然语言时间表达，如"去年"、"这个时候"</li>
          <li>• 可以搜索特定时间段的记忆</li>
          <li>• AI 会自动总结相关记忆，帮你快速回忆</li>
        </ul>
      </div>
    </div>
  )
}
