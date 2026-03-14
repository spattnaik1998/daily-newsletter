'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import NewsletterViewer from '@/components/NewsletterViewer'
import StatsCard from '@/components/StatsCard'
import Archive from '@/components/Archive'
import { useNewsletter } from '@/lib/hooks/useNewsletter'
import { Download } from 'lucide-react'

export default function Dashboard() {
  const [activeView, setActiveView] = useState<'latest' | 'archive' | 'stats'>('latest')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [morningBrief, setMorningBrief] = useState<string | null>(null)
  const [briefLoading, setBriefLoading] = useState(true)
  const { newsletter, loading, stats, error } = useNewsletter()

  // Fetch morning brief
  useEffect(() => {
    const fetchBrief = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/morning-brief/latest')
        if (response.ok) {
          const data = await response.json()
          setMorningBrief(data.content)
        }
      } catch (err) {
        console.error('Failed to fetch morning brief:', err)
      } finally {
        setBriefLoading(false)
      }
    }
    fetchBrief()
  }, [])

  return (
    <div className="min-h-screen bg-slate-950 flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Content */}
      <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-0' : 'ml-0'}`}>
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} activeView={activeView} onViewChange={setActiveView} />

        {/* Content Area */}
        <div className="relative z-10 p-8 lg:p-12 max-w-7xl mx-auto">
          {/* Stats Overview */}
          {activeView === 'stats' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12 animate-fade-in">
              <StatsCard
                label="Latest Newsletter"
                value={stats?.date || 'Today'}
                icon="calendar"
                trend="up"
              />
              <StatsCard
                label="News Articles"
                value={stats?.articles || '0'}
                icon="newspaper"
                subtext="collected today"
              />
              <StatsCard
                label="Research Papers"
                value={stats?.papers || '0'}
                icon="book"
                subtext="from arXiv"
              />
              <StatsCard
                label="Newsletter Posts"
                value={stats?.posts || '0'}
                icon="mail"
                subtext="from Substack"
              />
            </div>
          )}

          {/* Morning Brief */}
          {activeView === 'latest' && (
            <div className="mb-12 animate-fade-in">
              <div className="bg-slate-900 bg-opacity-50 border border-slate-700 rounded-lg p-8">
                <h2 className="text-2xl font-bold text-cyan-400 mb-6">Executive Morning Brief</h2>
                {briefLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="w-8 h-8 border-2 border-accent-cyan border-t-transparent rounded-full animate-spin"></div>
                  </div>
                ) : morningBrief ? (
                  <div className="space-y-4">
                    <div className="text-slate-300 whitespace-pre-wrap text-sm leading-relaxed max-h-96 overflow-y-auto">
                      {morningBrief}
                    </div>
                    <button
                      onClick={() => {
                        const element = document.createElement('a')
                        const file = new Blob([morningBrief], { type: 'text/markdown' })
                        element.href = URL.createObjectURL(file)
                        element.download = `morning-brief-${new Date().toISOString().split('T')[0]}.md`
                        document.body.appendChild(element)
                        element.click()
                        document.body.removeChild(element)
                      }}
                      className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      <Download size={16} />
                      Download Brief
                    </button>
                  </div>
                ) : (
                  <p className="text-slate-400 text-sm">Morning brief not available. Generate a newsletter to create one.</p>
                )}
              </div>
            </div>
          )}

          {/* Latest Newsletter */}
          {activeView === 'latest' && (
            <div className="animate-fade-in">
              <div className="mb-8">
                <h1 className="text-4xl md:text-5xl font-display font-bold mb-2 text-cream-100">
                  Today's Newsletter
                </h1>
                <p className="text-slate-400 text-lg font-light">
                  {newsletter?.date || 'Loading latest insights...'}
                </p>
              </div>

              {error && (
                <div className="bg-rose-500 bg-opacity-10 border border-rose-500 border-opacity-30 rounded-lg p-6 mb-8">
                  <p className="text-rose-200">{error}</p>
                </div>
              )}

              {loading ? (
                <div className="flex items-center justify-center h-96">
                  <div className="space-y-4 text-center">
                    <div className="w-12 h-12 border-2 border-accent-cyan border-t-transparent rounded-full animate-spin mx-auto"></div>
                    <p className="text-slate-400">Generating newsletter...</p>
                  </div>
                </div>
              ) : newsletter ? (
                <NewsletterViewer content={newsletter.content} metadata={newsletter.metadata} />
              ) : (
                <div className="text-center py-16">
                  <p className="text-slate-400 mb-6">No newsletter generated yet.</p>
                  <button className="px-8 py-3 bg-accent-cyan text-slate-950 rounded-lg font-semibold hover:bg-accent-teal transition-colors">
                    Generate Now
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Archive */}
          {activeView === 'archive' && <Archive />}
        </div>
      </main>
    </div>
  )
}
