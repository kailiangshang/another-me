import { useState } from 'react'
import { Send, Loader } from 'lucide-react'
import { mimicAPI } from '@/api'

export default function MimicMe() {
  const [prompt, setPrompt] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [mode, setMode] = useState<'chat' | 'post'>('chat')

  const handleSubmit = async () => {
    if (!prompt.trim()) return

    setLoading(true)
    setError('')
    setResponse('')

    try {
      if (mode === 'chat') {
        const data = await mimicAPI.chat(prompt)
        setResponse(data.response)
      } else {
        const data = await mimicAPI.generatePost(prompt)
        setResponse(data.post)
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '生成失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">模仿我说话</h1>
        <p className="text-gray-600">让 AI 用你的语气、风格和思维方式回应问题</p>
      </div>

      {/* 模式选择 */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex gap-4">
          <button
            onClick={() => setMode('chat')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              mode === 'chat'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            对话模式
          </button>
          <button
            onClick={() => setMode('post')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              mode === 'post'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            生成朋友圈
          </button>
        </div>
      </div>

      {/* 输入区域 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {mode === 'chat' ? '你的问题' : '朋友圈主题'}
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
            placeholder={
              mode === 'chat'
                ? '例如：如果我在2020年听到这句话，我会怎么回答？'
                : '例如：今天天气不错'
            }
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <button
            onClick={handleSubmit}
            disabled={!prompt.trim() || loading}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {loading ? <Loader className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            生成
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 rounded">
            {error}
          </div>
        )}
      </div>

      {/* 响应区域 */}
      {response && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            {mode === 'chat' ? 'AI 回复' : '生成的朋友圈'}
          </h3>
          <div className="p-4 bg-gray-50 rounded-lg whitespace-pre-wrap">
            {response}
          </div>
        </div>
      )}

      {/* 使用提示 */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 使用提示</h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• <strong>对话模式</strong>：让 AI 模仿你的说话风格回答问题</li>
          <li>• <strong>生成朋友圈</strong>：基于你的历史发言风格，生成社交媒体帖子</li>
          <li>• 确保已上传足够的个人数据，AI 才能更好地模仿你</li>
        </ul>
      </div>
    </div>
  )
}
