'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { ChevronDown, Download, Share2, Bookmark, Zap, Sparkles, BookOpen, Users, Lightbulb, Newspaper } from 'lucide-react'
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
  const [saved, setSaved] = useState(false)

  if (!content) {
    return (
      <div className="p-8 text-center text-slate-400">
        <p>No newsletter content available</p>
      </div>
    )
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
      {metadata && (
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-4 p-6 glass rounded-lg border border-slate-700"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="text-center">
            <div className="text-2xl font-bold gradient-text">{metadata.articles_count || 0}</div>
            <div className="text-sm text-slate-400">News Articles</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold gradient-text">{metadata.papers_count || 0}</div>
            <div className="text-sm text-slate-400">Research Papers</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold gradient-text">{metadata.posts_count || 0}</div>
            <div className="text-sm text-slate-400">Newsletter Posts</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold gradient-text">{metadata.themes?.length || 0}</div>
            <div className="text-sm text-slate-400">Emerging Themes</div>
          </div>
        </motion.div>
      )}

      {/* Full Newsletter Content */}
      <motion.div
        className="border border-slate-700 rounded-xl overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <div className="p-8 bg-slate-900 bg-opacity-50 prose prose-invert max-w-none overflow-auto max-h-[70vh]">
          <ReactMarkdown
            components={{
              h1: ({ node, ...props }) => <h1 className="text-3xl font-bold text-white mt-6 mb-4 gradient-text" {...props} />,
              h2: ({ node, ...props }) => <h2 className="text-2xl font-bold text-white mt-5 mb-3 text-cyan-400" {...props} />,
              h3: ({ node, ...props }) => <h3 className="text-xl font-semibold text-slate-100 mt-4 mb-2" {...props} />,
              p: ({ node, ...props }) => <p className="text-slate-300 mb-4 leading-relaxed" {...props} />,
              ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-4 space-y-2" {...props} />,
              ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-4 space-y-2" {...props} />,
              li: ({ node, ...props }) => <li className="text-slate-300" {...props} />,
              strong: ({ node, ...props }) => <strong className="text-cyan-300 font-semibold" {...props} />,
              em: ({ node, ...props }) => <em className="text-slate-200 italic" {...props} />,
              a: ({ node, href, ...props }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-cyan-400 hover:text-cyan-300 underline hover:underline-offset-2 transition-colors"
                  {...props}
                />
              ),
              code: ({ node, inline, ...props }) =>
                inline ? (
                  <code className="bg-slate-800 text-cyan-300 px-2 py-1 rounded text-sm font-mono" {...props} />
                ) : (
                  <code className="block bg-slate-800 text-slate-300 p-4 rounded-lg overflow-x-auto font-mono text-sm mb-4" {...props} />
                ),
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-cyan-500 pl-4 italic text-slate-400 my-4" {...props} />
              ),
              hr: ({ node, ...props }) => <hr className="border-t border-slate-700 my-6" {...props} />
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
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
