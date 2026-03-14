'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Download, Copy, Share2, Eye, FileText, Sparkles } from 'lucide-react'

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
    const file = new Blob([content], { type: format === 'md' ? 'text/markdown' : 'text/plain' })
    element.href = URL.createObjectURL(file)
    const now = new Date()
    const dateStr = now.toISOString().split('T')[0]
    element.download = `newsletter-${dateStr}.${format}`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode('preview')}
            className="px-3 py-1.5 rounded-lg transition-all text-xs font-medium"
            style={{
              background: viewMode === 'preview' ? 'rgba(0, 245, 255, 0.15)' : 'transparent',
              color: viewMode === 'preview' ? '#00f5ff' : '#94a3b8',
              border: viewMode === 'preview' ? '1px solid rgba(0, 245, 255, 0.3)' : '1px solid rgba(0, 245, 255, 0.1)',
            }}
          >
            <Eye size={14} className="inline mr-1" />
            Preview
          </button>
          <button
            onClick={() => setViewMode('raw')}
            className="px-3 py-1.5 rounded-lg transition-all text-xs font-medium"
            style={{
              background: viewMode === 'raw' ? 'rgba(0, 245, 255, 0.15)' : 'transparent',
              color: viewMode === 'raw' ? '#00f5ff' : '#94a3b8',
              border: viewMode === 'raw' ? '1px solid rgba(0, 245, 255, 0.3)' : '1px solid rgba(0, 245, 255, 0.1)',
            }}
          >
            <FileText size={14} className="inline mr-1" />
            Raw
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-lg transition-all text-xs font-medium text-slate-400 hover:text-slate-300"
            style={{
              border: '1px solid rgba(0, 245, 255, 0.1)',
            }}
            title="Copy to clipboard"
          >
            <Copy size={14} className="inline mr-1" />
            {copied ? 'Copied' : 'Copy'}
          </button>
          <button
            onClick={() => handleDownload('md')}
            className="px-3 py-1.5 rounded-lg transition-all text-xs font-medium text-slate-400 hover:text-slate-300"
            style={{
              border: '1px solid rgba(0, 245, 255, 0.1)',
            }}
          >
            <Download size={14} className="inline mr-1" />
            Download
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="rounded-lg overflow-hidden" style={{
        background: 'rgba(0, 245, 255, 0.02)',
        border: '1px solid rgba(0, 245, 255, 0.08)',
      }}>
        {viewMode === 'preview' ? (
          <article className="p-6 lg:p-8 max-w-none prose prose-invert prose-sm">
            <style>{`
              .prose {
                --tw-prose-body: #cbd5e1;
                --tw-prose-headings: #00f5ff;
                --tw-prose-lead: #cbd5e1;
                --tw-prose-links: #00f5ff;
                --tw-prose-bold: #f1f5f9;
                --tw-prose-counters: #f1f5f9;
                --tw-prose-bullets: #00f5ff;
                --tw-prose-hr: rgba(0, 245, 255, 0.15);
                --tw-prose-quotes: #cbd5e1;
                --tw-prose-quote-borders: rgba(0, 245, 255, 0.2);
                --tw-prose-captions: #94a3b8;
                --tw-prose-code: #00f5ff;
                --tw-prose-pre-code: #cbd5e1;
                --tw-prose-pre-bg: rgba(15, 23, 42, 0.6);
                --tw-prose-pre-border: rgba(0, 245, 255, 0.1);
                --tw-prose-th-borders: rgba(0, 245, 255, 0.15);
                --tw-prose-td-borders: rgba(0, 245, 255, 0.08);
              }

              .prose h1 { font-size: 1.875rem; font-weight: 700; margin-bottom: 1rem; color: #00f5ff; }
              .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.75rem; color: #00f5ff; }
              .prose h3 { font-size: 1.125rem; font-weight: 600; margin-top: 1rem; margin-bottom: 0.5rem; color: #00d4ff; }

              .prose a { text-decoration: none; border-bottom: 1px solid rgba(0, 245, 255, 0.3); transition: all 0.2s; }
              .prose a:hover { color: #00d4ff; border-bottom-color: #00d4ff; }

              .prose pre { border-radius: 0.375rem; overflow-x: auto; padding: 1rem; border: 1px solid rgba(0, 245, 255, 0.1); }
              .prose code { font-size: 0.8rem; }

              .prose ul, .prose ol { margin-left: 1.25rem; }
              .prose li { margin-top: 0.25rem; margin-bottom: 0.25rem; }

              .prose hr { border: none; border-top: 1px solid rgba(0, 245, 255, 0.15); margin: 1.5rem 0; }
            `}</style>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {content}
            </ReactMarkdown>
          </article>
        ) : (
          <div className="p-6 lg:p-8 overflow-x-auto">
            <pre className="font-mono text-xs text-slate-300 leading-relaxed">
              <code>{content}</code>
            </pre>
          </div>
        )}
      </div>

      {/* Themes Section */}
      {metadata?.themes && metadata.themes.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">Emerging Themes</h3>
          <div className="flex flex-wrap gap-2">
            {metadata.themes.map((theme) => (
              <span
                key={theme}
                className="px-3 py-1 rounded-full text-xs font-medium"
                style={{
                  background: 'rgba(0, 245, 255, 0.1)',
                  color: '#00f5ff',
                  border: '1px solid rgba(0, 245, 255, 0.2)',
                }}
              >
                {theme}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
