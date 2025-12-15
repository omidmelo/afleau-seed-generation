#!/usr/bin/env python3
"""
Script to upsert generated seeds from CSV files to PostgreSQL seeds_posts table
"""

import csv
import sys
import argparse
import logging
from pathlib import Path
from typing import Iterable, Dict, Any, Optional

import psycopg
from psycopg.rows import dict_row

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lib.util import get_pg_conn_string
from lib.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


UPSERT_SQL = """
INSERT INTO afleau.seeds_posts (platform, raw_input, parsed_json, priority)
VALUES (%(platform)s, %(raw_input)s, %(parsed_json)s::jsonb, %(priority)s)
ON CONFLICT (platform, lower(btrim(raw_input)))
DO UPDATE SET
    parsed_json = COALESCE(EXCLUDED.parsed_json, afleau.seeds_posts.parsed_json),
    priority    = GREATEST(afleau.seeds_posts.priority, COALESCE(EXCLUDED.priority, 0)),
    updated_at  = now();
"""


def read_tier3_csv(file_path: Path, category: str) -> Iterable[Dict[str, Any]]:
    """
    Read Tier 3 CSV file and yield seed dictionaries.
    
    CSV format: tier1_name, tier2_name, seed_text
    """
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seed_text = (row.get("seed_text") or "").strip()
            if not seed_text:
                continue
            
            yield {
                "category": category,
                "tier1_name": row.get("tier1_name", "").strip() or None,
                "tier2_name": row.get("tier2_name", "").strip() or None,
                "seed_text": seed_text,
            }


def upsert_seeds(
    conn_str: str,
    seeds: Iterable[Dict[str, Any]],
    platform: str,
    default_priority: int = 0,
) -> int:
    """
    Upsert seeds into afleau.seeds_posts.

    Each seed item should look like:
      {
        "category": "health_wellbeing",
        "tier1_name": "Fitness",
        "tier2_name": "Yoga",
        "seed_text": "beginner yoga for flexibility"
      }
    """
    rows = []
    for s in seeds:
        seed_text = (s.get("seed_text") or s.get("text") or "").strip()
        if not seed_text:
            continue

        category = (s.get("category") or "").strip() or None
        tier1_name = (s.get("tier1_name") or "").strip() or None
        tier2_name = (s.get("tier2_name") or "").strip() or None
        priority = s.get("priority", default_priority)

        # Build parsed_json with category hierarchy
        parsed_json = {}
        if category:
            parsed_json["category"] = category
        if tier1_name:
            parsed_json["tier1_name"] = tier1_name
        if tier2_name:
            parsed_json["tier2_name"] = tier2_name

        rows.append(
            {
                "platform": platform,
                "raw_input": seed_text,
                "parsed_json": psycopg.types.json.Json(parsed_json) if parsed_json else None,
                "priority": int(priority) if priority is not None else default_priority,
            }
        )

    if not rows:
        logger.warning("No rows to upsert")
        return 0

    logger.info(f"Upserting {len(rows)} seeds to PostgreSQL...")
    
    try:
        with psycopg.connect(conn_str, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.executemany(UPSERT_SQL, rows)
                conn.commit()
        logger.info(f"Successfully upserted {len(rows)} seeds")
        return len(rows)
    except Exception as e:
        logger.error(f"Error upserting seeds: {e}")
        raise


def get_tier3_file_path(category: str, platform: str) -> Path:
    """Get the path to the aggregated Tier 3 CSV file"""
    # Set config values temporarily to get correct output dir
    config.category = category
    config.platform = platform
    output_dir = Path(config.get_output_dir())
    filename = f"all_tier3_{category}_{platform}.csv"
    return output_dir / filename


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Upsert generated seeds from CSV files to PostgreSQL'
    )
    parser.add_argument(
        '--category', '-c',
        default='health_wellbeing',
        help='Category to upsert (default: health_wellbeing)'
    )
    parser.add_argument(
        '--platform', '-p',
        default='youtube',
        choices=['youtube', 'instagram'],
        help='Platform to upsert (default: youtube)'
    )
    parser.add_argument(
        '--priority', '-pr',
        type=int,
        default=0,
        help='Default priority for seeds (default: 0)'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='Limit the number of seeds to upsert (default: no limit)'
    )
    parser.add_argument(
        '--in-vpc',
        action='store_true',
        default=False,
        help='Use VPC private IP for database connection (default: False)'
    )
    parser.add_argument(
        '--no-vpc',
        dest='in_vpc',
        action='store_false',
        help='Use public IP for database connection (default)'
    )
    parser.add_argument(
        '--file',
        type=Path,
        help='Path to CSV file (overrides category/platform)'
    )

    args = parser.parse_args()

    # Get connection string
    try:
        conn_str = get_pg_conn_string(in_vpc=args.in_vpc)
        logger.info(f"Connecting to PostgreSQL (VPC: {args.in_vpc})")
    except Exception as e:
        logger.error(f"Failed to get connection string: {e}")
        sys.exit(1)

    # Determine file path and extract category/platform
    if args.file:
        file_path = args.file
        # Try to extract category and platform from filename
        # Pattern: all_tier3_{category}_{platform}.csv
        filename = file_path.stem
        if filename.startswith('all_tier3_'):
            parts = filename.replace('all_tier3_', '').split('_')
            if len(parts) >= 2:
                category = '_'.join(parts[:-1])
                platform = parts[-1]
            else:
                category = args.category
                platform = args.platform
        else:
            category = args.category
            platform = args.platform
    else:
        file_path = get_tier3_file_path(args.category, args.platform)
        category = args.category
        platform = args.platform

    logger.info(f"Reading seeds from: {file_path}")
    logger.info(f"Category: {category}, Platform: {platform}")

    # Read seeds from CSV
    seeds = list(read_tier3_csv(file_path, category))
    
    if not seeds:
        logger.warning(f"No seeds found in {file_path}")
        sys.exit(0)

    logger.info(f"Found {len(seeds)} seeds in CSV file")
    
    # Apply limit if specified
    if args.limit is not None and args.limit > 0:
        original_count = len(seeds)
        seeds = seeds[:args.limit]
        logger.info(f"Limiting to {len(seeds)} seeds (from {original_count} total)")

    # Upsert to PostgreSQL
    try:
        count = upsert_seeds(
            conn_str=conn_str,
            seeds=seeds,
            platform=platform,
            default_priority=args.priority
        )
        logger.info(f"Successfully upserted {count} seeds to afleau.seeds_posts")
    except Exception as e:
        logger.error(f"Failed to upsert seeds: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

