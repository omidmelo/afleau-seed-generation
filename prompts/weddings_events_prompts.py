"""
Prompt templates for Weddings & Events data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Weddings & Events domains. Generate a comprehensive list of broad categories that cover the entire spectrum of wedding and event planning topics.

TASK: Create 12-15 broad Tier 1 categories for Weddings & Events that are:
- Comprehensive and cover major wedding and event areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking wedding and event information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical wedding and event categories
- Include both wedding planning and general event planning
- Cover different event types and planning stages

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Wedding Planning",
    "Wedding Decor",
    "Event Venues"
  ]
}

Generate exactly 12-15 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Weddings & Events domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 8-12 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical wedding and event topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Budget Planning",
    "Vendor Selection",
    "Timeline Creation"
  ]
}}

Generate exactly 8-12 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Weddings & Events content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 10-15 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different event types and planning stages
- Cover different contexts (tutorials, inspiration, tips, reviews, etc.)
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
    "wedding planning tips",
    "how to plan a wedding",
    "wedding budget guide",
    "wedding decor ideas",
    "event planning checklist"
  ]
}}

Generate exactly 10-15 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Weddings & Events content creation. Generate natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 10-15 natural search queries for "{tier2_name}" that sound like real Instagram searches. These should be:
- Short, hashtag-friendly phrases
- Visual and inspiration-focused
- Include popular hashtag variations
- Cover different contexts (inspiration, tips, real weddings, etc.)
- Include quick tips and visual content-focused queries

REQUIREMENTS:
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick tips, and wedding/event inspiration

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "wedding inspiration",
    "event planning",
    "wedding decor",
    "bridal tips",
    "wedding ideas"
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

