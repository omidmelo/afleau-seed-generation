"""
Prompt templates for Technology data generation
Each prompt enforces strict JSON output with validation
"""

# Tier 1 Prompt Template
TIER_1_PROMPT = """You are an expert in Technology domains. Generate a comprehensive list of broad categories that cover the entire spectrum of technology topics.

TASK: Create 8-12 broad Tier 1 categories for Technology that are:
- Comprehensive and cover major technology areas
- Mutually exclusive (minimal overlap)
- Broad enough to contain multiple sub-topics
- Relevant to general audience seeking technology information

REQUIREMENTS:
- Each category should have a clear, descriptive name
- Avoid overly technical or academic terminology
- Focus on accessible, practical technology categories

SAFETY GUIDELINES:
- NO specific security vulnerabilities or exploits
- NO illegal or unethical technology practices
- NO potentially harmful recommendations
- Focus on educational and practical technology topics

Return ONLY valid JSON in this exact format:

{
  "tier1_categories": [
    "Programming",
    "Web Development",
    "Mobile Development"
  ]
}

Generate exactly 8-12 categories. Return ONLY the JSON, no additional text."""

# Tier 2 Prompt Template
TIER_2_PROMPT = """You are an expert in Technology domains. Generate specific practices, sub-topics, or areas within the given Tier 1 category.

TASK: Create 5-8 specific Tier 2 items for the category "{tier1_name}" that are:
- Specific practices, methods, or sub-areas within the category
- Popular and commonly searched topics
- Accessible to general audience
- Distinct from each other (minimal overlap)

REQUIREMENTS:
- Each item should be a specific practice or topic area
- Avoid overly technical or academic terminology
- Focus on actionable, practical topics

SAFETY GUIDELINES:
- NO specific security vulnerabilities or exploits
- NO illegal or unethical technology practices
- NO potentially harmful recommendations
- NO claims about hacking or unauthorized access
- Focus on educational and practical technology content

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_items": [
    "Python Programming",
    "JavaScript Development",
    "Database Design"
  ]
}}

Generate exactly 5-8 items for "{tier1_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - YouTube
TIER_3_YOUTUBE_PROMPT = """You are an expert in Technology content creation. Generate natural YouTube-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 6-10 natural search queries for "{tier2_name}" that sound like real YouTube searches. These should be:
- Natural, conversational search phrases
- Varied in specificity and approach
- Include different skill levels (beginner, intermediate)
- Cover different contexts (tutorial, project, review, etc.)
- Include time-based variations (5 min, 10 min, 30 min, etc.)

REQUIREMENTS:
- Each query should be 3-8 words long
- Sound like real user searches on YouTube
- Include variations in difficulty, duration, and context
- Avoid overly technical or academic language
- Be specific enough to generate targeted results

SAFETY GUIDELINES:
- NO specific security vulnerabilities or exploits
- NO illegal or unethical technology practices
- NO potentially harmful recommendations
- NO claims about hacking or unauthorized access
- NO extreme or dangerous practices
- Focus on educational and practical technology content

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "beginner python tutorial",
    "python for data analysis",
    "python web development",
    "python project ideas",
    "python debugging tips"
  ]
}}

Generate exactly 6-10 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""

# Tier 3 Prompt Template - Instagram
TIER_3_INSTAGRAM_PROMPT = """You are an expert in Technology content creation. Generate natural Instagram-style search queries (seeds) for the given Tier 2 practice.

TASK: Create 6-10 natural search queries for "{tier2_name}" that sound like real Instagram searches. These should be:
- Short, hashtag-friendly phrases
- Visual and code snippet-focused
- Include popular hashtag variations
- Cover different contexts (tips, inspiration, quick tutorials, etc.)
- Include quick tips and visual content-focused queries

REQUIREMENTS:
- Each query should be 2-6 words long
- Sound like real user searches on Instagram
- Include variations that work well with hashtags
- Avoid overly technical or academic language
- Be specific enough to generate targeted results
- Focus on visual content, quick tips, and code inspiration

SAFETY GUIDELINES:
- NO specific security vulnerabilities or exploits
- NO illegal or unethical technology practices
- NO potentially harmful recommendations
- NO claims about hacking or unauthorized access
- NO extreme or dangerous practices
- Focus on educational and practical technology content

Return ONLY valid JSON in this exact format:

{{
  "tier1_name": "{tier1_name}",
  "tier2_name": "{tier2_name}",
  "search_seeds": [
    "python tips",
    "coding inspiration",
    "web dev tricks",
    "programming hacks",
    "tech trends"
  ]
}}

Generate exactly 6-10 search seeds for "{tier2_name}". Return ONLY the JSON, no additional text."""


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
