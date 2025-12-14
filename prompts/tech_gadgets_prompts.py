"""
Prompt templates for Tech & Gadgets data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Tech & Gadgets domains. Generate a comprehensive list of broad categories that cover the entire spectrum of consumer technology and gadget topics.

TASK: Create 20-25 broad Tier 1 categories for Tech & Gadgets that are:
- Comprehensive and cover major consumer tech areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking tech information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical consumer tech categories

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Smartphones",
    "Laptops",
    "Smart Home"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Tech & Gadgets domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 12-15 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical tech topics

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Phone Reviews",
    "Camera Features",
    "Battery Life"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template
# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Tech & Gadgets content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 15-20 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different price points and brands
- Cover different contexts (reviews, tutorials, comparisons, etc.)
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
    "best smartphone 2025",
    "iPhone vs Android comparison",
    "budget phone reviews",
    "phone camera tips",
    "smartphone battery life"
  ]
}}

Generate exactly 15-20 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Tech & Gadgets content creation. Generate natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 15-20 natural search queries for "{tier2_name}" that sound like real Instagram searches. These should be:
- Short, hashtag-friendly phrases
- Visual and product-focused
- Include popular hashtag variations
- Cover different contexts (reviews, tips, unboxing, etc.)
- Include quick tips and visual content-focused queries

REQUIREMENTS:
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick tips, and tech inspiration

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "tech reviews",
    "gadget unboxing",
    "phone tips",
    "tech hacks",
    "gadget inspiration"
  ]
}}

Generate exactly 15-20 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


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
