import { useState, useEffect } from 'react'
import { Brain, Loader } from 'lucide-react'
import { analysisAPI } from '@/api'

export default function KnowMyself() {
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState<any>(null)
  const [error, setError] = useState('')
  const [analysisType, setAnalysisType] = useState('comprehensive')

  const generateReport = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await analysisAPI.generateReport(undefined, undefined, analysisType)
      setReport(data.report)
    } catch (err: any) {
      setError(err.response?.data?.detail || '分析失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">自我认知分析</h1>
        <p className="text-gray-600">帮你更客观地认识自己，发现盲点</p>
      </div>

      {/* 分析类型选择 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          选择分析类型
        </label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { value: 'comprehensive', label: '综合分析' },
            { value: 'emotion', label: '情绪分析' },
            { value: 'keywords', label: '关键词' },
            { value: 'relationships', label: '人际关系' },
          ].map((type) => (
            <button
              key={type.value}
              onClick={() => setAnalysisType(type.value)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                analysisType === type.value
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              {type.label}
            </button>
          ))}
        </div>

        <button
          onClick={generateReport}
          disabled={loading}
          className="mt-4 w-full flex items-center justify-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              分析中...
            </>
          ) : (
            <>
              <Brain className="w-5 h-5" />
              生成分析报告
            </>
          )}
        </button>

        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 rounded">
            {error}
          </div>
        )}
      </div>

      {/* 分析报告 */}
      {report && (
        <div className="space-y-6">
          {/* 综合总结 */}
          {report.summary && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">📝 综合总结</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{report.summary}</p>
            </div>
          )}

          {/* 情绪分析 */}
          {report.emotions && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">😊 情绪分析</h2>
              <div className="space-y-3">
                <div>
                  <span className="text-gray-600">整体情绪：</span>
                  <span className="font-semibold ml-2">
                    {report.emotions.overall === 'positive' && '😊 积极'}
                    {report.emotions.overall === 'negative' && '😔 消极'}
                    {report.emotions.overall === 'neutral' && '😐 中性'}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-green-50 p-3 rounded">
                    <p className="text-sm text-gray-600">积极</p>
                    <p className="text-2xl font-bold text-green-600">
                      {report.emotions.distribution.positive || 0}
                    </p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-600">中性</p>
                    <p className="text-2xl font-bold text-gray-600">
                      {report.emotions.distribution.neutral || 0}
                    </p>
                  </div>
                  <div className="bg-red-50 p-3 rounded">
                    <p className="text-sm text-gray-600">消极</p>
                    <p className="text-2xl font-bold text-red-600">
                      {report.emotions.distribution.negative || 0}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* 关键词 */}
          {report.keywords && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">🔑 高频关键词</h2>
              <div className="flex flex-wrap gap-2">
                {report.keywords.keywords?.slice(0, 20).map((kw: any, idx: number) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                    style={{ fontSize: `${12 + kw.weight * 6}px` }}
                  >
                    {kw.word}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* 人际关系 */}
          {report.relationships && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">👥 人际关系</h2>
              <div className="space-y-2">
                {report.relationships.people?.map((person: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <span className="font-medium">{person.name}</span>
                    <span className="text-sm text-gray-600">提及 {person.frequency} 次</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* 使用提示 */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">💡 分析说明</h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>• <strong>综合分析</strong>：包含情绪、关键词、人际关系的全面分析</li>
          <li>• <strong>情绪分析</strong>：分析你的整体情绪状态和变化趋势</li>
          <li>• <strong>关键词</strong>：提取你最常提到的话题和概念</li>
          <li>• <strong>人际关系</strong>：分析你经常提到的人和关系网络</li>
        </ul>
      </div>
    </div>
  )
}
