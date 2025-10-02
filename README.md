# Health & Wellbeing Data Generation

This project generates hierarchical structured data for the Health & Wellbeing domain using AWS Bedrock's `amazon.nova-micro-v1:0` model.

## Overview

The system creates three tiers of data:
- **Tier 1**: Broad categories (Fitness, Nutrition, Mental Health, etc.)
- **Tier 2**: Specific practices/sub-topics under each Tier 1 (Yoga, Intermittent Fasting, Sleep Hygiene)
- **Tier 3**: Natural YouTube-style search queries/seeds derived from Tier 2 ("20 min yoga for beginners at home")

## Features

- **Resumable**: Automatically resumes from checkpoints if interrupted
- **Safe Content**: Filters out medical advice and potentially harmful content
- **Deduplication**: Removes duplicate search seeds
- **Batch Processing**: Efficiently handles large datasets
- **CSV Output**: Structured data saved to CSV files for easy analysis

## Prerequisites

1. AWS credentials configured (via AWS CLI, environment variables, or IAM role)
2. Access to AWS Bedrock service
3. Python 3.8+

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `health_wellbeing_config.py` to customize:
- Bedrock model settings (temperature, max_tokens, etc.)
- Batch sizes for processing
- Output file names and locations
- Safety filters

## Usage

```bash
python main.py
```

The script will:
1. Generate Tier 1 categories and save to `output/tier1.json`
2. Generate Tier 2 items for each Tier 1 category and save to separate CSV files
3. Generate Tier 3 search seeds for each Tier 2 item and save to separate CSV files

## Output Files

- **tier1.json**: Tier 1 categories (list of category names)
- **all_tier2.csv**: Aggregated CSV file with ALL Tier 2 data (columns: tier1_name, tier2_name)
- **tier2_[category].csv**: Separate CSV file for each Tier 1 category with columns: tier1_name, tier2_name
- **all_tier3.csv**: Aggregated CSV file with ALL Tier 3 data (columns: tier1_name, tier2_name, seed_text)
- **tier3_[practice].csv**: Separate CSV file for each Tier 2 practice with columns: tier1_name, tier2_name, seed_text

### File Naming Examples:
- `all_tier2.csv` - Contains ALL Tier 2 practices from all categories
- `tier2_fitness.csv` - Contains only fitness-related Tier 2 practices
- `tier2_nutrition.csv` - Contains only nutrition-related Tier 2 practices
- `all_tier3.csv` - Contains ALL Tier 3 search seeds from all practices
- `tier3_yoga.csv` - Contains only yoga-related Tier 3 search seeds
- `tier3_meal_prep.csv` - Contains only meal prep-related Tier 3 search seeds

## Resumability

The system automatically saves progress after each major step:
- If Tier 1 already exists, it skips generation
- If individual Tier 2 files exist, it only generates missing category files
- If individual Tier 3 files exist, it only generates missing practice files
- Each file is independent, so you can resume from any point

## Safety Features

- Filters out content containing medical advice, diagnostic claims, or brand names
- Enforces content length limits
- Removes duplicate search seeds
- Focuses on general wellness and educational content

## Logging

All operations are logged to both console and `health_wellbeing_generation.log`.

## Error Handling

- Automatic retries for Bedrock API calls
- Graceful handling of individual failures
- Comprehensive error logging
- Checkpoint recovery

## Example Output

### Tier 1 (tier1.json)
```json
[
  "Fitness",
  "Nutrition",
  "Mental Health"
]
```

### Tier 2 (all_tier2.csv - aggregated)
```csv
tier1_name,tier2_name
Fitness,Yoga
Fitness,Strength Training
Fitness,Cardio
Nutrition,Meal Prep
Nutrition,Healthy Snacking
Mental Health,Meditation
```

### Tier 2 (tier2_fitness.csv - category-specific)
```csv
tier1_name,tier2_name
Fitness,Yoga
Fitness,Strength Training
Fitness,Cardio
```

### Tier 3 (all_tier3.csv - aggregated)
```csv
tier1_name,tier2_name,seed_text
Fitness,Yoga,beginner yoga for flexibility
Fitness,Yoga,10 minute morning yoga routine
Nutrition,Meal Prep,healthy meal prep for weight loss
Mental Health,Meditation,5 minute morning meditation
```

### Tier 3 (tier3_yoga.csv - practice-specific)
```csv
tier1_name,tier2_name,seed_text
Fitness,Yoga,beginner yoga for flexibility
Fitness,Yoga,10 minute morning yoga routine
Fitness,Yoga,yoga for back pain relief
```
