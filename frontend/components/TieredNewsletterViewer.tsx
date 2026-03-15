'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { ChevronDown, Download, Share2, Bookmark, Zap, Sparkles, BookOpen, Users, Lightbulb } from 'lucide-react'
import { motion } from 'framer-motion'

interface NewsletterSection {
  type: 'lead' | 'must-read' | 'news' | 'spotlight' | 'insights' | 'themes' | 'papers'
  title: string
  icon: React.ReactNode
  content: string
  items?: Array<{
    title: string
    source?: string
    url?: string
    summary?: string
    badge?: string
  }>
}

interface TieredNewsletterViewerProps {
  content: string
  metadata?: {
    date?: string
    articles_count?: number
    papers_count?: number
    posts_count?: number
    themes?: string[]
  }
}

export default function TieredNewsletterViewer({ content, metadata }: TieredNewsletterViewerProps) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({})
  const [saved, setSaved] = useState(false)

  const toggleSection = (id: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [id]: !prev[id]
    }))
  }

  const sections: NewsletterSection[] = [
    {
      type: 'lead',
      title: 'Lead Story',
      icon: <Zap className="w-5 h-5" />,
      content: 'The single most important AI development today'
    },
    {
      type: 'must-read',
      title: 'Must Read Today',
      icon: <Sparkles className="w-5 h-5" />,
      content: 'Top 3 developments that move the needle'
    },
    {
      type: 'news',
      title: 'AI News Briefing',
      icon: <Newspaper className="w-5 h-5" />,
      content: `${metadata?.articles_count || 0} articles from 17 sources`
    },
    {
      type: 'spotlight',
      title: 'Research Spotlight',
      icon: <BookOpen className="w-5 h-5" />,
      content: 'Featured paper worth deep-diving into'
    },
    {
      type: 'insights',
      title: 'Community Insights',
      icon: <Users className="w-5 h-5" />,
      content: `${metadata?.posts_count || 0} posts from 12 newsletters`
    },
    {
      type: 'themes',
      title: 'Emerging Themes',
      icon: <Lightbulb className="w-5 h-5" />,
      content: metadata?.themes?.join(', ') || 'Detected patterns'
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <div className="space-y-8">
      {/* Header Actions */}
      <motion.div
        className="flex gap-3 flex-wrap"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <button className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg font-medium transition-colors">
          <Download size={18} />
          Download
        </button>
        <button className="flex items-center gap-2 px-4 py-2 border border-slate-600 hover:border-cyan-500 text-slate-300 rounded-lg font-medium transition-colors">
          <Share2 size={18} />
          Share
        </button>
        <button
          onClick={() => setSaved(!saved)}
          className={`flex items-center gap-2 px-4 py-2 border rounded-lg font-medium transition-colors ${
            saved
              ? 'border-cyan-500 bg-cyan-500 bg-opacity-10 text-cyan-400'
              : 'border-slate-600 text-slate-300 hover:border-cyan-500'
          }`}
        >
          <Bookmark size={18} fill={saved ? 'currentColor' : 'none'} />
          {saved ? 'Saved' : 'Save'}
        </button>
      </motion.div>

      {/* Newsletter Metadata */}
      <motion.div
        className="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 glass rounded-lg"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <div className="text-center">
          <div className="text-2xl font-bold gradient-text">{metadata?.articles_count || 0}</div>
          <div className="text-sm text-slate-400">News Articles</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold gradient-text">{metadata?.papers_count || 0}</div>
          <div className="text-sm text-slate-400">Research Papers</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold gradient-text">{metadata?.posts_count || 0}</div>
          <div className="text-sm text-slate-400">Newsletter Posts</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold gradient-text">{metadata?.themes?.length || 0}</div>
          <div className="text-sm text-slate-400">Emerging Themes</div>
        </div>
      </motion.div>

      {/* Newsletter Sections */}
      <motion.div
        className="space-y-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {sections.map((section, index) => (
          <motion.div
            key={section.type}
            variants={itemVariants}
            className="border border-slate-700 rounded-xl overflow-hidden hover-lift"
          >
            {/* Section Header */}
            <button
              onClick={() => toggleSection(section.type)}
              className="w-full p-6 bg-gradient-to-r from-slate-800 to-slate-900 hover:from-slate-700 hover:to-slate-800 transition-colors flex items-center justify-between group"
            >
              <div className="flex items-center gap-4 text-left flex-1">
                <div className="text-cyan-400 group-hover:text-cyan-300 transition-colors">
                  {section.icon}
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white group-hover:text-cyan-300 transition-colors">
                    {section.title}
                  </h3>
                  <p className="text-sm text-slate-400">{section.content}</p>
                </div>
              </div>
              <motion.div
                animate={{ rotate: expandedSections[section.type] ? 180 : 0 }}
                transition={{ duration: 0.3 }}
              >
                <ChevronDown size={20} className="text-slate-400" />
              </motion.div>
            </button>

            {/* Section Content */}
            <motion.div
              initial={false}
              animate={{ height: expandedSections[section.type] ? 'auto' : 0 }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="p-6 border-t border-slate-700 bg-slate-900 bg-opacity-50 prose prose-invert max-w-none">
                <ReactMarkdown
                  components={{
                    p: ({ node, ...props }) => <p className="text-slate-300 mb-4" {...props} />,
                    li: ({ node, ...props }) => <li className="text-slate-300 ml-6" {...props} />,
                    strong: ({ node, ...props }) => <strong className="text-cyan-400 font-semibold" {...props} />,
                    a: ({ node, href, ...props }) => (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-cyan-400 hover:text-cyan-300 underline"
                        {...props}
                      />
                    )
                  }}
                >
                  {content}
                </ReactMarkdown>
              </div>
            </motion.div>
          </motion.div>
        ))}
      </motion.div>

      {/* Emerging Themes Visualization */}
      {metadata?.themes && metadata.themes.length > 0 && (
        <motion.div
          className="p-6 glass rounded-xl border border-slate-700"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <h3 className="text-lg font-semibold text-white mb-4">Key Themes Detected</h3>
          <div className="flex flex-wrap gap-2">
            {metadata.themes.map((theme, index) => (
              <motion.div
                key={theme}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.5 + index * 0.05 }}
                className="badge badge-cyan"
              >
                {theme}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}

// Icon component since we can't import directly
function Newspaper({ className }: { className: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2m2 2a2 2 0 002-2m-2 2v-6a2 2 0 012-2h2.5a2 2 0 002-2v-1" />
    </svg>
  )
}
