# Daily AI Newsletter - Complete Startup Guide

## 🎯 Quick Start (5 minutes)

### 1. Start the Backend API

```bash
# Terminal 1 - Backend
cd /path/to/Newsletter_Daily
python api/main.py

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

### 2. Start the Frontend

```bash
# Terminal 2 - Frontend
cd /path/to/Newsletter_Daily/frontend
npm run dev

# Expected output:
# ✓ Ready in 2.5s
# ➜  Local:   http://localhost:3000
```

### 3. Open in Browser

Visit: `http://localhost:3000`

---

## 📋 System Requirements

- **Node.js**: 18.0 or higher
- **Python**: 3.11 or higher
- **npm**: 9.0 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies + 100MB for newsletters
- **Anthropic API Key** (optional): For Claude Haiku intelligent summarization
  - Get one at: https://console.anthropic.com/
  - Set as environment variable: `ANTHROPIC_API_KEY=your-key`
  - Without it, the system falls back to text extraction

---

## 🔧 Full Setup Instructions

### Backend Setup

```bash
# Install system dependencies (if needed)
# macOS:
brew install python3

# Ubuntu/Debian:
sudo apt-get install python3.11 python3-pip

# Verify Python installation
python --version  # Should be 3.11+

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install Python dependencies
pip install fastapi uvicorn pydantic python-dotenv

# Or install from requirements
pip install -r requirements.txt

# Create output directory for newsletters
mkdir -p output/newsletters output/cache

# Optional: Set up environment variables
# For Claude Haiku intelligent summarization (optional):
export ANTHROPIC_API_KEY="your-anthropic-api-key"  # macOS/Linux
# or on Windows:
# set ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Frontend Setup

```bash
# Install Node.js (if not installed)
# Visit https://nodejs.org (18+ LTS recommended)

# Verify Node installation
node --version  # Should be 18.0+
npm --version   # Should be 9.0+

# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Verify build compiles
npm run type-check

# Optional: Run linter
npm run lint
```

---

## 🚀 Running the Application

### Development Mode

**Terminal 1 - API Backend:**
```bash
python api/main.py

# Server starts on http://localhost:8000
# API docs: http://localhost:8000/docs
# Reload on file changes: ✓ (auto-reload enabled)
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev

# Server starts on http://localhost:3000
# Reload on file changes: ✓ (auto-reload enabled)
```

**Terminal 3 - Monitor (optional):**
```bash
# Watch output/newsletters for generated files
watch -n 2 'ls -lh output/newsletters/ | tail -5'
```

### Production Mode

**Backend:**
```bash
# Build and run (no reload)
python api/main.py

# Or with Gunicorn (recommended)
pip install gunicorn
gunicorn api.main:app --bind 0.0.0.0:8000 --workers 4
```

**Frontend:**
```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start

# Or deploy to Vercel
npm run deploy  # (requires Vercel CLI)
```

---

## 🎮 Using the Dashboard

### Dashboard Tabs

1. **Latest** - View today's newsletter with tiered layout
2. **Performance** - Real-time pipeline metrics and statistics
3. **Profile** - Customize interests and expertise level
4. **Settings** - Configure cache, lookback windows, limits
5. **Archive** - Browse historical newsletters

### Generating a Newsletter

1. Click **"Generate Now"** button (top right)
2. Wait for generation to complete (~5-10 seconds)
3. View in **Latest** tab with tiered sections:
   - 📰 Lead Story
   - ⭐ Must Read Today
   - 📢 AI News Briefing
   - 🔬 Research Spotlight
   - 💬 Community Insights
   - 🎯 Emerging Themes

### Customizing Your Profile

1. Go to **Profile** tab
2. Update your name
3. Select expertise level
4. Choose interests (LLMs, AI Safety, etc.)
5. Set learning goal
6. Click **Save Profile**

### Adjusting Settings

1. Go to **Settings** tab
2. Configure:
   - **Cache TTL**: 1-24 hours (recommended: 6 hours)
   - **News Lookback**: 1-168 hours (default: 24)
   - **Substack Lookback**: 24-720 hours (default: 168 = 7 days)
   - **Content Limits**: 1-50 items per category
3. Click **Save Settings**

---

## 📊 API Endpoints Reference

### Newsletter Operations
```
POST   /api/newsletter/generate       Start generation
GET    /api/newsletter/status         Check status
GET    /api/newsletter/latest         Get today's
GET    /api/newsletter/{date}         Get specific date
GET    /api/newsletter/archive        List all (max 30)
```

### User Settings
```
GET    /api/user-profile              Get profile
POST   /api/user-profile              Update profile
POST   /api/settings                  Update settings
```

### Statistics
```
GET    /api/stats                     Get pipeline stats
GET    /api/morning-brief/latest      Get morning brief
GET    /health                        Health check
```

### Documentation
```
GET    /docs                          Swagger UI
GET    /redoc                         ReDoc UI
GET    /                              API info
```

**Example API Call:**
```bash
# Generate newsletter
curl -X POST http://localhost:8000/api/newsletter/generate

# Check status
curl http://localhost:8000/api/newsletter/status

# Get latest newsletter
curl http://localhost:8000/api/newsletter/latest | jq '.data.content'
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

```bash
# Check what's using the port
lsof -i :3000    # Frontend
lsof -i :8000    # Backend

# Kill the process
kill -9 <PID>

# Or use different ports
npm run dev -- -p 3001           # Frontend
python api/main.py --port 8001   # Backend
```

### Issue: "Module not found" Error

```bash
# Frontend
cd frontend
rm -rf node_modules .next
npm install
npm run build

# Backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: CORS Errors

```
Error: Access to XMLHttpRequest blocked by CORS policy
```

**Solution**: Ensure backend is running on `http://localhost:8000`

Edit `api/main.py` if different port:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    # Add your frontend URL here
)
```

### Issue: Newsletter Generation Timeout

- Check Python process is running: `ps aux | grep python`
- Check `/output/newsletters/` directory exists
- Check disk space: `df -h`
- View logs for errors

### Issue: API Documentation Not Loading

Visit `http://localhost:8000/docs` directly (Swagger UI)

---

## 📈 Performance Tips

### Frontend Optimization
- Clear cache: `rm -rf .next && npm run build`
- Monitor bundle size: `npm run build -- --debug`
- Enable HTTP/2 in production

### Backend Optimization
- Verify cache is working: Check logs for "Using cached data"
- Monitor memory: `ps aux | grep python`
- Use GunicornWorkers: `gunicorn ... --workers 4`

### Overall System
- Close unnecessary applications
- Allocate at least 2GB RAM to VMs
- Use SSD for better I/O performance

---

## 📦 File Locations

```
Newsletter_Daily/
├── api/
│   ├── main.py              ← FastAPI application
│   └── requirements.txt      ← API dependencies
├── frontend/
│   ├── app/
│   │   ├── page.tsx         ← Main dashboard
│   │   └── globals.css      ← Styling & animations
│   ├── components/          ← React components
│   ├── package.json
│   └── node_modules/        ← npm dependencies
├── agents/                  ← Newsletter generation agents
├── connectors/              ← Data source connectors
├── pipeline/
│   └── daily_pipeline.py    ← Orchestration
├── config/
│   └── settings.py          ← Configuration
├── output/
│   ├── newsletters/         ← Generated files
│   └── cache/               ← 6-hour cache
├── requirements.txt         ← Python dependencies
├── STARTUP_GUIDE.md         ← This file
└── FRONTEND_README.md       ← Frontend documentation
```

---

## ✅ Verification Checklist

Before considering setup complete:

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] Dashboard loads without errors
- [ ] Can generate a newsletter (button doesn't throw error)
- [ ] Stats tab shows "idle" status
- [ ] Profile tab saves without errors
- [ ] Settings tab accepts input changes

---

## 🔄 Daily Workflow

### Morning
1. Open dashboard at `http://localhost:3000`
2. Click **"Generate Now"** button
3. Wait for generation to complete (~5-10 seconds)
4. Review in **Latest** tab

### Throughout the Day
- Check **Performance** tab for metrics
- Adjust interests in **Profile** tab
- Browse **Archive** for past newsletters

### Evening
- Review **Settings** for optimization
- Check cache hit rates
- Plan next day's interests

---

## 🤝 Getting Help

### Check Logs
```bash
# Backend logs (current terminal)
# Shows: INFO, ERROR, WARNING messages

# Frontend logs (browser console)
# F12 → Console tab → Check for errors
```

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Code References
- Backend: `api/main.py` - Detailed docstrings
- Frontend: `frontend/components/` - TypeScript interfaces
- Config: `config/settings.py` - All configurable options

---

## 🎓 Learning Resources

### Components Deep Dive
```bash
# Frontend architecture
frontend/
├── app/page.tsx              # Main layout
├── components/
│   ├── TieredNewsletterViewer.tsx   # Newsletter display
│   ├── PipelineStatsPanel.tsx        # Metrics
│   ├── UserProfilePanel.tsx          # Settings
│   └── SettingsPanel.tsx             # Config
└── lib/
    ├── api.ts                # API client
    └── hooks/
        └── useNewsletter.ts  # Custom hook
```

### API Flow
1. Frontend calls `POST /api/newsletter/generate`
2. Backend starts background task
3. Frontend polls `GET /api/newsletter/status`
4. When complete, fetches `GET /api/newsletter/latest`
5. Renders in tiered format

---

## 🚀 Next Steps

### Week 1
- Generate daily newsletters
- Customize profile with interests
- Explore different settings
- Monitor performance metrics

### Week 2+
- Set up automatic daily generation (in settings)
- Integrate with email (custom extension)
- Export newsletters to PDF
- Share notable articles with team

---

## 📞 Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Review logs for error messages
3. Check GitHub issues: `https://github.com/spattnaik1998/daily-newsletter`
4. Read documentation files in project root

---

**You're all set! 🚀 Happy news curation!**
