#!/usr/bin/env python3
"""
Test script to verify the setup and configuration
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported"""
    try:
        from lib.bedrock_client import BedrockClient, BedrockError
        from lib.generator import DataGenerator
        from lib.config import config
        from lib.registry import prompt_registry
        from prompts.health_wellbeing_prompts import build_tier1_prompt, build_tier2_prompt, build_tier3_prompt
        logger.info("✓ All imports successful")
        return True
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        return False


def test_config():
    """Test configuration values"""
    try:
        from lib.config import config
        
        # Check required config values
        assert config.model_id == "amazon.nova-micro-v1:0"
        assert config.region == "us-east-1"
        assert config.max_retries > 0
        assert config.max_seed_length > 0
        assert config.min_seed_length > 0
        
        logger.info("✓ Configuration values are valid")
        return True
    except Exception as e:
        logger.error(f"✗ Configuration error: {e}")
        return False


def test_prompts():
    """Test prompt generation"""
    try:
        from prompts.health_wellbeing_prompts import build_tier1_prompt, build_tier2_prompt, build_tier3_prompt
        
        # Test Tier 1 prompt
        tier1_prompt = build_tier1_prompt()
        assert len(tier1_prompt) > 100
        assert "tier1_categories" in tier1_prompt
        
        # Test Tier 2 prompt
        tier2_prompt = build_tier2_prompt("Fitness")
        assert len(tier2_prompt) > 100
        assert "Fitness" in tier2_prompt
        assert "tier2_items" in tier2_prompt
        
        # Test Tier 3 prompt
        tier3_prompt = build_tier3_prompt("Fitness", "Yoga", "youtube")
        assert len(tier3_prompt) > 100
        assert "Yoga" in tier3_prompt
        assert "search_seeds" in tier3_prompt
        
        logger.info("✓ Prompt generation working correctly")
        return True
    except Exception as e:
        logger.error(f"✗ Prompt generation error: {e}")
        return False


def test_output_directory():
    """Test output directory creation"""
    try:
        from lib.config import config
        from pathlib import Path
        
        output_dir = Path(config.get_output_dir())
        output_dir.mkdir(parents=True, exist_ok=True)
        
        assert output_dir.exists()
        logger.info(f"✓ Output directory created: {output_dir}")
        return True
    except Exception as e:
        logger.error(f"✗ Output directory error: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("Running setup tests...")
    
    tests = [
        test_imports,
        test_config,
        test_prompts,
        test_output_directory
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        logger.info("")
    
    logger.info("=" * 50)
    logger.info(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("✓ All tests passed! Setup is ready.")
        return 0
    else:
        logger.error("✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

