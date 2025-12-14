"""
Prompt templates for Pets & Animals data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Pets & Animals domains. Generate a comprehensive list of broad categories that cover the entire spectrum of pet care and animal-related topics.

TASK: Create 8-12 broad Tier 1 categories for Pets & Animals that are:
- Comprehensive and cover major pet/animal areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking pet/animal information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical pet/animal categories

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Pet Care",
    "Animal Training",
    "Wildlife"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Pets & Animals domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 5-8 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical pet/animal topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Dog Training",
    "Cat Care",
    "Pet Health"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
TIER_3_PROMPT = """You are an expert in Pets & Animals content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 8-12 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different pet types and animal species
- Cover different contexts (training, health, behavior, etc.)
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
    "dog training tips",
    "cat behavior problems",
    "pet health checkup",
    "puppy training basics",
    "bird care guide"
  ]
}}

Generate exactly 8-12 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


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
