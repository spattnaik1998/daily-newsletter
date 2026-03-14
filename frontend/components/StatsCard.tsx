'use client'

import { Calendar, Newspaper, Book, Mail, TrendingUp, TrendingDown } from 'lucide-react'

interface StatsCardProps {
  label: string
  value: string | number
  icon: 'calendar' | 'newspaper' | 'book' | 'mail'
  trend?: 'up' | 'down'
  subtext?: string
}

const iconMap = {
  calendar: Calendar,
  newspaper: Newspaper,
  book: Book,
  mail: Mail,
}

export default function StatsCard({ label, value, icon, trend, subtext }: StatsCardProps) {
  const Icon = iconMap[icon]
  const TrendIcon = trend === 'up' ? TrendingUp : TrendingDown
  const trendColor = trend === 'up' ? 'text-accent-teal' : 'text-accent-rose'

  return (
    <div className="group relative bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 rounded-xl p-6 overflow-hidden transition-all duration-300 hover:border-accent-cyan hover:shadow-lg hover:shadow-cyan-500/10">
      {/* Background glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent-cyan/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <p className="text-slate-400 text-sm font-medium uppercase tracking-wide mb-2">{label}</p>
            <h3 className="text-3xl lg:text-4xl font-display font-bold text-cream-100">
              {value}
            </h3>
          </div>
          <div className="p-3 bg-slate-700 bg-opacity-50 rounded-lg group-hover:bg-accent-cyan group-hover:text-slate-950 transition-all duration-300">
            <Icon size={24} strokeWidth={1.5} />
          </div>
        </div>

        {/* Subtext and Trend */}
        <div className="flex items-center justify-between gap-2">
          {subtext && <p className="text-xs text-slate-500 font-light">{subtext}</p>}
          {trend && (
            <div className={`flex items-center gap-1 ${trendColor}`}>
              <TrendIcon size={14} />
              <span className="text-xs font-medium">{trend === 'up' ? '+12%' : '-8%'}</span>
            </div>
          )}
        </div>
      </div>

      {/* Bottom accent line */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-accent-cyan via-accent-teal to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    </div>
  )
}
