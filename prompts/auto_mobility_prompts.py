"""
Prompt templates for Auto & Mobility data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Auto & Mobility domains. Generate a comprehensive list of broad categories that cover the entire spectrum of automotive and transportation topics.

TASK: Create 8-12 broad Tier 1 categories for Auto & Mobility that are:
- Comprehensive and cover major automotive/transportation areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking automotive information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical automotive categories

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Vehicle Maintenance",
    "Driving Skills",
    "Car Buying"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Auto & Mobility domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 5-8 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical automotive topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Oil Changes",
    "Tire Care",
    "Engine Maintenance"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
TIER_3_PROMPT = """You are an expert in Auto & Mobility content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 6-10 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different skill levels (beginner, intermediate, advanced)
- Cover different contexts (DIY, professional, emergency, etc.)
- Include time-based variations (5 min, 10 min, 30 min, etc.)

REQUIREMENTS:
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Include variations in difficulty, duration, and context
- Avoid overly technical or academic language
- Be specific enough to generate targeted results

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "car maintenance tips",
    "DIY oil change guide",
    "tire pressure check",
    "engine troubleshooting basics",
    "car cleaning hacks"
  ]
}}

Generate exactly 6-10 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


def build_tier1_prompt() -> str:
    """Build the Tier 1 generation prompt"""
    return TIER_1_PROMPT


def build_tier2_prompt(tier1_name: str) -> str:
    """Build the Tier 2 generation prompt for a specific Tier 1 category"""
    return TIER_2_PROMPT.format(tier1_name=tier1_name)


def build_tier3_prompt(tier1_name: str, tier2_name: str) -> str:
    """Build the Tier 3 generation prompt for a specific Tier 2 item"""
    return TIER_3_PROMPT.format(
        tier1_name=tier1_name,
        tier2_name=tier2_name
    )
