import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, Upload, Settings, MessageCircle, Brain, Clock } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: '首页' },
    { path: '/upload', icon: Upload, label: '数据上传' },
    { path: '/config', icon: Settings, label: '配置' },
    { path: '/mimic', icon: MessageCircle, label: '模仿我说话' },
    { path: '/analysis', icon: Brain, label: '自我认知' },
    { path: '/memory', icon: Clock, label: '记忆回溯' },
  ]

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary-600">Another Me</h1>
          <p className="text-sm text-gray-500 mt-1">世界上另一个我</p>
        </div>
        
        <nav className="mt-6">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-6 py-3 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-50 text-primary-600 border-r-4 border-primary-600'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-5 h-5 mr-3" />
                {item.label}
              </Link>
            )
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 bg-gray-50 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          {children}
        </div>
      </main>
    </div>
  )
}
