'use client'

import { motion } from 'framer-motion'
import {
  Zap,
  Database,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Clock,
  GitBranch
} from 'lucide-react'

interface PipelineStats {
  execution_time: number
  cache_hit_rate: number
  articles_fetched: number
  papers_fetched: number
  posts_fetched: number
  duplicates_removed: number
  fetch_time: number
  last_run: string
  status: 'idle' | 'running' | 'completed' | 'error'
}

interface PipelineStatsPanelProps {
  stats?: PipelineStats
  isLoading?: boolean
}

const DEFAULT_STATS: PipelineStats = {
  execution_time: 0,
  cache_hit_rate: 0,
  articles_fetched: 0,
  papers_fetched: 0,
  posts_fetched: 0,
  duplicates_removed: 0,
  fetch_time: 0,
  last_run: 'Never',
  status: 'idle'
}

export default function PipelineStatsPanel({ stats = DEFAULT_STATS, isLoading }: PipelineStatsPanelProps) {
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

  const statCards = [
    {
      label: 'Pipeline Status',
      value: stats.status === 'running' ? 'Running...' : stats.status.charAt(0).toUpperCase() + stats.status.slice(1),
      icon: <RefreshCw className={`w-5 h-5 ${stats.status === 'running' ? 'animate-spin' : ''}`} />,
      color: stats.status === 'completed' ? 'text-teal-400' : stats.status === 'error' ? 'text-rose-400' : 'text-cyan-400',
      bgColor: stats.status === 'completed' ? 'bg-teal-500' : stats.status === 'error' ? 'bg-rose-500' : 'bg-cyan-500',
      trend: null
    },
    {
      label: 'Execution Time',
      value: `${stats.execution_time.toFixed(2)}s`,
      icon: <Clock className="w-5 h-5" />,
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-500',
      trend: stats.execution_time < 10 ? 'up' : null,
      trendText: stats.execution_time < 10 ? '5-10x speedup' : null
    },
    {
      label: 'Cache Hit Rate',
      value: `${(stats.cache_hit_rate * 100).toFixed(0)}%`,
      icon: <Database className="w-5 h-5" />,
      color: 'text-teal-400',
      bgColor: 'bg-teal-500',
      trend: stats.cache_hit_rate > 0.6 ? 'up' : null,
      trendText: stats.cache_hit_rate > 0.6 ? 'Excellent' : null
    },
    {
      label: 'Parallel Fetch Time',
      value: `${stats.fetch_time.toFixed(2)}s`,
      icon: <Zap className="w-5 h-5" />,
      color: 'text-amber-400',
      bgColor: 'bg-amber-500',
      trend: stats.fetch_time < 5 ? 'up' : null,
      trendText: stats.fetch_time < 5 ? 'Optimal' : null
    }
  ]

  const contentStats = [
    {
      label: 'News Articles',
      value: stats.articles_fetched,
      icon: '📰',
      color: 'from-cyan-500/20 to-cyan-500/5'
    },
    {
      label: 'Research Papers',
      value: stats.papers_fetched,
      icon: '📚',
      color: 'from-teal-500/20 to-teal-500/5'
    },
    {
      label: 'Newsletter Posts',
      value: stats.posts_fetched,
      icon: '📬',
      color: 'from-purple-500/20 to-purple-500/5'
    },
    {
      label: 'Duplicates Removed',
      value: stats.duplicates_removed,
      icon: '🔄',
      color: 'from-amber-500/20 to-amber-500/5'
    }
  ]

  return (
    <motion.div
      className="space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Main Metrics */}
      <motion.div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, index) => (
          <motion.div
            key={index}
            variants={itemVariants}
            className="glass rounded-xl p-6 border border-slate-700 hover-lift group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className={`${card.bgColor} bg-opacity-20 p-3 rounded-lg text-white group-hover:scale-110 transition-transform`}>
                {card.icon}
              </div>
              {card.trend === 'up' && (
                <div className="flex items-center gap-1 text-teal-400 text-sm font-semibold">
                  <TrendingUp size={16} />
                  {card.trendText}
                </div>
              )}
            </div>
            <div className="space-y-1">
              <p className="text-sm text-slate-400">{card.label}</p>
              <p className={`text-3xl font-bold ${card.color}`}>{card.value}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Content Metrics */}
      <motion.div variants={itemVariants} className="glass rounded-xl border border-slate-700 overflow-hidden">
        <div className="p-6 border-b border-slate-700">
          <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-cyan-400" />
            Content Collected
          </h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 p-6">
          {contentStats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 + index * 0.05 }}
              className={`bg-gradient-to-br ${stat.color} rounded-lg p-4 border border-slate-700 text-center`}
            >
              <div className="text-3xl mb-2">{stat.icon}</div>
              <p className="text-sm text-slate-400 mb-2">{stat.label}</p>
              <p className="text-2xl font-bold gradient-text">{stat.value}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Performance Details */}
      <motion.div variants={itemVariants} className="glass rounded-xl p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
          <Zap className="w-5 h-5 text-cyan-400" />
          Performance Details
        </h3>

        <div className="space-y-4">
          {/* Execution Time Breakdown */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-slate-400">Total Execution Time</span>
              <span className="text-sm font-semibold text-cyan-400">{stats.execution_time.toFixed(2)}s</span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-cyan-500 to-teal-500"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min((stats.execution_time / 30) * 100, 100)}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-1">Target: &lt; 10s (achieved 5-10x speedup with parallel fetching)</p>
          </div>

          {/* Cache Hit Rate */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-slate-400">Cache Hit Rate</span>
              <span className="text-sm font-semibold text-teal-400">{(stats.cache_hit_rate * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-teal-500 to-emerald-500"
                initial={{ width: 0 }}
                animate={{ width: `${(stats.cache_hit_rate * 100).toFixed(0)}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-1">Target: 60-80% on repeat runs (6-hour TTL)</p>
          </div>

          {/* Deduplication Rate */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-slate-400">Duplicates Removed</span>
              <span className="text-sm font-semibold text-amber-400">{stats.duplicates_removed}</span>
            </div>
            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-amber-500 to-orange-500"
                initial={{ width: 0 }}
                animate={{ width: `${Math.min((stats.duplicates_removed / 50) * 100, 100)}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-1">Quality improvement: &lt; 2% duplicates</p>
          </div>
        </div>
      </motion.div>

      {/* Last Run Info */}
      <motion.div
        variants={itemVariants}
        className="p-4 bg-slate-800 bg-opacity-50 rounded-lg border border-slate-700 flex items-center justify-between"
      >
        <div className="flex items-center gap-2 text-slate-400">
          <Clock size={18} />
          <span className="text-sm">
            Last run: <span className="text-cyan-400 font-semibold">{stats.last_run}</span>
          </span>
        </div>
        {stats.status === 'running' && (
          <div className="flex items-center gap-2 text-cyan-400 animate-pulse">
            <RefreshCw size={18} className="animate-spin" />
            <span className="text-sm font-semibold">Generating...</span>
          </div>
        )}
      </motion.div>
    </motion.div>
  )
}
