"""
Prompt templates for Food data generation
Each prompt enforces strict JSON output with validation
"""

# Configuration constants
MAX_TIER_1_ITEMS = 20
MAX_TIER_2_ITEMS = 20
MAX_TIER_3_ITEMS = 20

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Food and Culinary domains. Generate a diverse and comprehensive list of broad categories that cover the ENTIRE spectrum of food and culinary topics.

TASK: Create up to {max_tier1} broad Tier 1 categories for Food that are:
- Exhaustive and cover ALL major food and culinary areas
- Comprehensive enough to include every possible food-related topic
- Broad enough to contain multiple sub-topics
- Cover every aspect of food culture, cooking, and dining

IMPORTANT: Categories MUST include (but are NOT LIMITED to):
- Home cooking and recipes (all types, all skill levels)
- Restaurant reviews and dining experiences (all cuisines, all price points, all dining styles)
- Cafes and coffee culture (all types of cafes, coffee styles, tea culture, beverages)
- International cuisines (ALL countries, ALL regions, ALL continents - be exhaustive)
- Regional and ethnic cuisines (every region, every culture, every tradition)
- Food trends and popular dishes (current and historical)
- Cooking techniques and methods (all techniques, all equipment, all styles)
- Food culture and traditions (all cultures, all celebrations, all food rituals)
- Street food and casual dining
- Fine dining and gourmet experiences
- Baking, pastry, and desserts
- Vegetarian, vegan, and special diets
- Food festivals and events
- Food history and origins
- Food science and nutrition
- Food photography and presentation
- Food travel and culinary tourism
- Food businesses and entrepreneurship

REQUIREMENTS:
- Generate AT MOST {max_tier1} categories
- Prioritize DIVERSITY and BROAD COVERAGE - ensure the categories cover as many different aspects of food and culinary topics as possible
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical food categories
- Include both home cooking and dining out experiences
- Cover diverse cuisines from different countries and regions worldwide
- Include different types of dining experiences, cooking methods, and food cultures
- Do NOT generate more than {max_tier1} categories - focus on quality and diversity within the limit

Return ONLY valid JSON in this exact format:

{{
  "tier1_categories": [
    "Home Cooking",
    "Restaurant Reviews",
    "International Cuisines",
    "Cafes & Coffee"
  ]
}}

Generate up to {max_tier1} diverse categories that cover broad ground. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Food and Culinary domains. Generate a diverse and comprehensive list of specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create up to {max_tier2} specific Tier 2 items for the category "{tier1_name}" that cover BROAD and DIVERSE ground:
- Specific practices, methods, or sub-areas within the category
- Maximize diversity across different aspects and approaches
- Include both popular and niche topics
- Accessible to general audience
- Distinct from each other (minimal overlap)
- Cover different skill levels, contexts, and variations where relevant

REQUIREMENTS:
- Generate AT MOST {max_tier2} items
- Prioritize DIVERSITY and BROAD COVERAGE - ensure the items cover as many different aspects, practices, methods, and variations as possible, yet be specific enough to be actionable
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical food topics
- For restaurant/cafe categories: cover diverse types, cuisines, dining experiences, price points, and restaurant styles
- For home cooking categories: cover diverse techniques, cuisines, meal types, skill levels, and dietary preferences
- For international cuisine categories: cover diverse countries, regions, cultural food traditions, and ethnic cuisines
- For cooking technique categories: cover diverse methods, equipment, styles, and approaches
- For food culture categories: cover diverse cultures, traditions, celebrations, and food rituals
- Do NOT generate more than {max_tier2} items - focus on quality and diversity within the limit

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Italian Cuisine",
    "Asian Fusion",
    "Mediterranean Cooking"
  ]
}}

Generate up to {max_tier2} diverse items for "{tier1_name}" that cover broad ground. Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Food and Culinary content creation. Generate a diverse and comprehensive list of natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create up to {max_tier3} natural search queries for "{tier2_name}" that sound like real YouTube searches. These should cover BROAD and DIVERSE ground:
- Natural, conversational search phrases
- Maximize diversity across different aspects and approaches
- Include varied skill levels (beginner, intermediate, advanced)
- Cover diverse contexts (recipes, techniques, reviews, dining experiences, tutorials, tips, comparisons, etc.)
- Include time-based variations (quick, easy, 30 min, 1 hour, slow cooking, meal prep, etc.)
- Include different difficulty levels (simple, easy, advanced, complex)
- Include dietary variations (vegetarian, vegan, gluten-free, keto, paleo, etc.) where relevant
- Include regional variations (authentic, traditional, fusion, modern, etc.) where relevant
- For restaurant/cafe topics: cover different types of reviews, best places, food tours, hidden gems, local spots, fine dining, casual dining, etc.
- For home cooking topics: cover different recipes, tutorials, cooking tips, techniques, equipment, meal types, etc.
- For international cuisine topics: cover authentic recipes, cultural food, regional dishes, traditional methods, modern interpretations, etc.
- Include variations for different occasions (weeknight meals, special occasions, holidays, parties, etc.)
- Include variations for different meal types (breakfast, lunch, dinner, snacks, desserts, beverages, etc.)

REQUIREMENTS:
- Generate AT MOST {max_tier3} search queries
- Prioritize DIVERSITY and BROAD COVERAGE - ensure the seeds cover as many different aspects, contexts, skill levels, and variations, yet be specific enough to generate targeted results.
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Ensure maximum variety across all dimensions: home cooking, restaurant reviews, cafe experiences, international cuisine, techniques, tips, etc.
- Do NOT generate more than {max_tier3} seeds - focus on quality and diversity within the limit

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "easy pasta recipe",
    "best italian restaurant review",
    "homemade pasta tutorial",
    "italian cafe experience",
    "authentic italian cooking"
  ]
}}

Generate up to {max_tier3} diverse search seeds for "{tier2_name}" that cover broad ground. Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Food and Culinary content creation. Generate a diverse and comprehensive list of natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create up to {max_tier3} natural search queries for "{tier2_name}" that sound like real Instagram searches. These should cover BROAD and DIVERSE ground:
- Short, hashtag-friendly phrases
- Visual and food-focused
- Maximize diversity across different aspects and hashtag variations
- Include popular hashtag variations and trending food hashtags
- Cover diverse contexts (recipes, inspiration, tips, restaurant visits, cafe culture, food photography, meal prep, etc.)
- Include different types of visual content-focused queries
- Include dietary variations (vegetarian, vegan, gluten-free, keto, etc.) where relevant
- Include regional and cultural variations where relevant
- For restaurant/cafe topics: cover different types of food photos, restaurant recommendations, cafe culture, hidden gems, local spots, fine dining, casual dining, etc.
- For home cooking topics: cover different recipe ideas, cooking inspiration, meal prep, techniques, meal types, etc.
- For international cuisine topics: cover cultural food, authentic dishes, food travel, traditional foods, modern interpretations, etc.
- Include variations for different occasions (weeknight meals, special occasions, holidays, parties, brunch, etc.)
- Include variations for different meal types (breakfast, lunch, dinner, snacks, desserts, beverages, etc.)
- Include aesthetic variations (food styling, plating, presentation, etc.)

REQUIREMENTS:
- Generate AT MOST {max_tier3} search queries
- Prioritize DIVERSITY and BROAD COVERAGE - ensure the seeds cover as many different aspects, contexts, hashtag styles, and variations as possible
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include diverse variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick tips, and food inspiration
- Ensure maximum variety across all dimensions: home cooking, restaurant experiences, cafe culture, international cuisine, food photography, etc.
- Do NOT generate more than {max_tier3} seeds - focus on quality and diversity within the limit

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "pasta recipes",
    "restaurant food",
    "cafe culture",
    "italian cuisine",
    "food inspiration"
  ]
}}

Generate up to {max_tier3} diverse search seeds for "{tier2_name}" that cover broad ground. Return ONLY the JSON, no additional text."""


def build_tier1_prompt() -> str:
    """Build the Tier 1 generation prompt"""
    return TIER_1_PROMPT.format(max_tier1=MAX_TIER_1_ITEMS)


def build_tier2_prompt(tier1_name: str) -> str:
    """Build the Tier 2 generation prompt for a specific Tier 1 category"""
    return TIER_2_PROMPT.format(tier1_name=tier1_name, max_tier2=MAX_TIER_2_ITEMS)


def build_tier3_prompt(tier1_name: str, tier2_name: str, platform: str = "youtube") -> str:
    """Build the Tier 3 generation prompt for a specific Tier 2 item and platform"""
    if platform.lower() == "instagram":
        prompt_template = TIER_3_INSTAGRAM_PROMPT
    else:
        prompt_template = TIER_3_YOUTUBE_PROMPT
    
    return prompt_template.format(
        tier1_name=tier1_name,
        tier2_name=tier2_name,
        max_tier3=MAX_TIER_3_ITEMS
    )

