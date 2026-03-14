'use client'

import { useState } from 'react'
import { Calendar, Search, ChevronRight, Download } from 'lucide-react'
import { format, subDays } from 'date-fns'

interface NewsletterItem {
  id: string
  date: Date
  title: string
  articleCount: number
  paperCount: number
  postCount: number
  themes: string[]
}

export default function Archive() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedDate, setSelectedDate] = useState<Date | null>(null)

  // Mock data - replace with API call
  const mockArchive: NewsletterItem[] = Array.from({ length: 30 }, (_, i) => ({
    id: `newsletter-${i}`,
    date: subDays(new Date(), i),
    title: `Daily AI Newsletter - ${format(subDays(new Date(), i), 'MMM d, yyyy')}`,
    articleCount: Math.floor(Math.random() * 15) + 5,
    paperCount: Math.floor(Math.random() * 20) + 8,
    postCount: Math.floor(Math.random() * 12) + 4,
    themes: ['Agentic AI', 'Multimodal', 'Robotics'].slice(0, Math.floor(Math.random() * 3) + 1),
  }))

  const filteredArchive = mockArchive.filter(
    (item) =>
      item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.date.toDateString().includes(searchTerm)
  )

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl md:text-5xl font-display font-bold mb-2 text-cream-100">
          Newsletter Archive
        </h1>
        <p className="text-slate-400 text-lg font-light">
          Browse all generated newsletters
        </p>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-4 top-3.5 text-slate-500" size={20} />
        <input
          type="text"
          placeholder="Search by date or content..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-12 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-300 placeholder-slate-500 focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan outline-none transition-all"
        />
      </div>

      {/* Archive List */}
      <div className="space-y-3">
        {filteredArchive.length > 0 ? (
          filteredArchive.map((item, idx) => (
            <div
              key={item.id}
              className="group p-5 bg-gradient-to-r from-slate-800 to-slate-900 border border-slate-700 rounded-lg hover:border-accent-cyan transition-all duration-300 hover:shadow-lg hover:shadow-cyan-500/10 cursor-pointer"
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                {/* Left: Date and Title */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Calendar size={16} className="text-accent-cyan opacity-60" />
                    <span className="text-sm text-slate-500 font-mono">
                      {format(item.date, 'MMM d, yyyy')}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-cream-100 group-hover:text-accent-cyan transition-colors">
                    {item.title}
                  </h3>
                </div>

                {/* Center: Stats */}
                <div className="flex items-center gap-6 md:gap-8 text-sm">
                  <div className="text-center">
                    <p className="text-slate-500 text-xs uppercase mb-1">Articles</p>
                    <p className="font-display text-xl font-bold text-accent-teal">{item.articleCount}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-500 text-xs uppercase mb-1">Papers</p>
                    <p className="font-display text-xl font-bold text-accent-cyan">{item.paperCount}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-slate-500 text-xs uppercase mb-1">Posts</p>
                    <p className="font-display text-xl font-bold text-accent-gold">{item.postCount}</p>
                  </div>
                </div>

                {/* Right: Actions */}
                <div className="flex items-center gap-2">
                  <button className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-400 hover:text-accent-cyan">
                    <Download size={18} />
                  </button>
                  <ChevronRight size={20} className="text-slate-500 group-hover:text-accent-cyan transition-colors" />
                </div>
              </div>

              {/* Themes tags */}
              {item.themes.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-700 flex flex-wrap gap-2">
                  {item.themes.map((theme) => (
                    <span
                      key={theme}
                      className="text-xs px-3 py-1 bg-slate-700 text-slate-300 rounded-full hover:bg-accent-cyan hover:text-slate-950 transition-colors"
                    >
                      {theme}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))
        ) : (
          <div className="text-center py-12">
            <p className="text-slate-400 mb-4">No newsletters found matching your search.</p>
            <button
              onClick={() => setSearchTerm('')}
              className="text-accent-cyan hover:text-accent-teal transition-colors"
            >
              Clear search
            </button>
          </div>
        )}
      </div>

      {/* Pagination Info */}
      <div className="mt-8 text-center">
        <p className="text-slate-500 text-sm">
          Showing {filteredArchive.length} of {mockArchive.length} newsletters
        </p>
      </div>
    </div>
  )
}
