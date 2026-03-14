import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#0f1219',
          900: '#1a1f36',
          800: '#2d3345',
          700: '#3f4557',
          600: '#505a6f',
        },
        cream: {
          50: '#faf9f7',
          100: '#f8f7f3',
          200: '#f1ede6',
        },
        accent: {
          cyan: '#06b6d4',
          teal: '#14b8a6',
          gold: '#f59e0b',
          rose: '#f43f5e',
        },
      },
      fontFamily: {
        display: ['var(--font-playfair)', 'serif'],
        sans: ['var(--font-poppins)', 'sans-serif'],
        mono: ['var(--font-jetbrains)', 'monospace'],
      },
      spacing: {
        '13': '3.25rem',
        '15': '3.75rem',
      },
      borderRadius: {
        '3xl': '1.5rem',
      },
      boxShadow: {
        'sm-dark': '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
        'md-dark': '0 4px 6px -1px rgba(0, 0, 0, 0.4)',
        'lg-dark': '0 10px 15px -3px rgba(0, 0, 0, 0.5)',
        'xl-dark': '0 20px 25px -5px rgba(0, 0, 0, 0.6)',
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'pulse-subtle': 'pulseSubtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
      },
      backgroundImage: {
        'gradient-mesh': 'linear-gradient(135deg, #1a1f36 0%, #2d3345 50%, #1a1f36 100%)',
        'grain': 'url(\'data:image/svg+xml,%3Csvg width="100" height="100" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noise"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="4" /%3E%3C/filter%3E%3Crect width="100" height="100" fill="%231a1f36" filter="url(%23noise)" opacity="0.05"/%3E%3C/svg%3E\')',
      },
    },
  },
  plugins: [],
}

export default config
