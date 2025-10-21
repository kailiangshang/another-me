import { useState } from 'react'
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
      </div>

      {/* 生成报告按钮 */}
      <div className="flex justify-center">
        <button
          onClick={generateReport}
          disabled={loading}
          className="flex items-center gap-2 bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50"
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
      </div>

      {/* 错误信息 */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          {error}
        </div>
      )}

      {/* 报告展示 */}
      {report && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">分析报告</h2>
          <div className="prose max-w-none">
            {typeof report === 'string' ? (
              <div dangerouslySetInnerHTML={{ __html: report.replace(/\n/g, '<br />') }} />
            ) : (
              <pre className="whitespace-pre-wrap">{JSON.stringify(report, null, 2)}</pre>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
