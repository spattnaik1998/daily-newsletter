'use client'

import { useState } from 'react'
import { Menu, Bell, Settings, BarChart3, Archive, Zap } from 'lucide-react'

interface HeaderProps {
  onMenuClick: () => void
  activeView: 'latest' | 'archive' | 'stats'
  onViewChange: (view: 'latest' | 'archive' | 'stats') => void
}

export default function Header({ onMenuClick, activeView, onViewChange }: HeaderProps) {
  const [showNotifications, setShowNotifications] = useState(false)

  const views = [
    { id: 'latest', label: 'Latest', icon: Zap },
    { id: 'stats', label: 'Stats', icon: BarChart3 },
    { id: 'archive', label: 'Archive', icon: Archive },
  ]

  return (
    <header className="sticky top-0 z-30 backdrop-blur-md bg-slate-950 bg-opacity-80 border-b border-slate-700 border-opacity-50">
      <div className="flex items-center justify-between px-6 lg:px-12 h-20">
        {/* Left: Menu Toggle (Mobile) + Logo */}
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-accent-cyan"
          >
            <Menu size={24} />
          </button>
          <div className="hidden sm:flex items-center gap-2">
            <div className="text-xl font-bold text-accent-cyan">✦</div>
            <span className="font-display text-lg font-semibold text-cream-100">Daily AI</span>
          </div>
        </div>

        {/* Center: View Tabs */}
        <div className="hidden md:flex items-center gap-1 bg-slate-800 rounded-lg p-1">
          {views.map((view) => {
            const Icon = view.icon
            return (
              <button
                key={view.id}
                onClick={() => onViewChange(view.id as any)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors text-sm font-medium ${
                  activeView === view.id
                    ? 'bg-accent-cyan text-slate-950'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Icon size={16} />
                {view.label}
              </button>
            )
          })}
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-3">
          {/* Notification Bell */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-accent-cyan"
            >
              <Bell size={20} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-accent-rose rounded-full"></span>
            </button>

            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 bg-slate-800 border border-slate-700 rounded-lg shadow-lg overflow-hidden">
                <div className="p-4 border-b border-slate-700">
                  <h3 className="font-semibold text-cream-100">Notifications</h3>
                </div>
                <div className="max-h-96 overflow-y-auto">
                  <div className="p-4 hover:bg-slate-700 transition-colors cursor-pointer">
                    <p className="text-sm text-cream-100 font-medium">Newsletter Generated</p>
                    <p className="text-xs text-slate-400 mt-1">Today at 7:00 AM</p>
                  </div>
                  <div className="p-4 border-t border-slate-700 hover:bg-slate-700 transition-colors cursor-pointer">
                    <p className="text-sm text-cream-100 font-medium">New Research Papers Available</p>
                    <p className="text-xs text-slate-400 mt-1">3 papers from arXiv</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Settings */}
          <button className="p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-accent-cyan">
            <Settings size={20} />
          </button>

          {/* Generate Button */}
          <button className="hidden sm:flex items-center gap-2 px-4 py-2 bg-accent-cyan text-slate-950 rounded-lg font-medium hover:bg-accent-teal transition-colors">
            <Zap size={16} />
            Generate
          </button>
        </div>
      </div>

      {/* Mobile View Tabs */}
      <div className="md:hidden flex items-center gap-1 px-6 pb-4 overflow-x-auto">
        {views.map((view) => {
          const Icon = view.icon
          return (
            <button
              key={view.id}
              onClick={() => onViewChange(view.id as any)}
              className={`flex items-center gap-2 px-3 py-2 rounded-md transition-colors text-xs font-medium whitespace-nowrap ${
                activeView === view.id
                  ? 'bg-accent-cyan text-slate-950'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon size={14} />
              {view.label}
            </button>
          )
        })}
      </div>
    </header>
  )
}
