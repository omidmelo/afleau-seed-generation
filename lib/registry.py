"""
Prompt registry for dynamic category-based prompt loading
"""

import importlib
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PromptRegistry:
    """Registry for managing category-specific prompts"""
    
    def __init__(self):
        self._prompt_modules: Dict[str, Any] = {}
        self._available_categories = self._discover_categories()
    
    def _discover_categories(self) -> list:
        """Discover available categories by scanning for prompt files"""
        categories = []
        # Get the project root (parent of lib directory)
        project_root = Path(__file__).parent.parent
        prompts_dir = project_root / "prompts"
        
        # Look for prompt files in the prompts subdirectory
        for file_path in prompts_dir.glob("*_prompts.py"):
            category_name = file_path.stem.replace("_prompts", "")
            categories.append(category_name)
        
        logger.info(f"Discovered categories: {categories}")
        return categories
    
    def get_prompts(self, category: str):
        """Get prompt functions for a specific category"""
        if category not in self._prompt_modules:
            self._load_category_prompts(category)
        
        return self._prompt_modules.get(category)
    
    def _load_category_prompts(self, category: str):
        """Load prompt module for a specific category"""
        try:
            module_name = f"prompts.{category}_prompts"
            module = importlib.import_module(module_name)
            
            # Validate that the module has required functions
            required_functions = ['build_tier1_prompt', 'build_tier2_prompt', 'build_tier3_prompt']
            missing_functions = [func for func in required_functions if not hasattr(module, func)]
            
            if missing_functions:
                raise ImportError(f"Category '{category}' is missing required functions: {missing_functions}")
            
            self._prompt_modules[category] = module
            logger.info(f"Loaded prompts for category: {category}")
            
        except ImportError as e:
            logger.error(f"Failed to load prompts for category '{category}': {e}")
            raise ValueError(f"Category '{category}' not found or invalid. Available categories: {self._available_categories}")
    
    def get_available_categories(self) -> list:
        """Get list of available categories"""
        return self._available_categories.copy()
    
    def is_category_available(self, category: str) -> bool:
        """Check if a category is available"""
        return category in self._available_categories


# Global registry instance
prompt_registry = PromptRegistry()

