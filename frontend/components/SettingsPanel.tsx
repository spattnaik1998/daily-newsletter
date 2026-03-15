'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Save, RotateCcw, Clock, Zap, Database, Settings as SettingsIcon } from 'lucide-react'

interface Settings {
  cache_ttl: number
  news_lookback_hours: number
  substack_lookback_hours: number
  max_articles: number
  max_papers: number
  max_posts: number
  auto_generate: boolean
  auto_generate_time: string
}

interface SettingsPanelProps {
  onSave?: (settings: Settings) => Promise<void>
}

const DEFAULT_SETTINGS: Settings = {
  cache_ttl: 6,
  news_lookback_hours: 24,
  substack_lookback_hours: 168,
  max_articles: 10,
  max_papers: 10,
  max_posts: 10,
  auto_generate: false,
  auto_generate_time: '07:00'
}

export default function SettingsPanel({ onSave }: SettingsPanelProps) {
  const [settings, setSettings] = useState<Settings>(DEFAULT_SETTINGS)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleChange = (key: keyof Settings, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      if (onSave) {
        await onSave(settings)
      }
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (error) {
      console.error('Failed to save settings:', error)
    } finally {
      setSaving(false)
    }
  }

  const handleReset = () => {
    setSettings(DEFAULT_SETTINGS)
  }

  const sections = [
    {
      id: 'cache',
      title: 'Cache Configuration',
      icon: <Database className="w-5 h-5" />,
      settings: [
        {
          label: 'Cache TTL (hours)',
          key: 'cache_ttl' as const,
          type: 'number',
          min: 1,
          max: 24,
          help: 'How long to cache API responses'
        }
      ]
    },
    {
      id: 'lookback',
      title: 'Data Lookback Windows',
      icon: <Clock className="w-5 h-5" />,
      settings: [
        {
          label: 'News Lookback (hours)',
          key: 'news_lookback_hours' as const,
          type: 'number',
          min: 1,
          max: 168,
          help: 'How far back to fetch news articles'
        },
        {
          label: 'Substack Lookback (hours)',
          key: 'substack_lookback_hours' as const,
          type: 'number',
          min: 24,
          max: 720,
          help: 'How far back to fetch newsletter posts (7 days = 168 hours)'
        }
      ]
    },
    {
      id: 'limits',
      title: 'Content Limits',
      icon: <Zap className="w-5 h-5" />,
      settings: [
        {
          label: 'Max Articles',
          key: 'max_articles' as const,
          type: 'number',
          min: 1,
          max: 50,
          help: 'Maximum articles to include per newsletter'
        },
        {
          label: 'Max Papers',
          key: 'max_papers' as const,
          type: 'number',
          min: 1,
          max: 50,
          help: 'Maximum research papers to include'
        },
        {
          label: 'Max Posts',
          key: 'max_posts' as const,
          type: 'number',
          min: 1,
          max: 50,
          help: 'Maximum newsletter posts to include'
        }
      ]
    },
    {
      id: 'schedule',
      title: 'Automatic Generation',
      icon: <SettingsIcon className="w-5 h-5" />,
      settings: [
        {
          label: 'Enable Auto-Generation',
          key: 'auto_generate' as const,
          type: 'checkbox',
          help: 'Automatically generate newsletter at specified time'
        },
        {
          label: 'Generation Time (UTC)',
          key: 'auto_generate_time' as const,
          type: 'time',
          disabled: !settings.auto_generate,
          help: 'What time to generate the newsletter daily'
        }
      ]
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  }

  return (
    <div className="space-y-6">
      {/* Success Message */}
      {success && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="p-4 bg-teal-500 bg-opacity-15 border border-teal-500 border-opacity-30 rounded-lg text-teal-400 flex items-center gap-2"
        >
          <Zap size={18} />
          Settings saved successfully!
        </motion.div>
      )}

      {/* Settings Sections */}
      <motion.div
        className="space-y-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {sections.map(section => (
          <motion.div
            key={section.id}
            variants={itemVariants}
            className="glass rounded-xl overflow-hidden border border-slate-700"
          >
            {/* Section Header */}
            <div className="p-6 border-b border-slate-700 flex items-center gap-3">
              <div className="text-cyan-400">{section.icon}</div>
              <h3 className="text-lg font-semibold text-white">{section.title}</h3>
            </div>

            {/* Section Settings */}
            <div className="p-6 space-y-6">
              {section.settings.map(setting => (
                <div key={String(setting.key)} className="space-y-2">
                  <label className="block text-sm font-medium text-slate-200">
                    {setting.label}
                  </label>

                  {setting.type === 'checkbox' ? (
                    <label className="flex items-center gap-3 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={settings[setting.key] as boolean}
                        onChange={e =>
                          handleChange(setting.key, e.target.checked)
                        }
                        className="w-5 h-5 rounded border-slate-500 bg-slate-800 cursor-pointer accent-cyan-500"
                      />
                      <span className="text-sm text-slate-400">
                        {setting.help}
                      </span>
                    </label>
                  ) : (
                    <>
                      <input
                        type={setting.type}
                        value={settings[setting.key]}
                        onChange={e =>
                          handleChange(
                            setting.key,
                            setting.type === 'number' ? parseInt(e.target.value) : e.target.value
                          )
                        }
                        disabled={setting.disabled}
                        min={setting.min}
                        max={setting.max}
                        className="w-full px-4 py-2 bg-slate-800 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                      <p className="text-xs text-slate-400">{setting.help}</p>
                    </>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="flex gap-3 pt-6 border-t border-slate-700"
      >
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-colors"
        >
          <Save size={20} />
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
        <button
          onClick={handleReset}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-3 border border-slate-600 hover:border-slate-500 text-slate-300 hover:text-white rounded-lg font-semibold transition-colors"
        >
          <RotateCcw size={20} />
          Reset
        </button>
      </motion.div>

      {/* Help Text */}
      <div className="p-4 bg-slate-800 bg-opacity-50 rounded-lg border border-slate-700">
        <p className="text-xs text-slate-400 space-y-2">
          <div>
            <strong className="text-slate-300">💡 Tip:</strong> Adjust the lookback windows to control content freshness. Shorter windows mean faster generation but less content.
          </div>
          <div>
            <strong className="text-slate-300">⚡ Note:</strong> Cache TTL of 6 hours provides ~70% cache hit rate on repeat runs.
          </div>
        </p>
      </div>
    </div>
  )
}
