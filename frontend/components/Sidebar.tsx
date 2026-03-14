'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Menu, X, Home, Archive, Settings, LogOut, Zap, BookOpen } from 'lucide-react'
import { LucideIcon } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
}

type MenuItem =
  | { label: string; icon: LucideIcon; href: string; badge?: string | null }
  | { label: string; icon: LucideIcon; submenu: Array<{ label: string; href: string }> }

export default function Sidebar({ isOpen, onToggle }: SidebarProps) {
  const [expandedMenu, setExpandedMenu] = useState<string | null>(null)

  const menuItems: MenuItem[] = [
    {
      label: 'Dashboard',
      icon: Home,
      href: '/',
      badge: null,
    },
    {
      label: 'Archive',
      icon: Archive,
      href: '/archive',
      badge: null,
    },
    {
      label: 'Generation',
      icon: Zap,
      submenu: [
        { label: 'Manual Run', href: '/generate' },
        { label: 'Schedule', href: '/schedule' },
        { label: 'History', href: '/history' },
      ],
    },
    {
      label: 'Resources',
      icon: BookOpen,
      submenu: [
        { label: 'Sources', href: '/sources' },
        { label: 'Categories', href: '/categories' },
        { label: 'Themes', href: '/themes' },
      ],
    },
    {
      label: 'Settings',
      icon: Settings,
      href: '/settings',
      badge: null,
    },
  ]

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className={`hidden md:flex flex-col fixed left-0 top-0 h-screen bg-slate-900 border-r border-slate-700 transition-all duration-300 z-40 ${isOpen ? 'w-64' : 'w-20'}`}>
        {/* Logo */}
        <div className="h-20 flex items-center justify-center border-b border-slate-700">
          <div className="text-2xl font-bold font-display text-accent-cyan">✦</div>
        </div>

        {/* Menu */}
        <nav className="flex-1 overflow-y-auto py-8 px-4 space-y-2">
          {menuItems.map((item, idx) => (
            <div key={idx}>
              {'submenu' in item ? (
                <div>
                  <button
                    onClick={() => setExpandedMenu(expandedMenu === item.label ? null : item.label)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      expandedMenu === item.label
                        ? 'bg-slate-800 text-accent-cyan'
                        : 'text-slate-300 hover:bg-slate-800 hover:text-accent-cyan'
                    }`}
                  >
                    <item.icon size={20} />
                    {isOpen && <span className="text-sm font-medium flex-1 text-left">{item.label}</span>}
                  </button>
                  {isOpen && expandedMenu === item.label && (
                    <div className="pl-8 py-2 space-y-1 border-l border-slate-700">
                      {item.submenu.map((subitem, sidx) => (
                        <Link
                          key={sidx}
                          href={subitem.href}
                          className="block px-3 py-2 text-xs text-slate-400 hover:text-accent-cyan rounded-md transition-colors hover:bg-slate-800"
                        >
                          {subitem.label}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              ) : (
                <Link
                  href={item.href}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    item.badge
                      ? 'bg-accent-gold bg-opacity-10 text-accent-gold'
                      : 'text-slate-300 hover:bg-slate-800 hover:text-accent-cyan'
                  }`}
                >
                  <item.icon size={20} />
                  {isOpen && (
                    <div className="flex-1 flex items-center justify-between">
                      <span className="text-sm font-medium">{item.label}</span>
                      {item.badge && <span className="text-xs bg-accent-gold text-slate-900 px-2 py-0.5 rounded-full">{item.badge}</span>}
                    </div>
                  )}
                </Link>
              )}
            </div>
          ))}
        </nav>

        {/* Footer */}
        <div className="border-t border-slate-700 p-4 space-y-2">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-accent-cyan transition-colors text-sm font-medium">
            <LogOut size={18} />
            {isOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Mobile Sidebar Toggle (shown in Header) */}
      <style>{`
        @media (max-width: 768px) {
          aside {
            transform: ${isOpen ? 'translateX(0)' : 'translateX(-100%)'};
          }
        }
      `}</style>
    </>
  )
}
