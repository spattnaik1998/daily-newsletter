# How to Run the Daily AI Newsletter Generator

## Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API Key (already set in `.env`)

## Quick Start - Complete System (Backend + Frontend)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend API Server

Open a terminal and run:

```bash
python api_server.py
```

You should see:
```
Starting Daily AI Newsletter API Server...
Available at: http://localhost:8000
API docs: http://localhost:8000/docs
```

The API will be running on: **http://localhost:8000**

### Step 3: Start the Frontend (in a new terminal)

```bash
cd frontend
npm install
npm run dev
```

The frontend will be running on: **http://localhost:3000**

### Step 4: Open in Browser

Visit: **http://localhost:3000**

You should see the newsletter dashboard with:
- Latest newsletter
- Statistics (Articles, Papers, Posts, Themes)
- Newsletter archive
- Generation controls

---

## What You Can Do with the Frontend

1. **View Latest Newsletter** - See today's AI newsletter with all content
2. **Check Statistics** - View counts of articles, papers, and posts
3. **Browse Archive** - See previous newsletters
4. **Generate Newsletter** - Trigger manual generation
5. **Download** - Download newsletters as markdown

---

## Backend API Endpoints

The API provides these endpoints:

### Newsletter Management
- `GET /api/newsletter/latest` - Get latest newsletter
- `GET /api/newsletter/{date}` - Get newsletter by date (YYYY-MM-DD)
- `GET /api/newsletter/archive` - Get archive list with pagination
- `GET /api/newsletter/stats` - Get statistics
- `POST /api/newsletter/generate` - Trigger generation
- `GET /api/newsletter/{date}/download?format=md` - Download newsletter

### Settings
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings
- `GET /api/settings/sources` - Get sources configuration
- `PUT /api/settings/sources` - Update sources

### Health
- `GET /` - Health check
- `GET /api/health` - Detailed health check

Visit **http://localhost:8000/docs** for interactive API documentation.

---

## Individual Components (Standalone)

### Run Only Backend API
```bash
python api_server.py
```

### Run Only Frontend
```bash
cd frontend
npm install
npm run dev
```

### Run Only Newsletter Generation (CLI)
```bash
python main.py
```
This generates a newsletter and saves it to `output/newsletters/YYYY-MM-DD-ai-newsletter.md`

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable not set"
- Verify `.env` file exists with your API key
- The API key should start with `sk-ant-`

### Error: "Backend not responding" on frontend
- Make sure backend is running on port 8000
- Check: `http://localhost:8000` in browser

### Error: "Port already in use"
- Backend (8000): `lsof -i :8000` then `kill -9 <PID>`
- Frontend (3000): `lsof -i :3000` then `kill -9 <PID>`

### No newsletter in frontend
- Generate one: `python main.py`
- Or use the "Generate Now" button in the frontend
- Check `output/newsletters/` for generated files

---

## File Structure

```
Newsletter_Daily/
├── api_server.py                 # FastAPI backend
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (API key)
│
├── agents/                       # AI agents
│   ├── relevance_evaluator.py   # Claude-powered relevance check
│   ├── news_agent.py
│   ├── arxiv_agent.py
│   ├── substack_agent.py
│   ├── summarization_agent.py
│   └── newsletter_agent.py
│
├── connectors/                   # Data connectors
│   ├── apify_connector.py
│   ├── arxiv_connector.py
│   └── substack_connector.py
│
├── pipeline/                     # Orchestration
│   └── daily_pipeline.py
│
├── output/newsletters/           # Generated newsletters
│   └── 2026-03-14-ai-newsletter.md
│
├── config/                       # Configuration
│   └── settings.py
│
└── frontend/                     # Next.js frontend
    ├── app/
    ├── components/
    ├── lib/
    ├── package.json
    └── .env.local
```

---

## Features

✓ AI-powered relevance evaluation (Claude Opus 4.6)
✓ 2-3 day source age constraint
✓ Multi-source aggregation (News, Papers, Substack)
✓ Batch processing for efficiency
✓ Beautiful web interface
✓ REST API backend
✓ Newsletter archive
✓ Download support

---

## Notes

- Backend requires ANTHROPIC_API_KEY from `.env`
- Without API key: Falls back to basic filtering
- Generated newsletters saved to `output/newsletters/`
- Frontend has fallback demo data if backend unavailable
- All API calls are documented at `/docs` endpoint

Enjoy your AI newsletters!
