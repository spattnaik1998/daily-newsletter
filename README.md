# Daily AI Newsletter Generator

An automated system that generates a **daily AI newsletter** summarizing the most important developments in artificial intelligence.

## Overview

This project aggregates information from three major sources:

1. **AI News** - via Apify crawling (TechCrunch, VentureBeat, The Verge, etc.)
2. **AI Research Papers** - from arXiv (cs.AI, cs.LG, cs.CL, cs.CV categories)
3. **AI Newsletters** - from Substack (Import AI, Latent Space, The Sequence, Ben's Bites, etc.)

The system generates a **clean, readable markdown newsletter** each day at 7:00 AM UTC.

## Frontend

A sophisticated, professional web interface built with **Next.js 14** and **React 18** provides:

- **Dashboard**: Latest newsletter display with real-time stats
- **Archive**: Searchable history of all past newsletters
- **Responsive Design**: Mobile-friendly interface with refined aesthetics
- **Markdown Viewer**: Beautiful rendering of newsletter content with syntax highlighting
- **Download Options**: Export newsletters as Markdown, Text, or PDF
- **Admin Controls**: Manual generation trigger, schedule management, source configuration

The frontend features a **refined minimalist design** with:
- Elegant typography (Playfair Display + Poppins + JetBrains Mono)
- Deep slate backgrounds with cyan accents
- Smooth animations and micro-interactions
- Professional B2B SaaS aesthetic

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## Project Structure

```
Newsletter_Daily/
├── backend/                          # Python backend
│   ├── agents/                       # Agent modules
│   │   ├── news_agent.py            # News crawler agent
│   │   ├── arxiv_agent.py           # arXiv research agent
│   │   ├── substack_agent.py        # Substack newsletter agent
│   │   ├── summarization_agent.py   # Content summarization agent
│   │   └── newsletter_agent.py      # Newsletter generation agent
│   │
│   ├── connectors/                  # External data source connectors
│   │   ├── apify_connector.py       # Apify API connector
│   │   ├── arxiv_connector.py       # arXiv API connector
│   │   └── substack_connector.py    # Substack content extractor
│   │
│   ├── pipeline/                    # Pipeline orchestration
│   │   └── daily_pipeline.py        # Main pipeline coordinator
│   │
│   ├── utils/                       # Helper utilities
│   │   └── text_processing.py       # Text processing functions
│   │
│   ├── config/                      # Configuration
│   │   └── settings.py              # Configuration settings
│   │
│   ├── output/                      # Output directory
│   │   └── newsletters/             # Generated newsletters
│   │
│   ├── main.py                      # Entry point script
│   └── requirements.txt             # Python dependencies
│
├── frontend/                         # React/Next.js frontend
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx              # Root layout
│   │   ├── page.tsx                # Dashboard page
│   │   └── globals.css             # Global styles
│   │
│   ├── components/                 # React components
│   │   ├── Sidebar.tsx             # Navigation sidebar
│   │   ├── Header.tsx              # Top header
│   │   ├── StatsCard.tsx           # Statistics cards
│   │   ├── NewsletterViewer.tsx    # Newsletter display
│   │   └── Archive.tsx             # Archive view
│   │
│   ├── lib/                        # Utilities and hooks
│   │   ├── api.ts                  # API client
│   │   ├── utils.ts                # Helper functions
│   │   └── hooks/                  # React hooks
│   │
│   ├── public/                     # Static assets
│   ├── package.json                # npm dependencies
│   ├── tsconfig.json               # TypeScript config
│   ├── tailwind.config.ts          # Tailwind CSS config
│   └── README.md                   # Frontend documentation
│
├── CLAUDE.md                        # Project specification
├── README.md                        # This file
└── SETUP.md                         # Repository setup guide
```

## Full Stack Setup

### Backend (Python)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure settings:**
   Edit `config/settings.py` to customize sources and API settings.

3. **Run the pipeline:**
   ```bash
   python main.py
   ```

### Frontend (Next.js)

1. **Install Node dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env.local
   ```
   Update `NEXT_PUBLIC_API_URL` to point to your backend.

3. **Run development server:**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000)

### Full Stack Development

Run both services in parallel:

**Terminal 1 - Backend:**
```bash
# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access the application at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000 (when API service is added)

## Configuration

Edit `config/settings.py` to customize:

- **Time window** - Number of hours to look back (default: 24)
- **Output directory** - Where newsletters are saved
- **API endpoints** - Configure news sources and API timeouts
- **Summarization settings** - Max summary length and style

## Usage

### Run the Pipeline Once

```bash
python main.py
```

This will:
1. Fetch news articles from AI news websites
2. Fetch recent papers from arXiv
3. Fetch posts from AI Substack newsletters
4. Summarize all content
5. Generate a markdown newsletter
6. Save it to `output/newsletters/YYYY-MM-DD-ai-newsletter.md`

### Schedule Daily Execution

#### Using cron (Linux/Mac):

```bash
0 7 * * * cd /path/to/Newsletter_Daily && python main.py
```

#### Using GitHub Actions:

Create `.github/workflows/daily-newsletter.yml`:

```yaml
name: Daily Newsletter

on:
  schedule:
    - cron: '0 7 * * *'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python main.py
      - run: |
          git config user.email "bot@example.com"
          git config user.name "Newsletter Bot"
          git add .
          git commit -m "Daily newsletter - $(date +%Y-%m-%d)" || true
          git push
```

## Newsletter Output Format

The generated newsletter follows this structure:

```markdown
# Daily AI Newsletter

**Date:** YYYY-MM-DD

---

## Major AI News
* Article title with link
* Summary and source

---

## Important Research Papers
* Paper title
* 1-2 sentence summary
* Link to arXiv

---

## Insights from AI Newsletters
* Key ideas from Substack posts
* Links to full posts

---

## Emerging Themes
* Agentic AI
* Multimodal Models
* Robotics
* etc.

---
```

## Project Structure Details

### Agents

Each agent has a single responsibility:

- **NewsCrawlerAgent** - Crawls AI news websites and extracts articles
- **ArxivAgent** - Fetches recent papers from arXiv categories
- **SubstackAgent** - Extracts posts from AI newsletters
- **SummarizationAgent** - Creates concise summaries and bullet points
- **NewsletterAgent** - Assembles the final markdown newsletter

### Connectors

Connectors handle external API interactions:

- **ApifyConnector** - Manages Apify actor crawling
- **ArxivConnector** - Queries the arXiv API
- **SubstackConnector** - Fetches Substack content via RSS or web scraping

### Pipeline

The `DailyPipeline` orchestrates all agents in the correct order and logs progress.

## Dependencies

- **requests** - HTTP client for API calls
- **pydantic** - Data validation
- **beautifulsoup4** - HTML parsing
- **feedparser** - RSS feed parsing
- **python-dateutil** - Date/time utilities
- **markdown** - Markdown generation
- **arxiv** - arXiv API client

## Future Extensions

The system is designed to support these extensions:

- Automatic email delivery
- PDF export
- Voice/audio briefing generation
- Telegram or Slack delivery
- Weekly AI digest
- GitHub trending AI repositories

## Development Guidelines

1. **Keep code modular** - Each agent has a single responsibility
2. **Use proper logging** - Track pipeline progress with logging
3. **Handle errors gracefully** - Graceful fallbacks for API failures
4. **Maintain clean output** - Newsletter markdown should be professional
5. **Document code** - Use docstrings for all modules and functions

## Troubleshooting

### No articles/papers/posts fetched?

- Check internet connectivity
- Verify API endpoints are accessible
- Review logs for error messages
- Some sources may require authentication (configure in settings.py)

### Newsletter generation fails?

- Ensure output directory exists
- Check file permissions
- Review error logs

### Missing dependencies?

```bash
pip install -r requirements.txt --upgrade
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues or questions:
- Check existing GitHub issues
- Review the CLAUDE.md specification
- Check agent docstrings for implementation details
