"""
Main entry point for the Daily AI Newsletter Generator.

This script:
1. Initializes the pipeline
2. Runs the daily newsletter generation
3. Saves the output to output/newsletters/YYYY-MM-DD-ai-newsletter.md
4. Logs the results
"""

import sys
import logging
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from pipeline.daily_pipeline import DailyPipeline
from config.settings import OUTPUT_DIR, OUTPUT_FILENAME_TEMPLATE, DATE_FORMAT, LOG_LEVEL, LOG_FORMAT

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the newsletter generator."""
    try:
        logger.info("Initializing Daily AI Newsletter Generator")

        # Create pipeline
        pipeline = DailyPipeline()

        # Run pipeline
        newsletter, metadata = pipeline.run(hours=24)

        # Create output directory if it doesn't exist
        output_dir = Path(OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        today_date = datetime.now().strftime(DATE_FORMAT)
        filename = OUTPUT_FILENAME_TEMPLATE.format(date=today_date)
        output_path = output_dir / filename

        # Save newsletter
        logger.info(f"Saving newsletter to {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(newsletter)

        # Save morning brief if available
        if metadata.get("morning_brief"):
            morning_brief_filename = OUTPUT_FILENAME_TEMPLATE.format(
                date=today_date
            ).replace("ai-newsletter.md", "morning-brief.md")
            morning_brief_path = output_dir / morning_brief_filename
            logger.info(f"Saving morning brief to {morning_brief_path}")
            with open(morning_brief_path, "w", encoding="utf-8") as f:
                f.write(metadata["morning_brief"])
            logger.info(f"✓ Morning brief saved to: {morning_brief_path}")

        # Log summary
        pipeline.log_summary(metadata)

        logger.info(f"\n✓ Newsletter successfully generated!")
        logger.info(f"✓ Saved to: {output_path}")

        return 0

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
