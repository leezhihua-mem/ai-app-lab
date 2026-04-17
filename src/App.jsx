import React from 'react'
import appsData from '../apps.json'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-potato-50 to-potato-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-potato-600">
            🥔 土豆AI应用实验室
          </h1>
          <p className="text-gray-600 mt-2">
            AI App Lab by Potato Agent System
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Search */}
        <div className="mb-8">
          <input
            type="text"
            placeholder="搜索应用..."
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-potato-400 focus:outline-none"
          />
        </div>

        {/* Apps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {appsData.apps.map((app, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6"
            >
              <div className="flex items-center mb-4">
                <span className="text-4xl mr-3">{app.icon}</span>
                <h3 className="text-xl font-semibold text-gray-800">
                  {app.name}
                </h3>
              </div>
              
              <p className="text-gray-600 mb-4">{app.description}</p>
              
              <div className="flex items-center justify-between">
                <span className={`px-3 py-1 rounded-full text-sm ${
                  app.status === '已部署' 
                    ? 'bg-green-100 text-green-600'
                    : app.status === '开发中'
                    ? 'bg-yellow-100 text-yellow-600'
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {app.status}
                </span>
                
                <span className="text-sm text-gray-500">
                  {app.category}
                </span>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="text-sm text-gray-500">
                  技术栈：
                  {app.tech_stack.map((tech, i) => (
                    <span key={i} className="inline-block mr-2">
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-8">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <div className="text-gray-600">
              <p>🥔 土豆AI应用实验室</p>
              <p className="text-sm mt-1">
                GitHub: <a 
                  href="https://github.com/leezhihua-mem/ai-app-lab"
                  className="text-potato-600 hover:underline"
                >
                  leezhihua-mem/ai-app-lab
                </a>
              </p>
            </div>
            
            <div className="text-gray-500 text-sm">
              创建时间：2026-04-17
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App