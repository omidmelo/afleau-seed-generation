#!/usr/bin/env python3
"""
Main execution script for data generation across multiple categories
"""

import asyncio
import logging
import sys
import argparse
from pathlib import Path

from bedrock_client_adapted import BedrockClient, BedrockError
from data_generator import DataGenerator
from data_generation_config import config
from prompt_registry import prompt_registry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('health_wellbeing_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


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
        logger.error(f"Category '{args.category}' not found. Available categories: {available_categories}")
        return 1
    
    # Validate platform
    if not config.is_valid_platform(args.platform):
        logger.error(f"Platform '{args.platform}' is not valid. Supported platforms: youtube, instagram")
        return 1
    
    logger.info(f"Starting data generation process for category: {args.category}, platform: {args.platform}")
    
    try:
        # Initialize Bedrock client
        bedrock_client = BedrockClient(region=config.region)
        logger.info(f"Initialized Bedrock client for region: {config.region}")
        
        # Initialize data generator
        generator = DataGenerator(bedrock_client, args.category, args.platform)
        logger.info(f"Initialized data generator for category: {args.category}, platform: {args.platform}")
        
        # Generate all data
        results = await generator.generate_all_data()
        
        # Print results summary
        logger.info("=" * 60)
        logger.info("GENERATION COMPLETE - SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Tier 1 categories generated: {results['tier1_count']}")
        logger.info(f"Tier 2 items generated: {results['tier2_count']}")
        logger.info(f"Tier 3 seeds generated: {results['tier3_count']}")
        
        if results['errors']:
            logger.warning(f"Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                logger.warning(f"  - {error}")
        else:
            logger.info("No errors encountered")
        
        logger.info(f"Output files saved to: {config.get_output_dir()}/")
        logger.info(f"  - {config.get_tier1_file()}")
        logger.info(f"  - all_tier2_{args.category}.csv (aggregated Tier 2 data)")
        logger.info(f"  - tier2_{args.category}_[category].csv files (separate file for each Tier 1 category)")
        logger.info(f"  - all_tier3_{args.category}_{args.platform}.csv (aggregated Tier 3 data for {args.platform})")
        logger.info(f"  - tier3_{args.category}_{args.platform}_[practice].csv files (separate file for each Tier 2 practice)")
        
        # Calculate totals
        total_items = results['tier1_count'] + results['tier2_count'] + results['tier3_count']
        logger.info(f"Total items generated: {total_items}")
        
        logger.info("=" * 60)
        
    except BedrockError as e:
        logger.error(f"Bedrock API error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
