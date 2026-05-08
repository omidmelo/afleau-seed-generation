"""
Configuration for data generation (supports multiple categories)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DataGenerationConfig:
    """Configuration for data generation across multiple categories"""
    # Category settings
    category: str = "health_wellbeing"  # Default category for backward compatibility

    # Platform settings
    platform: str = "youtube"  # Default platform: 'youtube' or 'instagram'

    # Bedrock settings
    region: str = "us-east-1"

    # Model settings — model IDs are unique across providers, so a single field suffices
    # model_id: str = "amazon.nova-micro-v1:0"
    model_id: str = "us.anthropic.claude-sonnet-4-6"

    # Shared inference settings
    temperature: float = 0.1
    top_p: float = 0.9
    max_tokens: int = 4000
    max_retries: int = 3
    
    # Processing settings (for future use if batch processing is re-implemented)
    # tier2_batch_size: int = 5  # Number of Tier 2 items to process in parallel
    # tier3_batch_size: int = 6  # Number of Tier 3 seeds to generate per Tier 2
    
    # Output settings
    base_output_dir: str = "data"  # Base directory for all outputs
    tier1_filename: str = "tier1.json"
    # Note: tier2 and tier3 files are now generated dynamically per category/practice
    
    # Safety settings
    max_seed_length: int = 50  # Maximum length for Tier 3 seeds
    min_seed_length: int = 10  # Minimum length for Tier 3 seeds
    
    def get_output_dir(self) -> str:
        """Get the output directory for the current category and platform"""
        return f"{self.base_output_dir}/{self.platform}/{self.category}"
    
    def get_tier1_file(self) -> str:
        """Get the Tier 1 filename for the current category"""
        return f"tier1_{self.category}.json"
    
    @staticmethod
    def detect_provider(model_id: str) -> str:
        """
        Infer the LLM provider from the model ID.

        Model ID conventions:
          Bedrock     — "vendor.model:version"
                         e.g. amazon.nova-micro-v1:0
                              us.anthropic.claude-sonnet-4-6
        """
        return "bedrock"

    @staticmethod
    def is_valid_platform(platform: str) -> bool:
        """Check if platform is valid"""
        return platform.lower() in ["youtube", "instagram"]


# Global config instance
config = DataGenerationConfig()

