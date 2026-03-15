'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import TieredNewsletterViewer from '@/components/TieredNewsletterViewer'
import PipelineStatsPanel from '@/components/PipelineStatsPanel'
import SettingsPanel from '@/components/SettingsPanel'
import UserProfilePanel from '@/components/UserProfilePanel'
import Archive from '@/components/Archive'
import { Zap, Settings, User, BookOpen, BarChart3 } from 'lucide-react'

type ActiveView = 'latest' | 'archive' | 'stats' | 'settings' | 'profile'

export default function Dashboard() {
  const [activeView, setActiveView] = useState<ActiveView>('latest')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isGenerating, setIsGenerating] = useState(false)
  const [newsletter, setNewsletter] = useState<any>(null)
  const [pipelineStats, setPipelineStats] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Fetch latest newsletter on mount
  useEffect(() => {
    fetchLatestNewsletter()
    fetchStats()
  }, [])

  const fetchLatestNewsletter = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:8000/api/newsletter/latest')
      const data = await response.json()

      if (data.status === 'success') {
        setNewsletter({
          content: data.data.content,
          date: data.data.date,
          metadata: data.data.metadata || {
            date: data.data.date,
            articles_count: 0,
            papers_count: 0,
            posts_count: 0,
            themes: []
          }
        })
        setError(null)
      } else {
        setError(data.message || 'Failed to fetch newsletter')
      }
    } catch (err) {
      console.error('Error fetching newsletter:', err)
      setError('Failed to fetch newsletter. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/stats')
      const data = await response.json()

      if (data.status === 'success') {
        setPipelineStats(data.data)
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const handleGenerateNewsletter = async () => {
    try {
      setIsGenerating(true)
      setError(null)

      const response = await fetch('http://localhost:8000/api/newsletter/generate', {
        method: 'POST'
      })

      const data = await response.json()

      if (data.status === 'success') {
        // Poll for completion
        let completed = false
        let attempts = 0
        const maxAttempts = 60 // 5 minutes max

        while (!completed && attempts < maxAttempts) {
          await new Promise(resolve => setTimeout(resolve, 5000)) // Wait 5 seconds

          const statusResponse = await fetch('http://localhost:8000/api/newsletter/status')
          const statusData = await statusResponse.json()

          if (!statusData.data.is_generating) {
            completed = true
            await fetchLatestNewsletter()
            await fetchStats()
          }

          attempts++
        }

        if (!completed) {
          setError('Generation timed out')
        }
      } else {
        setError(data.message || 'Failed to generate newsletter')
      }
    } catch (err) {
      console.error('Error generating newsletter:', err)
      setError('Failed to generate newsletter')
    } finally {
      setIsGenerating(false)
    }
  }

  const navItems = [
    {
      id: 'latest',
      label: 'Latest',
      icon: <BookOpen size={20} />,
      badge: null
    },
    {
      id: 'stats',
      label: 'Performance',
      icon: <BarChart3 size={20} />,
      badge: null
    },
    {
      id: 'profile',
      label: 'Profile',
      icon: <User size={20} />,
      badge: null
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: <Settings size={20} />,
      badge: null
    },
    {
      id: 'archive',
      label: 'Archive',
      icon: <BookOpen size={20} />,
      badge: null
    }
  ] as const

  return (
    <div className="min-h-screen bg-slate-950 flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Content */}
      <main className="flex-1 transition-all duration-300">
        {/* Header */}
        <header className="sticky top-0 z-40 glass border-b border-slate-700">
          <div className="px-8 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-2xl font-bold text-white">Daily AI Newsletter</h1>
            </div>

            <button
              onClick={handleGenerateNewsletter}
              disabled={isGenerating}
              className="flex items-center gap-2 px-6 py-2 bg-gradient-to-r from-cyan-600 to-teal-600 hover:from-cyan-700 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all"
            >
              <Zap size={18} />
              {isGenerating ? 'Generating...' : 'Generate Now'}
            </button>
          </div>

          {/* Navigation Tabs */}
          <div className="px-8 border-t border-slate-700 flex gap-1 overflow-x-auto">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => setActiveView(item.id as ActiveView)}
                className={`px-4 py-4 font-medium text-sm flex items-center gap-2 border-b-2 transition-all whitespace-nowrap ${
                  activeView === item.id
                    ? 'border-cyan-500 text-cyan-400'
                    : 'border-transparent text-slate-400 hover:text-slate-300'
                }`}
              >
                {item.icon}
                {item.label}
                {item.badge && (
                  <span className="ml-2 px-2 py-1 bg-cyan-600 text-white text-xs rounded-full">
                    {item.badge}
                  </span>
                )}
              </button>
            ))}
          </div>
        </header>

        {/* Content Area */}
        <div className="relative z-10 p-8 lg:p-12 max-w-7xl mx-auto">
          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 bg-rose-500 bg-opacity-15 border border-rose-500 border-opacity-30 rounded-lg text-rose-400 flex items-center gap-2"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </motion.div>
          )}

          {/* Latest Newsletter */}
          {activeView === 'latest' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <div>
                <h1 className="text-4xl md:text-5xl font-bold mb-2 gradient-text">
                  Today's Newsletter
                </h1>
                <p className="text-slate-400 text-lg">
                  {newsletter?.date ? `Generated on ${newsletter.date}` : 'Loading...'}
                </p>
              </div>

              {loading ? (
                <div className="flex items-center justify-center h-96">
                  <div className="space-y-4 text-center">
                    <div className="w-12 h-12 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
                    <p className="text-slate-400">Loading newsletter...</p>
                  </div>
                </div>
              ) : newsletter ? (
                <TieredNewsletterViewer
                  content={newsletter.content}
                  metadata={newsletter.metadata}
                />
              ) : (
                <div className="glass rounded-xl p-12 border border-slate-700 text-center">
                  <p className="text-slate-400 mb-6">No newsletter generated yet.</p>
                  <button
                    onClick={handleGenerateNewsletter}
                    disabled={isGenerating}
                    className="px-8 py-3 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 text-white rounded-lg font-semibold transition-colors"
                  >
                    {isGenerating ? 'Generating...' : 'Generate First Newsletter'}
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {/* Performance Stats */}
          {activeView === 'stats' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="mb-8">
                <h1 className="text-4xl font-bold mb-2 gradient-text">Pipeline Performance</h1>
                <p className="text-slate-400 text-lg">Real-time metrics and statistics</p>
              </div>
              <PipelineStatsPanel stats={pipelineStats} isLoading={loading} />
            </motion.div>
          )}

          {/* User Profile */}
          {activeView === 'profile' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="mb-8">
                <h1 className="text-4xl font-bold mb-2 gradient-text">Your Profile</h1>
                <p className="text-slate-400 text-lg">Personalize your newsletter experience</p>
              </div>
              <UserProfilePanel />
            </motion.div>
          )}

          {/* Settings */}
          {activeView === 'settings' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="mb-8">
                <h1 className="text-4xl font-bold mb-2 gradient-text">Settings</h1>
                <p className="text-slate-400 text-lg">Configure pipeline behavior and data sources</p>
              </div>
              <SettingsPanel />
            </motion.div>
          )}

          {/* Archive */}
          {activeView === 'archive' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="mb-8">
                <h1 className="text-4xl font-bold mb-2 gradient-text">Newsletter Archive</h1>
                <p className="text-slate-400 text-lg">View past newsletters</p>
              </div>
              <Archive />
            </motion.div>
          )}
        </div>
      </main>
    </div>
  )
}
