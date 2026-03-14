'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Download, Copy, Share2, Eye, FileText, Zap } from 'lucide-react'

interface NewsletterViewerProps {
  content: string
  metadata?: {
    articles?: number
    papers?: number
    posts?: number
    themes?: string[]
  }
}

export default function NewsletterViewer({ content, metadata }: NewsletterViewerProps) {
  const [copied, setCopied] = useState(false)
  const [viewMode, setViewMode] = useState<'preview' | 'raw'>('preview')

  const handleCopy = () => {
    navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = (format: 'md' | 'txt') => {
    const element = document.createElement('a')
    const file = new Blob([content], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `newsletter.${format}`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="space-y-6">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 bg-slate-800 border border-slate-700 rounded-lg">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setViewMode('preview')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm font-medium ${
              viewMode === 'preview'
                ? 'bg-accent-cyan text-slate-950'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Eye size={16} />
            Preview
          </button>
          <button
            onClick={() => setViewMode('raw')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors text-sm font-medium ${
              viewMode === 'raw'
                ? 'bg-accent-cyan text-slate-950'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText size={16} />
            Raw
          </button>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-4 py-2 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors text-sm font-medium"
            title="Copy to clipboard"
          >
            <Copy size={16} />
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <div className="relative group">
            <button className="flex items-center gap-2 px-4 py-2 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors text-sm font-medium">
              <Download size={16} />
              Download
            </button>
            <div className="absolute right-0 mt-2 w-40 bg-slate-900 border border-slate-700 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none group-hover:pointer-events-auto z-50">
              <button
                onClick={() => handleDownload('md')}
                className="w-full text-left px-4 py-2 hover:bg-slate-800 transition-colors text-sm text-slate-300 first:rounded-t-lg"
              >
                Markdown (.md)
              </button>
              <button
                onClick={() => handleDownload('txt')}
                className="w-full text-left px-4 py-2 hover:bg-slate-800 transition-colors text-sm text-slate-300 last:rounded-b-lg"
              >
                Text (.txt)
              </button>
            </div>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors text-sm font-medium">
            <Share2 size={16} />
            Share
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="border border-slate-700 rounded-lg overflow-hidden bg-gradient-to-b from-slate-900 to-slate-950">
        {viewMode === 'preview' ? (
          <article className="prose prose-invert max-w-none p-8 lg:p-12">
            <div className="prose-headings:font-display prose-headings:text-cream-100 prose-p:text-slate-300 prose-a:text-accent-cyan hover:prose-a:text-accent-teal prose-strong:text-cream-100 prose-code:text-accent-gold prose-pre:bg-slate-800 prose-ul:text-slate-300 prose-ol:text-slate-300 prose-li:text-slate-300">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
            </div>
          </article>
        ) : (
          <div className="p-8 lg:p-12 overflow-x-auto">
            <pre className="font-mono text-sm text-slate-300 leading-relaxed">
              <code>{content}</code>
            </pre>
          </div>
        )}
      </div>

      {/* Metadata Footer */}
      {metadata && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-slate-800 border border-slate-700 rounded-lg">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Articles</p>
            <p className="text-2xl font-display font-bold text-accent-teal">{metadata.articles || 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Papers</p>
            <p className="text-2xl font-display font-bold text-accent-cyan">{metadata.papers || 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Posts</p>
            <p className="text-2xl font-display font-bold text-accent-gold">{metadata.posts || 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-1">Themes</p>
            <p className="text-2xl font-display font-bold text-accent-rose">{metadata.themes?.length || 0}</p>
          </div>
        </div>
      )}
    </div>
  )
}
