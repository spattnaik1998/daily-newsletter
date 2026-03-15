# Daily AI Newsletter - Frontend & API

A premium, production-grade web application dashboard for the Daily AI Newsletter Generator with intelligent AI content curation.

## 🎨 Design Philosophy

**Luxury Data Dashboard Aesthetic** - Refined, professional interface with sophisticated typography, subtle gradients, and elegant micro-interactions inspired by premium financial dashboards and data visualization tools.

### Visual Design Highlights
- **Color Palette**: Deep slate (slate-950) backgrounds with cyan/teal accents and emerald highlights
- **Typography**: Playfair Display (serif headlines) + Space Grotesk (sans-serif body) + JetBrains Mono (code)
- **Effects**: Glass morphism, gradient accents, staggered animations, hover effects
- **Accessibility**: WCAG 2.1 AA compliant, keyboard navigation, focus indicators

## 🚀 Features

### 1. **Tiered Newsletter Display**
   - **Lead Story**: Most important AI development highlighted
   - **Must Read Today**: Top 3 items with impact scoring
   - **AI News Briefing**: Full article list ranked by relevance
   - **Research Spotlight**: Featured paper with Code Available badges
   - **Community Insights**: Key perspectives from 12 Substack newsletters
   - **Emerging Themes**: Auto-detected patterns and trends

### 2. **Real-Time Performance Metrics**
   - Pipeline execution time (showing 5-10x speedup)
   - Cache hit rate monitoring (60-80% on repeat runs)
   - Content source breakdown (17 news + 12 newsletters)
   - Deduplication statistics
   - Progress tracking with live updates

### 3. **User Profile Configuration**
   - Name, interests, expertise level
   - Learning goals for content filtering
   - Interest-based content prioritization
   - Expertise-level technical depth adjustment

### 4. **Advanced Settings Panel**
   - Cache TTL configuration (1-24 hours)
   - Data lookback windows (news, Substack, arXiv)
   - Content limits (articles, papers, posts)
   - Auto-generation scheduling
   - Source management

### 5. **Newsletter Archive**
   - Browse past newsletters by date
   - Search and filter capabilities
   - File size and metadata display
   - Download previous editions

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Production-grade animations
- **React Markdown** - Markdown rendering with custom components
- **Lucide React** - Beautiful icon library

### Backend API
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **CORS Middleware** - Cross-origin requests
- **Background Tasks** - Async generation tasks

### Design Tools
- Google Fonts (Playfair Display, Space Grotesk, JetBrains Mono)
- CSS Grid & Flexbox for layouts
- CSS Animations & Transitions
- Glass morphism effects

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- pip/poetry

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm start
```

Frontend runs on `http://localhost:3000`

### Backend API Setup

```bash
# Install Python dependencies
pip install fastapi uvicorn python-dotenv

# Run the API server
python api/main.py

# Or with Uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API runs on `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

## 🔌 API Endpoints

### Newsletter Management
- `POST /api/newsletter/generate` - Start newsletter generation
- `GET /api/newsletter/status` - Check generation status
- `GET /api/newsletter/latest` - Retrieve latest newsletter
- `GET /api/newsletter/{date}` - Get newsletter for specific date
- `GET /api/newsletter/archive` - List archived newsletters

### Pipeline Management
- `GET /api/stats` - Get real-time pipeline statistics
- `GET /health` - Health check endpoint

### User Configuration
- `GET /api/user-profile` - Get user profile
- `POST /api/user-profile` - Update user profile
- `POST /api/settings` - Update pipeline settings

### Content
- `GET /api/morning-brief/latest` - Get morning brief
- `GET /api/` - API information

## 🎯 Component Architecture

### Page Components
- **`app/page.tsx`** - Main dashboard with tab-based navigation
  - View switching (Latest, Stats, Profile, Settings, Archive)
  - Newsletter generation control
  - Real-time API integration

### Feature Components
- **`TieredNewsletterViewer`** - Tiered newsletter display with collapsible sections
- **`PipelineStatsPanel`** - Real-time performance metrics and charts
- **`UserProfilePanel`** - User preferences and interest configuration
- **`SettingsPanel`** - Advanced configuration options
- **`Archive`** - Newsletter history browser
- **`Sidebar`** - Navigation sidebar
- **`Header`** - Top navigation and controls

### Utilities
- **`lib/hooks/`** - Custom React hooks for API integration
- **`lib/api.ts`** - API client functions
- **`styles/globals.css`** - Global styles and animations

## 🎨 Styling System

### CSS Variables (globals.css)
```css
--font-playfair: 'Playfair Display', serif
--font-poppins: 'Poppins', sans-serif
--font-jetbrains: 'JetBrains Mono', monospace

--color-slate-950: #0f1219
--color-cyan: #06b6d4
--color-teal: #14b8a6
--color-gold: #f59e0b
--color-rose: #f43f5e
```

### Animation Library
- `fadeIn` - Fade in from below
- `slideInLeft/Right/Up` - Directional slides
- `scaleIn` - Scale from 0.95 to 1
- `pulse-glow` - Pulsing glow effect
- `float` - Gentle floating motion
- `shimmer` - Loading skeleton animation

### Glass Morphism
```css
.glass {
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(148, 163, 184, 0.1);
}
```

## 🚀 Production Deployment

### Frontend (Vercel Recommended)
```bash
npm run build
# Deploy to Vercel (automatic on git push)
```

### Backend (Docker)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
```

## 📊 Performance Optimizations

1. **Image Optimization** - Next.js Image component
2. **Code Splitting** - Route-based lazy loading
3. **Memoization** - React.memo for expensive components
4. **Caching** - 6-hour API response cache
5. **Parallel Processing** - ThreadPoolExecutor for data fetching
6. **Animations** - CSS-based for 60fps performance

## 🔐 Security

- CORS configured for localhost development
- Environment variable management (.env.local)
- API error handling and validation
- Input sanitization with React Markdown
- No sensitive data in localStorage

## 📱 Responsive Design

- Mobile-first approach
- Tailwind breakpoints (sm, md, lg, xl)
- Touch-friendly interactions
- Adaptive navigation (sidebar collapse on mobile)
- Optimized for screens 320px to 2560px

## 🧪 Testing

```bash
# Run type checking
npm run type-check

# Lint code
npm run lint

# Run tests (when added)
npm test
```

## 📚 File Structure

```
frontend/
├── app/
│   ├── layout.tsx         # Root layout with metadata
│   ├── page.tsx           # Main dashboard
│   ├── globals.css        # Global styles & animations
│   └── favicon.ico
├── components/
│   ├── TieredNewsletterViewer.tsx
│   ├── PipelineStatsPanel.tsx
│   ├── UserProfilePanel.tsx
│   ├── SettingsPanel.tsx
│   ├── Archive.tsx
│   ├── Sidebar.tsx
│   └── Header.tsx
├── lib/
│   ├── hooks/
│   │   └── useNewsletter.ts
│   └── api.ts
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── postcss.config.js

api/
├── main.py                # FastAPI application
└── requirements.txt
```

## 🐛 Troubleshooting

### Frontend issues
- Clear `.next` cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node version: `node --version` (should be 18+)

### Backend issues
- Verify Python version: `python --version` (should be 3.11+)
- Check port availability: `lsof -i :8000`
- Enable CORS if frontend on different port
- Check output/newsletters directory exists

### API connection errors
- Verify both services running (frontend:3000, backend:8000)
- Check CORS configuration in `api/main.py`
- Inspect network tab in browser DevTools

## 📖 Documentation

- [Backend API Docs](./api/main.py) - Detailed endpoint documentation
- [Frontend Component Guide](#component-architecture) - Component usage
- [Design System](./frontend/app/globals.css) - Color, typography, animations
- [Deployment Guide](#production-deployment) - Hosting instructions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT - See LICENSE file for details

## 🙏 Acknowledgments

- Designed following frontend-design principles
- Built with [Next.js](https://nextjs.org/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Animated with [Framer Motion](https://www.framer.com/motion/)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)

---

**Created with ❤️ for AI enthusiasts**
