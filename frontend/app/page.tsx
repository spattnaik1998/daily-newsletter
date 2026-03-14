'use client'

import { useState, useEffect } from 'react'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'
import NewsletterViewer from '@/components/NewsletterViewer'
import StatsCard from '@/components/StatsCard'
import Archive from '@/components/Archive'
import { useNewsletter } from '@/lib/hooks/useNewsletter'

export default function Dashboard() {
  const [activeView, setActiveView] = useState<'latest' | 'archive' | 'stats'>('latest')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const { newsletter, loading, stats, error } = useNewsletter()

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
