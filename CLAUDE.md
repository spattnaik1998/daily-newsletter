# CLAUDE.md

## Project: Daily AI Newsletter Generator

### Overview

This repository builds a lightweight automated system that generates a **daily AI newsletter** summarizing the most important developments in artificial intelligence.

The system aggregates information from three major sources:

1. AI news websites (via Apify crawling)
2. Latest AI research papers from arXiv
3. AI newsletters from Substack

Each day, the system collects the latest information, summarizes the most important developments, and generates a **clean markdown newsletter** that the user can download and read.

This project prioritizes **simplicity and readability**.
No database or long-term storage should be implemented.

The pipeline should only generate a **single newsletter file per run**.

---

# Project Goals

The goal of the system is to automatically produce a **daily AI briefing** that includes:

* Major AI news stories
* Important research papers
* Key insights from AI newsletters
* Emerging themes in AI

The output should be concise and readable.

The final output must be a **markdown newsletter file**.

---

# Data Sources

## 1. AI News (Apify MCP)

Use Apify actors to crawl major AI-related news websites.

Suggested sources:

* TechCrunch AI
* VentureBeat AI
* MIT Technology Review
* The Verge AI
* other AI blogs

Capabilities required:

* search
* crawl articles
* extract article text
* extract metadata

Expected fields:

* title
* source
* author
* url
* publication_date
* article_text

Only fetch articles from the **last 24 hours**.

---

## 2. AI Research Papers (arXiv)

Fetch the most recent papers from the following arXiv categories:

* cs.AI
* cs.LG
* cs.CL
* cs.CV

Extract the following metadata:

* title
* authors
* abstract
* pdf_url
* submission_date

Limit results to **papers submitted in the last 24 hours**.

---

## 3. AI Newsletters (Substack)

Fetch recent posts from AI-focused Substack newsletters.

Examples include:

* Import AI
* Latent Space
* The Sequence
* Ben's Bites
* other AI Substack publications

Extract:

* title
* author
* summary
* url
* publish_date

Only retrieve the **most recent posts**.

---

# System Architecture

The system should be implemented using a **simple modular agent architecture**.

Each agent performs one task in the pipeline.

---

## Agents

### NewsCrawlerAgent

Responsibilities:

* trigger Apify crawling
* fetch AI news articles
* extract structured article metadata
* return results as JSON objects

---

### ArxivAgent

Responsibilities:

* query the arXiv API
* fetch newly submitted AI papers
* normalize metadata
* return structured paper objects

---

### SubstackAgent

Responsibilities:

* fetch recent Substack posts
* extract titles and summaries
* normalize metadata

---

### SummarizationAgent

Responsibilities:

* summarize news articles
* summarize research papers
* summarize newsletter insights

Summaries should be:

* concise
* informative
* easy to scan

Bullet points are preferred.

---

### NewsletterAgent

Responsibilities:

* combine all processed results
* generate the final newsletter

The newsletter must be written in **clean markdown format**.

---

# Repository Structure

The repository should follow this structure:

ai-daily-newsletter/

├── agents/
│   ├── news_agent.py
│   ├── arxiv_agent.py
│   ├── substack_agent.py
│   ├── summarization_agent.py
│   └── newsletter_agent.py
│
├── connectors/
│   ├── apify_connector.py
│   ├── arxiv_connector.py
│   └── substack_connector.py
│
├── pipeline/
│   └── daily_pipeline.py
│
├── utils/
│   └── text_processing.py
│
├── output/
│   └── newsletters/
│
├── config/
│   └── settings.py
│
├── main.py
└── requirements.txt

---

# Daily Pipeline

The daily pipeline should execute the following steps:

1. Run NewsCrawlerAgent
2. Run ArxivAgent
3. Run SubstackAgent
4. Summarize all collected content
5. Generate newsletter
6. Save newsletter to file

The pipeline must output a single markdown file.

---

# Newsletter Format

The final newsletter should look like this:

# Daily AI Newsletter

Date: YYYY-MM-DD

---

## Major AI News

* Summary of key AI news stories
* Include links to original articles

---

## Important Research Papers

* Paper title
* 1–2 sentence summary
* link to arXiv

---

## Insights from AI Newsletters

* Key ideas from Substack posts
* Short summaries

---

## Emerging Themes

Short analysis of recurring themes across sources.

Examples:

* agentic AI
* multimodal models
* robotics
* synthetic data

---

# Output File

The newsletter should be saved as:

output/newsletters/YYYY-MM-DD-ai-newsletter.md

Only generate the file for the current day.

No database or persistent storage should be implemented.

---

# Scheduling

The system should support running once per day.

Preferred scheduling options:

* cron
  or
* GitHub Actions

Suggested schedule:

Every day at **7:00 AM**.

---

# Requirements

Use Python 3.11+

Suggested libraries:

* requests
* pydantic
* beautifulsoup4
* arxiv
* markdown
* python-dateutil

Keep dependencies minimal.

---

# Development Guidelines

Follow these principles:

1. Keep code modular.
2. Each agent should have a single responsibility.
3. Ensure connectors are reusable.
4. Log pipeline progress clearly.
5. Handle API failures gracefully.
6. Prioritize clean and readable newsletter output.

---

# Future Extensions

Design the system so the following features can be added later:

* automatic email delivery of newsletter
* PDF export
* voice/audio briefing generation
* Telegram or Slack delivery
* weekly AI digest
* GitHub trending AI repositories