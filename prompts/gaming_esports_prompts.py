"""
Prompt templates for Gaming & Esports data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Gaming & Esports domains. Generate a comprehensive list of broad categories that cover the entire spectrum of gaming and esports topics.

TASK: Create 8-12 broad Tier 1 categories for Gaming & Esports that are:
- Comprehensive and cover major gaming/esports areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking gaming information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or niche terminology
- Focus on accessible, popular gaming categories

SAFETY GUIDELINES:
- NO content promoting violence or harmful behavior
- NO gambling or betting content
- NO cheating or exploiting content
- Focus on educational and entertainment gaming content

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Game Genres",
    "Esports",
    "Gaming Hardware"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Gaming & Esports domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 5-8 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or niche terminology
- Focus on actionable, practical gaming topics

SAFETY GUIDELINES:
- NO content promoting violence or harmful behavior
- NO gambling or betting content
- NO cheating or exploiting content
- NO content that could be harmful to minors
- Focus on educational and entertainment gaming content

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Action Games",
    "Strategy Games",
    "RPG Games"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
TIER_3_PROMPT = """You are an expert in Gaming & Esports content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 6-10 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different skill levels (beginner, intermediate, advanced)
- Cover different contexts (tutorial, review, gameplay, etc.)
- Include time-based variations (5 min, 10 min, 30 min, etc.)

REQUIREMENTS:
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Include variations in difficulty, duration, and context
- Avoid overly technical or niche language
- Be specific enough to generate targeted results

SAFETY GUIDELINES:
- NO content promoting violence or harmful behavior
- NO gambling or betting content
- NO cheating or exploiting content
- NO content that could be harmful to minors
- NO extreme or dangerous gaming practices
- Focus on educational and entertainment gaming content

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "beginner gaming tips",
    "gaming setup guide",
    "best gaming strategies",
    "gaming tutorial for kids",
    "gaming equipment review"
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
