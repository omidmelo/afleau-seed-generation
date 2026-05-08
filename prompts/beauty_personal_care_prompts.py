"""
Prompt templates for Beauty & Personal Care data generation
Each prompt enforces strict JSON output with validation
"""


# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in influencer marketing and creator discovery within the Beauty & Personal Care space. Your goal is to identify the broad content categories that beauty and personal care creators and influencers produce content in.

TASK: Generate 10-12 broad Tier 1 categories that cover the full spectrum of Beauty & Personal Care creator content. These categories should:
- Reflect the major niches that beauty and personal care influencers operate in
- Be broad enough to contain multiple distinct sub-niches and content types
- Be mutually exclusive with minimal overlap
- Cover both mainstream and emerging creator communities

REQUIREMENTS:
- Each category should have a clear, recognizable name used in the creator community
- Avoid overly technical or academic terminology
- Think from the perspective of a brand marketer looking to discover creators across different beauty and personal care niches

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Skincare",
    "Makeup",
    "Hair Care"
  ]
}

Generate exactly 10-12 categories. Return ONLY the JSON, no additional text."""


# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in influencer marketing and creator discovery within the Beauty & Personal Care space. Your goal is to identify specific content niches and sub-topics that creators produce content around within a given category.

TASK: Generate 6-10 specific Tier 2 sub-niches for the category "{tier1_name}" that are:
- Specific enough to represent a distinct creator niche or content focus
- Popular and widely searched on YouTube and Instagram
- Broad enough that multiple creators actively produce content in that space
- Distinct from each other with minimal overlap

REQUIREMENTS:
- Each item should represent a real, recognizable content niche within the creator community
- Think about the types of content that beauty influencers and creators actually produce within "{tier1_name}"
- Include both mainstream and niche sub-categories to ensure diverse creator discovery
- Avoid overly technical or academic terminology

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Daily Skincare Routines",
    "Anti-Aging Skincare",
    "Acne & Blemish Care"
  ]
}}

Generate exactly 6-10 items for "{tier1_name}". Return ONLY the JSON, no additional text."""


# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in influencer marketing and creator discovery. Your goal is to generate YouTube search queries that surface content produced by beauty and personal care creators and influencers — not generic informational content, but the kind of content that real beauty creators actually publish on YouTube.

TASK: Generate 15-20 YouTube search queries for "{tier2_name}" within the broader "{tier1_name}" category. These queries should:
- Reflect the content formats and styles that beauty influencers produce on YouTube (e.g., tutorials, Get Ready With Me, hauls, product reviews, comparisons, transformations, routines, unboxings)
- Surface creator-made content rather than generic informational, medical, or brand/retailer results
- Cover a diverse range of creators across: skin tones and hair types, age groups, price points (budget drugstore to high-end luxury), and beauty philosophies (clean beauty, minimalist, full glam, etc.)
- Include varied content angles (beginner vs. experienced, everyday vs. special occasion, honest reviews vs. aspirational)

REQUIREMENTS:
- Each query should be 3-8 words long
- Queries should read like real YouTube searches that surface individual creator content, not medical advice or retail pages
- Include format-specific signals such as: "routine", "tutorial", "review", "haul", "transformation", "get ready with me", "testing", "worth it"
- Ensure the full set of queries reflects diversity in demographics, price points, and creator styles

SAFETY: Exclude queries that could surface dangerous DIY cosmetic procedures, eating disorder-adjacent content, harmful skin treatments, or misleading medical claims framed as beauty advice.

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "morning skincare routine for beginners",
    "get ready with me dewy skin",
    "drugstore skincare routine oily skin",
    "testing viral skincare products",
    "affordable skincare routine dark skin"
  ]
}}

Generate exactly 15-20 search seeds for "{tier2_name}" within "{tier1_name}". Return ONLY the JSON, no additional text."""


# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in influencer marketing and creator discovery. Your goal is to generate Instagram search queries that surface content produced by beauty and personal care creators and influencers — focusing on the visual, short-form content formats that beauty creators actually publish on Instagram.

TASK: Generate 15-20 Instagram search queries for "{tier2_name}" within the broader "{tier1_name}" category. These queries should:
- Reflect the content formats and styles that beauty influencers produce on Instagram (e.g., aesthetic reels, quick tips, before/after transformations, product showcases, Get Ready With Me clips, routine snapshots, trending audio formats)
- Surface creator-made content rather than brand campaigns or retailer posts
- Cover a diverse range of creators across: skin tones and hair types, age groups, price points (budget drugstore to high-end luxury), and beauty philosophies (clean beauty, minimalist, full glam, etc.)
- Include varied content styles (aspirational/aesthetic, educational quick tips, honest reviews, community-driven)

REQUIREMENTS:
- Each query should be 2-6 words long
- Queries should read like real Instagram searches that surface individual creator content
- Include format-specific signals such as: "routine", "tips", "transformation", "review", "aesthetic", "tutorial", "look", "haul"
- Ensure the full set of queries reflects diversity in demographics, price points, and creator styles
- Focus on visual and lifestyle-oriented angles that are native to Instagram's content culture

SAFETY: Exclude queries that could surface dangerous DIY cosmetic procedures, eating disorder-adjacent content, harmful skin treatments, or misleading medical claims framed as beauty advice.

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "morning skincare routine",
    "dewy skin transformation",
    "drugstore makeup look",
    "clean beauty tips",
    "affordable skincare dark skin"
  ]
}}

Generate exactly 15-20 search seeds for "{tier2_name}" within "{tier1_name}". Return ONLY the JSON, no additional text."""


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
