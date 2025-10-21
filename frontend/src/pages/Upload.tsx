import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import { uploadAPI } from '@/api'

export default function Upload() {
  const [uploading, setUploading] = useState(false)
  const [uploadResults, setUploadResults] = useState<any[]>([])
  const [error, setError] = useState<string>('')
  const [text, setText] = useState('')
  const [stats, setStats] = useState<any>(null)

  // 获取统计信息
  const fetchStats = async () => {
    try {
      const data = await uploadAPI.getStatus()
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  // 文件上传
  const onDrop = async (acceptedFiles: File[]) => {
    setUploading(true)
    setError('')
    
    try {
      const result = await uploadAPI.uploadFiles(acceptedFiles)
      setUploadResults(result.files || [])
      await fetchStats()
    } catch (err: any) {
      setError(err.message || '上传失败')
    } finally {
      setUploading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/json': ['.json'],
      'text/markdown': ['.md'],
    },
  })

  // 文本上传
  const handleTextUpload = async () => {
    if (!text.trim()) return
    
    setUploading(true)
    setError('')
    
    try {
      await uploadAPI.uploadText(text, 'manual')
      setText('')
      await fetchStats()
    } catch (err: any) {
      setError(err.message || '上传失败')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">数据上传</h1>
        <p className="text-gray-600">上传你的聊天记录、日记、照片等数据，训练专属 AI</p>
      </div>

      {/* 统计卡片 */}
      {stats && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">数据统计</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-gray-600">总文档数</p>
              <p className="text-2xl font-bold text-primary-600">{stats.total_documents || 0}</p>
            </div>
            <div>
              <p className="text-gray-600">最后更新</p>
              <p className="text-sm text-gray-800">
                {stats.last_updated ? new Date(stats.last_updated).toLocaleString('zh-CN') : 'N/A'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 文件上传区域 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">上传文件</h2>
        
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          <UploadIcon className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          {isDragActive ? (
            <p className="text-lg text-primary-600">释放以上传文件...</p>
          ) : (
            <>
              <p className="text-lg text-gray-700 mb-2">拖拽文件到此处，或点击选择</p>
              <p className="text-sm text-gray-500">支持 .txt, .json, .md 格式</p>
            </>
          )}
        </div>

        {uploading && (
          <div className="mt-4 text-center text-primary-600">
            上传中...
          </div>
        )}

        {error && (
          <div className="mt-4 flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        {uploadResults.length > 0 && (
          <div className="mt-4 space-y-2">
            {uploadResults.map((result, idx) => (
              <div key={idx} className="flex items-center gap-2 text-green-600 bg-green-50 p-3 rounded">
                <CheckCircle className="w-5 h-5" />
                <span>{result.filename} - 已处理 {result.processed} 条</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 文本输入上传 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">直接输入文本</h2>
        
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="粘贴或输入文本内容..."
          className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        
        <button
          onClick={handleTextUpload}
          disabled={!text.trim() || uploading}
          className="mt-4 flex items-center gap-2 bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <FileText className="w-5 h-5" />
          上传文本
        </button>
      </div>

      <button
        onClick={fetchStats}
        className="text-primary-600 hover:text-primary-700"
      >
        刷新统计
      </button>
    </div>
  )
}
