"""
Prompt templates for Entertainment & Comedy data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Entertainment & Comedy domains. Generate a comprehensive list of broad categories that cover the entire spectrum of entertainment and comedy topics.

TASK: Create 12-15 broad Tier 1 categories for Entertainment & Comedy that are:
- Comprehensive and cover major entertainment/comedy areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking entertainment/comedy content

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, popular entertainment categories
- Include both comedy and general entertainment topics
- Cover different content formats and styles

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Comedy Sketches",
    "Memes",
    "Viral Content"
  ]
}

Generate exactly 12-15 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Entertainment & Comedy domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 8-12 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, popular entertainment topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Stand-up Comedy",
    "Pranks",
    "Reaction Videos"
  ]
}}

Generate exactly 8-12 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Entertainment & Comedy content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 10-15 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different comedy styles and entertainment formats
- Cover different contexts (funny videos, comedy shows, viral content, etc.)
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
    "funny comedy videos",
    "best pranks compilation",
    "viral meme reactions",
    "stand up comedy specials",
    "entertainment funny moments"
  ]
}}

Generate exactly 10-15 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Entertainment & Comedy content creation. Generate natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 10-15 natural search queries for "{tier2_name}" that sound like real Instagram searches. These should be:
- Short, hashtag-friendly phrases
- Visual and entertainment-focused
- Include popular hashtag variations
- Cover different contexts (funny, memes, viral, comedy, etc.)
- Include quick tips and visual content-focused queries

REQUIREMENTS:
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick entertainment, and comedy inspiration

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "funny videos",
    "comedy memes",
    "viral content",
    "funny reels",
    "entertainment"
  ]
}}

Generate exactly 10-15 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


def build_tier1_prompt() -> str:
    """Build the Tier 1 generation prompt"""
    return TIER_1_PROMPT


def build_tier2_prompt(tier1_name: str) -> str:
    """Build the Tier 2 generation prompt for a specific Tier 1 category"""
    return TIER_2_PROMPT.format(tier1_name=tier1_name)


def build_tier3_prompt(tier1_name: str, tier2_name: str, platform: str = "youtube") -> str:
    """Build the Tier 3 generation prompt for a specific Tier 2 item and platform"""
    if platform.lower() == "instagram":
        prompt_template = TIER_3_INSTAGRAM_PROMPT
    else:
        prompt_template = TIER_3_YOUTUBE_PROMPT
    
    return prompt_template.format(
        tier1_name=tier1_name,
        tier2_name=tier2_name
    )

