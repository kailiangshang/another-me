import { useState, useEffect } from 'react'
import { Settings as SettingsIcon, CheckCircle, AlertCircle } from 'lucide-react'
import { configAPI } from '@/api'

export default function Config() {
  const [apiKey, setApiKey] = useState('')
  const [baseUrl, setBaseUrl] = useState('https://api.openai.com/v1')
  const [model, setModel] = useState('gpt-3.5-turbo')
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')
  const [apiKeySet, setApiKeySet] = useState(false)

  useEffect(() => {
    fetchConfig()
  }, [])

  const fetchConfig = async () => {
    try {
      const data = await configAPI.getApiConfig()
      setBaseUrl(data.base_url || 'https://api.openai.com/v1')
      setModel(data.model || 'gpt-3.5-turbo')
      setApiKeySet(data.api_key_set || false)
    } catch (err) {
      console.error('Failed to fetch config:', err)
    }
  }

  const handleSave = async () => {
    if (!apiKey.trim()) {
      setError('请输入 API Key')
      return
    }

    setSaving(true)
    setError('')
    setSuccess(false)

    try {
      await configAPI.updateApiKey(apiKey, baseUrl, model)
      setSuccess(true)
      setApiKeySet(true)
      setApiKey('')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err: any) {
      setError(err.message || '保存失败')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">API 配置</h1>
        <p className="text-gray-600">配置 OpenAI 兼容的 API 接口</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            API Key
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder={apiKeySet ? '已设置 API Key (留空不修改)' : '输入你的 API Key'}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          {apiKeySet && (
            <p className="mt-2 text-sm text-green-600 flex items-center gap-1">
              <CheckCircle className="w-4 h-4" />
              API Key 已配置
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Base URL
          </label>
          <input
            type="url"
            value={baseUrl}
            onChange={(e) => setBaseUrl(e.target.value)}
            placeholder="https://api.openai.com/v1"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
          <p className="mt-1 text-sm text-gray-500">
            支持 OpenAI 兼容的 API，如本地 LLM (Ollama, LM Studio 等)
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            模型名称
          </label>
          <input
            type="text"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            placeholder="gpt-3.5-turbo"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>

        {error && (
          <div className="flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        {success && (
          <div className="flex items-center gap-2 text-green-600 bg-green-50 p-3 rounded">
            <CheckCircle className="w-5 h-5" />
            配置已保存
          </div>
        )}

        <button
          onClick={handleSave}
          disabled={saving}
          className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <SettingsIcon className="w-5 h-5" />
          {saving ? '保存中...' : '保存配置'}
        </button>
      </div>

      {/* 使用提示 */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 提示</h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• 本项目支持任何 OpenAI 兼容的 API</li>
          <li>• 可以使用本地模型 (Ollama, LM Studio) 实现完全离线</li>
          <li>• 数据仅存储在本地，不会上传到云端</li>
        </ul>
      </div>
    </div>
  )
}
