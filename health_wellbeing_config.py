"""
Configuration for Health & Wellbeing data generation
"""

from dataclasses import dataclass


@dataclass
class HealthWellbeingConfig:
    """Configuration for Health & Wellbeing data generation"""
    # Bedrock settings
    region: str = "us-east-1"
    model_id: str = "amazon.nova-micro-v1:0"
    temperature: float = 0.1
    top_p: float = 0.9
    max_tokens: int = 4000
    max_retries: int = 3
    
    # Processing settings (for future use if batch processing is re-implemented)
    # tier2_batch_size: int = 5  # Number of Tier 2 items to process in parallel
    # tier3_batch_size: int = 6  # Number of Tier 3 seeds to generate per Tier 2
    
    # Output settings
    output_dir: str = "output"
    tier1_filename: str = "tier1.json"
    # Note: tier2 and tier3 files are now generated dynamically per category/practice
    
    # Safety settings
    max_seed_length: int = 50  # Maximum length for Tier 3 seeds
    min_seed_length: int = 10  # Minimum length for Tier 3 seeds


# Global config instance
config = HealthWellbeingConfig()
