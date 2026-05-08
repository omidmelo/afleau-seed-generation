#!/usr/bin/env python3
"""
Main execution script for data generation across multiple categories
"""

import asyncio
import logging
import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.base_client import LLMError
from lib.bedrock_client import BedrockClient
from lib.generator import DataGenerator
from lib.config import config
from lib.registry import prompt_registry

# Ensure logs directory exists
Path('logs').mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/health_wellbeing_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def create_client(model_id: str):
    """
    Factory for creating the LLM client from a model_id.

    Currently all supported models are served via AWS Bedrock, including:
      - amazon.nova-micro-v1:0
      - us.anthropic.claude-sonnet-4-6

    AWS credentials must be configured in the environment.
    """
    provider = config.detect_provider(model_id)
    logger.info(f"Detected provider: {provider} (model: {model_id}, region: {config.region})")
    return BedrockClient(region=config.region)


async def main():
    """Main execution function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate hierarchical data for various categories')
    parser.add_argument('--category', '-c',
                        default='health_wellbeing',
                        help='Category to generate data for (default: health_wellbeing)')
    parser.add_argument('--platform', '-p',
                        default='youtube',
                        choices=['youtube', 'instagram'],
                        help='Platform to generate seeds for (default: youtube)')
    parser.add_argument('--model',
                        default='us.anthropic.claude-sonnet-4-6',
                        help='Model ID to use. Provider is detected automatically from the model ID. '
                             '(default: us.anthropic.claude-sonnet-4-6)')
    parser.add_argument('--list-categories', '-l',
                        action='store_true',
                        help='List available categories and exit')

    args = parser.parse_args()

    # Handle list categories request
    if args.list_categories:
        available_categories = prompt_registry.get_available_categories()
        print("Available categories:")
        for category in available_categories:
            print(f"  - {category}")
        return 0

    # Validate category
    if not prompt_registry.is_category_available(args.category):
        available_categories = prompt_registry.get_available_categories()
        logger.error(
            f"Category '{args.category}' not found. "
            f"Available categories: {available_categories}"
        )
        return 1

    # Validate platform
    if not config.is_valid_platform(args.platform):
        logger.error(
            f"Platform '{args.platform}' is not valid. "
            f"Supported platforms: youtube, instagram"
        )
        return 1

    # Set model ID and auto-detect provider
    config.model_id = args.model
    provider = config.detect_provider(config.model_id)

    logger.info(
        f"Starting generation — category: {args.category}, "
        f"platform: {args.platform}, provider: {provider} (model: {config.model_id})"
    )

    try:
        # Instantiate the correct client — provider inferred from model ID
        client = create_client(config.model_id)

        # Initialise data generator (provider-agnostic)
        generator = DataGenerator(client, args.category, args.platform)
        logger.info(
            f"Initialised DataGenerator — "
            f"category: {args.category}, platform: {args.platform}, "
            f"model: {config.model_id}"
        )

        # Generate all data
        results = await generator.generate_all_data()

        # Print results summary
        logger.info("=" * 60)
        logger.info("GENERATION COMPLETE - SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Provider:                  {provider} ({config.model_id})")
        logger.info(f"Tier 1 categories generated: {results['tier1_count']}")
        logger.info(f"Tier 2 items generated:      {results['tier2_count']}")
        logger.info(f"Tier 3 seeds generated:      {results['tier3_count']}")

        if results['errors']:
            logger.warning(f"Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                logger.warning(f"  - {error}")
        else:
            logger.info("No errors encountered")

        logger.info(f"Output files saved to: {config.get_output_dir()}/")
        logger.info(f"  - {config.get_tier1_file()}")
        logger.info(f"  - all_tier2_{args.category}.csv (aggregated Tier 2 data)")
        logger.info(f"  - tier2_{args.category}_[category].csv files (per Tier 1 category)")
        logger.info(
            f"  - all_tier3_{args.category}_{args.platform}.csv "
            f"(aggregated Tier 3 data for {args.platform})"
        )
        logger.info(
            f"  - tier3_{args.category}_{args.platform}_[practice].csv "
            f"files (per Tier 2 practice)"
        )

        total_items = results['tier1_count'] + results['tier2_count'] + results['tier3_count']
        logger.info(f"Total items generated: {total_items}")
        logger.info("=" * 60)

    except LLMError as e:
        logger.error(f"LLM provider error ({provider}): {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
