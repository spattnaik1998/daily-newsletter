# API Key Setup Guide

## Overview

The **Daily AI Newsletter Generator** now includes a **robust relevance evaluation system** powered by Claude (Anthropic's LLM). This feature uses the Anthropic API to:

1. **Evaluate source relevance** - Determine if news, papers, and posts are truly AI-related
2. **Enforce date constraints** - Ensure sources are no more than **2-3 days old**
3. **Filter low-quality content** - Remove off-topic or low-value sources

---

## API Key Requirement

### **You NEED an Anthropic API Key**

To use the relevance evaluation feature, you must:

1. **Get an API Key**:
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Sign up or log in
   - Navigate to **API Keys** section
   - Create a new API key

2. **Set the Environment Variable**:

   **On Windows (PowerShell)**:
   ```powershell
   $env:ANTHROPIC_API_KEY = "your-api-key-here"
   ```

   **On Windows (Command Prompt)**:
   ```cmd
   set ANTHROPIC_API_KEY=your-api-key-here
   ```

   **On Linux/macOS**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Verify Setup**:
   ```python
   import os
   api_key = os.environ.get("ANTHROPIC_API_KEY")
   print(f"API Key loaded: {bool(api_key)}")
   ```

---

## Model Used

The system uses **Claude Opus 4.6**, which provides:

- **High accuracy** for relevance evaluation
- **Cost-effective** for batch processing
- **Fast inference** for pipeline execution

**Pricing** (approximate):
- Input: $5 per 1M tokens
- Output: $25 per 1M tokens
- Typical evaluation: $0.01-0.05 per 10 sources

---

## Fallback Behavior

If the API key is **not set** or evaluation fails:

1. The pipeline will **log a warning**
2. **Fall back to basic filtering** (date + keyword-based only)
3. **Continue execution** with reduced quality

No API key = no failure, just reduced relevance filtering.

---

## Configuration

### Optional Settings (in `config/settings.py`):

```python
# Enable/disable relevance evaluation
ENABLE_RELEVANCE_EVALUATION = True  # Set to False to disable

# Maximum source age
MAX_SOURCE_AGE_DAYS = 3  # 2-3 days
```

### Disable Relevance Evaluation

If you want to **skip API calls entirely**:

```python
from pipeline.daily_pipeline import DailyPipeline

# Initialize without relevance evaluation
pipeline = DailyPipeline(use_relevance_eval=False)
```

---

## What Gets Evaluated

### News Articles
- **Relevance Check**: Is it about AI, ML, LLMs, neural networks, AI applications, etc.?
- **Date Check**: Published within 2-3 days

### Research Papers
- **Relevance Check**: Are authors researching AI topics in abstract/title?
- **Date Check**: Submitted within 2-3 days

### Substack Posts
- **Relevance Check**: Does the post discuss AI/ML content?
- **Date Check**: Published within 2-3 days

---

## Evaluation Criteria

Sources are filtered out if they are:

1. **Off-topic**:
   - Sports, politics, weather, entertainment
   - Unrelated to AI/ML/LLMs

2. **Low-quality**:
   - Duplicate content
   - Promotional without technical merit
   - Click-bait

3. **Too old**:
   - More than 3 days old

4. **Unverifiable**:
   - Missing dates or titles
   - Broken metadata

---

## Example Usage

### Basic Setup

```bash
# 1. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run pipeline
python main.py
```

### Checking Logs

```bash
# You'll see logs like:
# ✓ Relevance evaluator initialized with Claude API
# ✓ Date filter: 45/80 sources within 2-3 days
# ✓ Relevance evaluation: 32 relevant sources
# ✓ Filtered out: 13 low-relevance sources
```

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY environment variable not set"

**Solution**: Set your API key before running:

```bash
export ANTHROPIC_API_KEY="your-key-here"
python main.py
```

### Error: "Invalid API key"

**Solution**:
- Check that your key starts with `sk-ant-`
- Verify it's not truncated
- Check Anthropic Console for key status

### Error: "Authentication failed"

**Solution**:
- Your API key may have expired or been revoked
- Create a new key in the Anthropic Console

### Slow evaluation / timeout

**Solution**:
- Network issues (normal, SDK retries automatically)
- API rate limits (wait a few minutes)
- Large batch size (the system batches 10 sources at a time automatically)

---

## Cost Estimation

For a typical daily run with:
- 50 news articles
- 20 research papers
- 15 Substack posts

**Estimated cost**: ~$0.02-0.05 per day

**Per month (30 days)**: ~$0.60-1.50

---

## Privacy & Security

- **No data storage**: Evaluations are temporary, not stored
- **No API key in logs**: API keys are never logged
- **Secure transmission**: HTTPS only (SDK handles this)
- **Batch processing**: Multiple sources evaluated in single request

---

## Advanced: Custom Evaluator

To implement a **custom evaluator** (e.g., using OpenAI):

```python
from agents.relevance_evaluator import RelevanceEvaluator

class CustomEvaluator(RelevanceEvaluator):
    def _evaluate_batch_relevance(self, sources, source_type):
        # Your custom logic here
        pass
```

Then pass it to the pipeline:

```python
pipeline = DailyPipeline()
pipeline.relevance_evaluator = CustomEvaluator()
```

---

## Support

For issues:
1. Check [Anthropic Console](https://console.anthropic.com/)
2. Review this guide
3. Check logs for error messages
4. Report issues on GitHub

---

## Next Steps

1. ✅ Get your API key from [console.anthropic.com](https://console.anthropic.com/)
2. ✅ Set `ANTHROPIC_API_KEY` environment variable
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Run: `python main.py`
5. ✅ Check logs for evaluation results

Happy newsletter generating! 🚀
