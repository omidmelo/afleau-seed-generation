"""
Prompt templates for Food data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Food and Culinary domains. Generate a COMPREHENSIVE and EXHAUSTIVE list of broad categories that cover the ENTIRE spectrum of food and culinary topics.

TASK: Create a comprehensive list of broad Tier 1 categories for Food that are:
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
- Be COMPREHENSIVE and EXHAUSTIVE - include EVERY possible food category
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical food categories
- Include both home cooking and dining out experiences
- Cover ALL cuisines from ALL countries and regions worldwide
- Include every type of dining experience, cooking method, and food culture
- Do NOT limit the number of categories - be as comprehensive as possible

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Home Cooking",
    "Restaurant Reviews",
    "International Cuisines",
    "Cafes & Coffee"
  ]
}

Generate a comprehensive and exhaustive list of categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Food and Culinary domains. Generate a COMPREHENSIVE and EXHAUSTIVE list of specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create a comprehensive list of specific Tier 2 items for the category "{tier1_name}" that are:
- EXHAUSTIVE - include ALL possible sub-topics, practices, methods, or areas
- Comprehensive enough to cover every aspect of the category
- Specific practices, methods, or sub-areas within the category
- Include both popular and niche topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Be COMPREHENSIVE and EXHAUSTIVE - include EVERY possible sub-topic
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical food topics
- For restaurant/cafe categories: include ALL specific types, ALL cuisines, ALL dining experiences, ALL price points, ALL restaurant styles
- For home cooking categories: include ALL techniques, ALL cuisines, ALL meal types, ALL skill levels, ALL dietary preferences
- For international cuisine categories: include ALL countries, ALL regions, ALL cultural food traditions, ALL ethnic cuisines - be exhaustive
- For cooking technique categories: include ALL methods, ALL equipment, ALL styles, ALL approaches
- For food culture categories: include ALL cultures, ALL traditions, ALL celebrations, ALL food rituals
- Do NOT limit the number of items - be as comprehensive as possible

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Italian Cuisine",
    "Asian Fusion",
    "Mediterranean Cooking"
  ]
}}

Generate a comprehensive and exhaustive list of items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Food and Culinary content creation. Generate a COMPREHENSIVE and EXHAUSTIVE list of natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create a comprehensive list of natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- EXHAUSTIVE - include ALL possible search variations and approaches
- Natural, conversational search phrases
- Varied in specificity and approach
- Include ALL skill levels (beginner, intermediate, advanced, expert, professional)
- Cover ALL contexts (recipes, techniques, reviews, dining experiences, tutorials, tips, comparisons, etc.)
- Include ALL time-based variations (quick, easy, 30 min, 1 hour, slow cooking, meal prep, etc.)
- Include ALL difficulty levels (simple, easy, advanced, complex, professional)
- Include ALL dietary variations (vegetarian, vegan, gluten-free, keto, paleo, etc.)
- Include ALL regional variations (authentic, traditional, fusion, modern, etc.)
- For restaurant/cafe topics: include ALL types of reviews, best places, food tours, hidden gems, local spots, fine dining, casual dining, etc.
- For home cooking topics: include ALL recipes, ALL tutorials, ALL cooking tips, ALL techniques, ALL equipment, ALL meal types, etc.
- For international cuisine topics: include ALL authentic recipes, ALL cultural food, ALL regional dishes, ALL traditional methods, ALL modern interpretations, etc.
- Include variations for different occasions (weeknight meals, special occasions, holidays, parties, etc.)
- Include variations for different meal types (breakfast, lunch, dinner, snacks, desserts, beverages, etc.)

REQUIREMENTS:
- Be COMPREHENSIVE and EXHAUSTIVE - generate as many search queries as possible
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Include ALL possible variations in difficulty, duration, context, dietary needs, and approach
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Mix ALL aspects: home cooking, restaurant reviews, cafe experiences, international cuisine, techniques, tips, etc.
- Do NOT limit the number of search seeds - be as comprehensive as possible

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

Generate a comprehensive and exhaustive list of search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Food and Culinary content creation. Generate a COMPREHENSIVE and EXHAUSTIVE list of natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create a comprehensive list of natural search queries for "{tier2_name}" that sound like real Instagram searches. These should be:
- EXHAUSTIVE - include ALL possible search variations and hashtag-friendly phrases
- Short, hashtag-friendly phrases
- Visual and food-focused
- Include ALL popular hashtag variations and trending food hashtags
- Cover ALL contexts (recipes, inspiration, tips, restaurant visits, cafe culture, food photography, meal prep, etc.)
- Include ALL types of visual content-focused queries
- Include ALL dietary variations (vegetarian, vegan, gluten-free, keto, etc.)
- Include ALL regional and cultural variations
- For restaurant/cafe topics: include ALL types of food photos, restaurant recommendations, cafe culture, hidden gems, local spots, fine dining, casual dining, etc.
- For home cooking topics: include ALL recipe ideas, ALL cooking inspiration, ALL meal prep, ALL techniques, ALL meal types, etc.
- For international cuisine topics: include ALL cultural food, ALL authentic dishes, ALL food travel, ALL traditional foods, ALL modern interpretations, etc.
- Include variations for different occasions (weeknight meals, special occasions, holidays, parties, brunch, etc.)
- Include variations for different meal types (breakfast, lunch, dinner, snacks, desserts, beverages, etc.)
- Include aesthetic variations (food styling, plating, presentation, etc.)

REQUIREMENTS:
- Be COMPREHENSIVE and EXHAUSTIVE - generate as many search queries as possible
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include ALL possible variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick tips, and food inspiration
- Mix ALL aspects: home cooking, restaurant experiences, cafe culture, international cuisine, food photography, etc.
- Do NOT limit the number of search seeds - be as comprehensive as possible

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

Generate a comprehensive and exhaustive list of search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


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

