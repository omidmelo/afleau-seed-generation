# Multi-Category Data Generation

This project generates hierarchical structured data for multiple domains using AWS Bedrock's `amazon.nova-micro-v1:0` model. The system supports various categories including Health & Wellbeing, Technology, Gaming, Travel, and many more.

## Overview

The system creates three tiers of data for any supported category and platform:
- **Tier 1**: Broad categories (e.g., for Health & Wellbeing: Fitness, Nutrition, Mental Health)
- **Tier 2**: Specific practices/sub-topics under each Tier 1 (e.g., Yoga, Intermittent Fasting, Sleep Hygiene)
- **Tier 3**: Natural search queries/seeds derived from Tier 2, tailored for the selected platform (YouTube or Instagram)

## Features

- **Multi-Category Support**: Generate data for multiple domains (Health & Wellbeing, Technology, Gaming, Travel, Food, etc.)
- **Multi-Platform Support**: Generate seeds for YouTube or Instagram with platform-specific prompts
- **Resumable**: Automatically resumes from checkpoints if interrupted
- **Category-Specific Prompts**: Each category has customized prompts for better results
- **Platform-Specific Content**: Tier 3 seeds are tailored for the selected platform
- **Deduplication**: Removes duplicate search seeds
- **Batch Processing**: Efficiently handles large datasets
- **CSV Output**: Structured data saved to CSV files for easy analysis
- **Command-Line Interface**: Easy category and platform selection via CLI arguments

## Prerequisites

1. AWS credentials configured (via AWS CLI, environment variables, or IAM role)
2. Access to AWS Bedrock service
3. Python 3.8+

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `lib/config.py` to customize:
- Bedrock model settings (temperature, max_tokens, etc.)
- Default category and platform
- Output directory structure
- Content validation settings (seed length limits, etc.)

Category-specific prompts are located in the `prompts/` directory. Each category has its own prompt file (e.g., `prompts/health_wellbeing_prompts.py`). Each prompt file includes platform-specific templates for YouTube and Instagram.

## Usage

### List Available Categories

```bash
python3 scripts/generate_seeds.py --list-categories
```

### Generate Data for a Specific Category and Platform

```bash
# Use default category (health_wellbeing) and platform (youtube)
python3 scripts/generate_seeds.py

# Specify a category (defaults to youtube platform)
python3 scripts/generate_seeds.py --category technology
python3 scripts/generate_seeds.py --category gaming_esports
python3 scripts/generate_seeds.py --category food

# Specify both category and platform
python3 scripts/generate_seeds.py --category food --platform youtube
python3 scripts/generate_seeds.py --category food --platform instagram
python3 scripts/generate_seeds.py -c health_wellbeing -p instagram
```

### Available Categories

- `health_wellbeing` - Health, fitness, nutrition, mental wellness
- `technology` - Software, programming, cloud computing, AI
- `gaming_esports` - Video games, esports, gaming hardware
- `parenting_family` - Parenting tips, family activities, child development
- `sustainability_activism` - Environmental conservation, social justice
- `auto_mobility` - Automotive, transportation, vehicle maintenance
- `luxury_lifestyle` - High-end fashion, fine dining, premium experiences
- `home_diy_decor` - Home improvement, DIY projects, interior design
- `travel_experiences` - Travel destinations, tourism, cultural experiences
- `tech_gadgets` - Consumer electronics, gadgets, tech reviews
- `pets_animals` - Pet care, animal training, wildlife
- `niche_novelty` - Unique hobbies, collectibles, specialized interests
- `beauty_personal_care` - Skincare, makeup, grooming, personal care
- `food` - Home cooking, restaurant reviews, cafes, international cuisines

### Supported Platforms

- `youtube` - YouTube-style search queries (longer, conversational phrases)
- `instagram` - Instagram-style search queries (shorter, hashtag-friendly phrases)

The script will:
1. Generate Tier 1 categories and save to `data/{platform}/{category}/tier1_{category}.json`
2. Generate Tier 2 items for each Tier 1 category and save to separate CSV files
3. Generate Tier 3 search seeds (platform-specific) for each Tier 2 item and save to separate CSV files

## Output Files

Outputs are organized by platform first, then category: `data/{platform}/{category}/`

### File Structure

For each category and platform combination (e.g., `health_wellbeing` on `youtube`), the following files are generated:

- **tier1_{category}.json**: Tier 1 categories (list of category names)
- **all_tier2_{category}.csv**: Aggregated CSV file with ALL Tier 2 data (columns: tier1_name, tier2_name)
- **tier2_{category}_{platform}_[tier1_name].csv**: Separate CSV file for each Tier 1 category (columns: tier1_name, tier2_name)
- **all_tier3_{category}_{platform}.csv**: Aggregated CSV file with ALL Tier 3 data (columns: tier1_name, tier2_name, seed_text)
- **tier3_{category}_{platform}_[tier2_name].csv**: Separate CSV file for each Tier 2 practice (columns: tier1_name, tier2_name, seed_text)

### File Naming Examples

#### YouTube Platform - Health & Wellbeing:
- `data/youtube/health_wellbeing/tier1_health_wellbeing.json` - Tier 1 categories
- `data/youtube/health_wellbeing/all_tier2_health_wellbeing.csv` - All Tier 2 practices
- `data/youtube/health_wellbeing/tier2_health_wellbeing_youtube_fitness.csv` - Fitness-related Tier 2 practices
- `data/youtube/health_wellbeing/all_tier3_health_wellbeing_youtube.csv` - All Tier 3 YouTube search seeds
- `data/youtube/health_wellbeing/tier3_health_wellbeing_youtube_yoga.csv` - Yoga-related Tier 3 YouTube search seeds

#### Instagram Platform - Food:
- `data/instagram/food/tier1_food.json` - Tier 1 categories
- `data/instagram/food/all_tier2_food.csv` - All Tier 2 practices
- `data/instagram/food/tier2_food_instagram_international_cuisines.csv` - International cuisines Tier 2
- `data/instagram/food/all_tier3_food_instagram.csv` - All Tier 3 Instagram search seeds
- `data/instagram/food/tier3_food_instagram_italian_cuisine.csv` - Italian cuisine Tier 3 Instagram search seeds

## Resumability

The system automatically saves progress after each major step:
- If Tier 1 already exists for a category/platform combination, it skips generation
- If individual Tier 2 files exist, it only generates missing category files
- If individual Tier 3 files exist, it only generates missing practice files
- Each file is independent, so you can resume from any point
- Platform and category-specific output directories ensure no conflicts between different runs

## Content Validation

- Enforces content length limits (configurable in `lib/config.py`)
- Removes duplicate search seeds using MD5 hashing
- Category-specific prompts ensure appropriate content generation
- Platform-specific prompts ensure content is tailored for YouTube or Instagram
- Each category can have its own validation rules

## Logging

All operations are logged to both console and `logs/health_wellbeing_generation.log`. The log file contains detailed information about the generation process, including API calls, errors, and progress updates. Log files are stored in the `logs/` directory.

## Error Handling

- Automatic retries for Bedrock API calls
- Graceful handling of individual failures
- Comprehensive error logging
- Checkpoint recovery

## Example Output

### Health & Wellbeing Category

#### Tier 1 (tier1_health_wellbeing.json)
```json
[
  "Fitness",
  "Nutrition",
  "Mental Health"
]
```

#### Tier 2 (all_tier2_health_wellbeing.csv - aggregated)
```csv
tier1_name,tier2_name
Fitness,Yoga
Fitness,Strength Training
Fitness,Cardio
Nutrition,Meal Prep
Nutrition,Healthy Snacking
Mental Health,Meditation
```

#### Tier 2 (tier2_health_wellbeing_fitness.csv - category-specific)
```csv
tier1_name,tier2_name
Fitness,Yoga
Fitness,Strength Training
Fitness,Cardio
```

#### Tier 3 (all_tier3_health_wellbeing.csv - aggregated)
```csv
tier1_name,tier2_name,seed_text
Fitness,Yoga,beginner yoga for flexibility
Fitness,Yoga,10 minute morning yoga routine
Nutrition,Meal Prep,healthy meal prep for weight loss
Mental Health,Meditation,5 minute morning meditation
```

#### Tier 3 (tier3_health_wellbeing_yoga.csv - practice-specific)
```csv
tier1_name,tier2_name,seed_text
Fitness,Yoga,beginner yoga for flexibility
Fitness,Yoga,10 minute morning yoga routine
Fitness,Yoga,yoga for back pain relief
```

## Adding New Categories

To add a new category, create a prompt file in the `prompts/` directory following the naming convention `{category_name}_prompts.py`. The file must implement three functions:

- `build_tier1_prompt() -> str`
- `build_tier2_prompt(tier1_name: str) -> str`
- `build_tier3_prompt(tier1_name: str, tier2_name: str, platform: str = "youtube") -> str`

The `build_tier3_prompt` function must handle both `youtube` and `instagram` platforms, returning platform-specific prompts. The system will automatically discover and register the new category. See existing prompt files in `prompts/` for examples.

## Project Structure

```
.
├── scripts/
│   └── generate_seeds.py      # Main execution script
├── lib/
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── bedrock_client.py       # AWS Bedrock client
│   ├── generator.py            # Data generation logic
│   └── registry.py             # Prompt registry for category discovery
├── prompts/
│   ├── __init__.py
│   ├── health_wellbeing_prompts.py
│   ├── technology_prompts.py
│   ├── food_prompts.py
│   └── ...                     # Other category prompt files
├── data/                       # Generated output files
│   ├── youtube/
│   │   ├── health_wellbeing/
│   │   ├── food/
│   │   └── ...
│   └── instagram/
│       ├── health_wellbeing/
│       ├── food/
│       └── ...
├── logs/                       # Log files
├── tests/                      # Test files
├── requirements.txt
└── README.md
```
