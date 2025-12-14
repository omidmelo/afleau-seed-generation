# Multi-Category Data Generation

This project generates hierarchical structured data for multiple domains using AWS Bedrock's `amazon.nova-micro-v1:0` model. The system supports various categories including Health & Wellbeing, Technology, Gaming, Travel, and many more.

## Overview

The system creates three tiers of data for any supported category:
- **Tier 1**: Broad categories (e.g., for Health & Wellbeing: Fitness, Nutrition, Mental Health)
- **Tier 2**: Specific practices/sub-topics under each Tier 1 (e.g., Yoga, Intermittent Fasting, Sleep Hygiene)
- **Tier 3**: Natural YouTube-style search queries/seeds derived from Tier 2 (e.g., "20 min yoga for beginners at home")

## Features

- **Multi-Category Support**: Generate data for multiple domains (Health & Wellbeing, Technology, Gaming, Travel, etc.)
- **Resumable**: Automatically resumes from checkpoints if interrupted
- **Category-Specific Prompts**: Each category has customized prompts for better results
- **Deduplication**: Removes duplicate search seeds
- **Batch Processing**: Efficiently handles large datasets
- **CSV Output**: Structured data saved to CSV files for easy analysis
- **Command-Line Interface**: Easy category selection via CLI arguments

## Prerequisites

1. AWS credentials configured (via AWS CLI, environment variables, or IAM role)
2. Access to AWS Bedrock service
3. Python 3.8+

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `data_generation_config.py` to customize:
- Bedrock model settings (temperature, max_tokens, etc.)
- Default category
- Output directory structure
- Content validation settings (seed length limits, etc.)

Category-specific prompts are located in the `prompts/` directory. Each category has its own prompt file (e.g., `prompts/health_wellbeing_prompts.py`).

## Usage

### List Available Categories

```bash
python main.py --list-categories
```

### Generate Data for a Specific Category

```bash
# Use default category (health_wellbeing)
python main.py

# Specify a category
python main.py --category technology
python main.py --category gaming_esports
python main.py --category travel_experiences
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

The script will:
1. Generate Tier 1 categories and save to `output_{category}/tier1_{category}.json`
2. Generate Tier 2 items for each Tier 1 category and save to separate CSV files
3. Generate Tier 3 search seeds for each Tier 2 item and save to separate CSV files

## Output Files

Each category generates its own output directory: `output_{category}/`

### File Structure

For each category (e.g., `health_wellbeing`), the following files are generated:

- **tier1_{category}.json**: Tier 1 categories (list of category names)
- **all_tier2_{category}.csv**: Aggregated CSV file with ALL Tier 2 data (columns: tier1_name, tier2_name)
- **tier2_{category}_[tier1_name].csv**: Separate CSV file for each Tier 1 category (columns: tier1_name, tier2_name)
- **all_tier3_{category}.csv**: Aggregated CSV file with ALL Tier 3 data (columns: tier1_name, tier2_name, seed_text)
- **tier3_{category}_[tier2_name].csv**: Separate CSV file for each Tier 2 practice (columns: tier1_name, tier2_name, seed_text)

### File Naming Examples (Health & Wellbeing):

- `output_health_wellbeing/tier1_health_wellbeing.json` - Tier 1 categories
- `output_health_wellbeing/all_tier2_health_wellbeing.csv` - All Tier 2 practices
- `output_health_wellbeing/tier2_health_wellbeing_fitness.csv` - Fitness-related Tier 2 practices
- `output_health_wellbeing/tier2_health_wellbeing_nutrition.csv` - Nutrition-related Tier 2 practices
- `output_health_wellbeing/all_tier3_health_wellbeing.csv` - All Tier 3 search seeds
- `output_health_wellbeing/tier3_health_wellbeing_yoga.csv` - Yoga-related Tier 3 search seeds
- `output_health_wellbeing/tier3_health_wellbeing_meal_prep.csv` - Meal prep-related Tier 3 search seeds

## Resumability

The system automatically saves progress after each major step:
- If Tier 1 already exists for a category, it skips generation
- If individual Tier 2 files exist, it only generates missing category files
- If individual Tier 3 files exist, it only generates missing practice files
- Each file is independent, so you can resume from any point
- Category-specific output directories ensure no conflicts between categories

## Content Validation

- Enforces content length limits (configurable in `data_generation_config.py`)
- Removes duplicate search seeds using MD5 hashing
- Category-specific prompts ensure appropriate content generation
- Each category can have its own validation rules

## Logging

All operations are logged to both console and `health_wellbeing_generation.log`. The log file contains detailed information about the generation process, including API calls, errors, and progress updates.

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
- `build_tier3_prompt(tier1_name: str, tier2_name: str) -> str`

The system will automatically discover and register the new category. See existing prompt files in `prompts/` for examples.
