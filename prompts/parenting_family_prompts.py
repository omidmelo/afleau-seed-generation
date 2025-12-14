"""
Prompt templates for Parenting & Family data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Parenting & Family domains. Generate a comprehensive list of broad categories that cover the entire spectrum of parenting and family topics.

TASK: Create 8-12 broad Tier 1 categories for Parenting & Family that are:
- Comprehensive and cover major parenting/family areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to parents and families seeking guidance

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly clinical or academic terminology
- Focus on accessible, practical parenting categories

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Child Development",
    "Parenting Strategies",
    "Family Activities"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Parenting & Family domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 5-8 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly clinical or academic terminology
- Focus on actionable, practical parenting topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Early Childhood Development",
    "Teenage Parenting",
    "Special Needs Parenting"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
TIER_3_PROMPT = """You are an expert in Parenting & Family content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 6-10 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different age groups (toddlers, kids, teens, etc.)
- Cover different contexts (home, school, activities, etc.)
- Include time-based variations (5 min, 10 min, 30 min, etc.)

REQUIREMENTS:
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Include variations in difficulty, duration, and context
- Avoid overly clinical or academic language
- Be specific enough to generate targeted results

SAFETY GUIDELINES:
- NO specific medical advice or diagnostic claims
- NO content that could be harmful to children
- NO extreme or controversial parenting methods
- NO content promoting unsafe practices
- NO content that could be inappropriate for children
- Focus on evidence-based, positive parenting approaches
- Ensure all content is family-friendly and age-appropriate

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "toddler activities at home",
    "positive parenting tips",
    "family bonding activities",
    "child development milestones",
    "parenting challenges solutions"
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
