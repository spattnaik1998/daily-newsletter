import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Daily AI Newsletter | Premium AI News Curation',
  description: 'Automated daily digest of AI breakthroughs, research papers, and industry insights.',
  keywords: ['AI', 'Newsletter', 'News Curation', 'Research', 'Automation'],
  authors: [{ name: 'Daily AI Newsletter' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://dailyainewsletter.com',
    title: 'Daily AI Newsletter',
    description: 'Premium AI News Curation Platform',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#1a1f36" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='50' font-size='50' fill='%2306b6d4' text-anchor='middle' dominant-baseline='central'>✦</text></svg>" />
      </head>
      <body className="relative">
        <div className="relative z-10">
          {children}
        </div>
      </body>
    </html>
  )
}
