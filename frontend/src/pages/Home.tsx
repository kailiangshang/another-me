import { Link } from 'react-router-dom'
import { MessageCircle, Brain, Clock, Upload, Settings } from 'lucide-react'

export default function Home() {
  const features = [
    {
      icon: MessageCircle,
      title: '模仿我说话',
      description: '让 AI 用你的语气、风格和思维方式回应问题',
      path: '/mimic',
      color: 'bg-blue-500',
    },
    {
      icon: Brain,
      title: '自我认知分析',
      description: '帮你更客观地认识自己，发现盲点',
      path: '/analysis',
      color: 'bg-purple-500',
    },
    {
      icon: Clock,
      title: '记忆回溯对话',
      description: '唤醒你遗忘的记忆,实现"时空对话"',
      path: '/memory',
      color: 'bg-pink-500',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          欢迎来到 <span className="text-primary-600">Another Me</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          用你的数据训练一个"像你"的 AI 分身 🌟
        </p>
        <p className="text-gray-500 mb-8">
          隐私优先 · 本地存储 · 完全开源
        </p>
        
        <div className="flex gap-4 justify-center">
          <Link
            to="/upload"
            className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Upload className="w-5 h-5" />
            开始上传数据
          </Link>
          <Link
            to="/config"
            className="flex items-center gap-2 bg-gray-200 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-300 transition-colors"
          >
            <Settings className="w-5 h-5" />
            配置 API
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <Link
              key={feature.path}
              to={feature.path}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
            >
              <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </Link>
          )
        })}
      </div>

      {/* Quick Start Guide */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          🚀 快速开始
        </h2>
        <ol className="space-y-3 text-gray-700">
          <li className="flex items-start">
            <span className="bg-primary-600 text-white w-6 h-6 rounded-full flex items-center justify-center mr-3 flex-shrink-0">1</span>
            <span><strong>配置 API Key</strong> - 在配置页面填入 OpenAI 兼容的 API 密钥</span>
          </li>
          <li className="flex items-start">
            <span className="bg-primary-600 text-white w-6 h-6 rounded-full flex items-center justify-center mr-3 flex-shrink-0">2</span>
            <span><strong>上传数据</strong> - 上传聊天记录、日记、照片等个人数据</span>
          </li>
          <li className="flex items-start">
            <span className="bg-primary-600 text-white w-6 h-6 rounded-full flex items-center justify-center mr-3 flex-shrink-0">3</span>
            <span><strong>开始体验</strong> - 尝试三大核心功能，与"另一个你"对话</span>
          </li>
        </ol>
      </div>
    </div>
  )
}
