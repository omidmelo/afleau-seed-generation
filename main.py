#!/usr/bin/env python3
"""
Main execution script for Health & Wellbeing data generation
"""

import asyncio
import logging
import sys
from pathlib import Path

from bedrock_client_adapted import BedrockClient, BedrockError
from health_wellbeing_generator import HealthWellbeingDataGenerator
from health_wellbeing_config import config

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
    logger.info("Starting Health & Wellbeing data generation process")
    
    try:
        # Initialize Bedrock client
        bedrock_client = BedrockClient(region=config.region)
        logger.info(f"Initialized Bedrock client for region: {config.region}")
        
        # Initialize data generator
        generator = HealthWellbeingDataGenerator(bedrock_client)
        logger.info("Initialized Health & Wellbeing data generator")
        
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
        
        logger.info(f"Output files saved to: {config.output_dir}/")
        logger.info(f"  - {config.tier1_filename}")
        logger.info(f"  - all_tier2.csv (aggregated Tier 2 data)")
        logger.info(f"  - tier2_[category].csv files (separate file for each Tier 1 category)")
        logger.info(f"  - all_tier3.csv (aggregated Tier 3 data)")
        logger.info(f"  - tier3_[practice].csv files (separate file for each Tier 2 practice)")
        
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
    asyncio.run(main())
