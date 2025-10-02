"""
Health & Wellbeing data generator service
Main service class with CSV checkpointing and resumability
"""

import json
import csv
import os
import hashlib
import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Set
from pathlib import Path

from bedrock_client_adapted import BedrockClient, BedrockError
from health_wellbeing_config import config
from health_wellbeing_prompts import build_tier1_prompt, build_tier2_prompt, build_tier3_prompt

logger = logging.getLogger(__name__)


class HealthWellbeingDataGenerator:
    """Main service for generating Health & Wellbeing hierarchical data"""
    
    def __init__(self, bedrock_client: BedrockClient):
        self.client = bedrock_client
        self.config = config
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # File paths
        self.tier1_file = self.output_dir / self.config.tier1_filename
        
        # Aggregated file paths
        self.tier2_aggregated_file = self.output_dir / "all_tier2.csv"
        self.tier3_aggregated_file = self.output_dir / "all_tier3.csv"
        
        # Deduplication tracking
        self.seed_hashes: Set[str] = set()
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a name to be used as a filename"""
        # Replace spaces with underscores and remove special characters
        sanitized = re.sub(r'[^\w\s-]', '', name)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.strip('_').lower()
    
    async def generate_all_data(self) -> Dict[str, Any]:
        """Generate all three tiers of data with checkpointing"""
        logger.info("Starting Health & Wellbeing data generation")
        
        results = {
            "tier1_count": 0,
            "tier2_count": 0,
            "tier3_count": 0,
            "errors": []
        }
        
        try:
            # Step 1: Generate Tier 1
            tier1_data = await self.generate_tier1()
            results["tier1_count"] = len(tier1_data)
            logger.info(f"Generated {len(tier1_data)} Tier 1 categories")
            
            # Step 2: Generate Tier 2
            tier2_data = await self.generate_tier2()
            results["tier2_count"] = len(tier2_data)
            logger.info(f"Generated {len(tier2_data)} Tier 2 items")
            
            # Step 3: Generate Tier 3
            tier3_data = await self.generate_tier3()
            results["tier3_count"] = len(tier3_data)
            logger.info(f"Generated {len(tier3_data)} Tier 3 seeds")
            
        except Exception as e:
            logger.error(f"Error in data generation: {e}")
            results["errors"].append(str(e))
        
        return results
    
    async def generate_tier1(self) -> List[str]:
        """Generate Tier 1 categories"""
        if self.tier1_file.exists():
            logger.info("Tier 1 file exists, loading from checkpoint")
            return self._load_tier1_from_file()
        
        logger.info("Generating Tier 1 categories")
        prompt = build_tier1_prompt()
        
        try:
            response = await self.client.invoke_model(
                model_id=self.config.model_id,
                prompt=prompt,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                max_tokens=self.config.max_tokens,
                max_retries=self.config.max_retries
            )
            
            # Parse JSON response
            data = json.loads(response["content"])
            tier1_categories = data.get("tier1_categories", [])
            
            # Save to file
            self._save_tier1_to_file(tier1_categories)
            logger.info(f"Generated and saved {len(tier1_categories)} Tier 1 categories")
            
            return tier1_categories
            
        except Exception as e:
            logger.error(f"Error generating Tier 1: {e}")
            raise BedrockError(f"Tier 1 generation failed: {e}") from e
    
    async def generate_tier2(self) -> List[Dict[str, Any]]:
        """Generate Tier 2 items for each Tier 1 category"""
        # Load Tier 1 data
        tier1_data = await self.generate_tier1()
        
        all_tier2_data = []
        
        # Process each Tier 1 category
        for tier1_name in tier1_data:
            tier2_filename = f"tier2_{self._sanitize_filename(tier1_name)}.csv"
            tier2_file_path = self.output_dir / tier2_filename
            
            # Check if this Tier 2 file already exists
            if tier2_file_path.exists():
                logger.info(f"Tier 2 file exists for '{tier1_name}', loading from checkpoint")
                tier2_data = self._load_tier2_from_file(tier2_file_path)
                all_tier2_data.extend(tier2_data)
                continue
            
            try:
                # Generate Tier 2 data for this category
                tier2_data = await self._generate_tier2_for_category(tier1_name)
                
                # Save to separate file
                self._save_tier2_to_file(tier2_data, tier2_file_path)
                all_tier2_data.extend(tier2_data)
                
                logger.info(f"Generated Tier 2 for '{tier1_name}' - {len(tier2_data)} items")
                
            except Exception as e:
                logger.error(f"Error generating Tier 2 for '{tier1_name}': {e}")
                continue
        
        # Create aggregated Tier 2 file
        self._create_aggregated_tier2_file(all_tier2_data)
        
        return all_tier2_data
    
    async def _generate_tier2_for_category(self, tier1_name: str) -> List[Dict[str, Any]]:
        """Generate Tier 2 items for a specific Tier 1 category"""
        prompt = build_tier2_prompt(tier1_name)
        
        response = await self.client.invoke_model(
            model_id=self.config.model_id,
            prompt=prompt,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            max_tokens=self.config.max_tokens,
            max_retries=self.config.max_retries
        )
        
        # Parse JSON response
        data = json.loads(response["content"])
        tier2_items = data.get("tier2_items", [])
        
        # Add Tier 1 context to each Tier 2 item
        result = []
        for item in tier2_items:
            result.append({
                "tier1_name": tier1_name,
                "tier2_name": item
            })
        
        return result
    
    async def generate_tier3(self) -> List[Dict[str, Any]]:
        """Generate Tier 3 seeds for each Tier 2 item"""
        # Load Tier 2 data
        tier2_data = await self.generate_tier2()
        
        all_tier3_data = []
        
        # Process each Tier 2 item
        for tier2_item in tier2_data:
            tier1_name = tier2_item["tier1_name"]
            tier2_name = tier2_item["tier2_name"]
            
            tier3_filename = f"tier3_{self._sanitize_filename(tier2_name)}.csv"
            tier3_file_path = self.output_dir / tier3_filename
            
            # Check if this Tier 3 file already exists
            if tier3_file_path.exists():
                logger.info(f"Tier 3 file exists for '{tier2_name}', loading from checkpoint")
                tier3_data = self._load_tier3_from_file(tier3_file_path)
                all_tier3_data.extend(tier3_data)
                continue
            
            try:
                # Generate Tier 3 data for this item
                tier3_data = await self._generate_tier3_for_item(tier2_item)
                
                # Apply deduplication and safety filters
                filtered_seeds = self._filter_tier3_seeds(tier3_data)
                
                # Save to separate file
                self._save_tier3_to_file(filtered_seeds, tier3_file_path)
                all_tier3_data.extend(filtered_seeds)
                
                logger.info(f"Generated Tier 3 for '{tier2_name}' - {len(filtered_seeds)} seeds")
                
            except Exception as e:
                logger.error(f"Error generating Tier 3 for '{tier2_name}': {e}")
                continue
        
        # Create aggregated Tier 3 file
        self._create_aggregated_tier3_file(all_tier3_data)
        
        return all_tier3_data
    
    async def _generate_tier3_for_item(self, tier2_item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate Tier 3 seeds for a specific Tier 2 item"""
        prompt = build_tier3_prompt(
            tier2_item["tier1_name"],
            tier2_item["tier2_name"]
        )
        
        response = await self.client.invoke_model(
            model_id=self.config.model_id,
            prompt=prompt,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            max_tokens=self.config.max_tokens,
            max_retries=self.config.max_retries
        )
        
        # Parse JSON response
        data = json.loads(response["content"])
        seeds = data.get("search_seeds", [])
        
        # Add Tier 1 and Tier 2 context to each seed
        result = []
        for seed_text in seeds:
            result.append({
                "tier1_name": tier2_item["tier1_name"],
                "tier2_name": tier2_item["tier2_name"],
                "seed_text": seed_text
            })
        
        return result
    
    def _filter_tier3_seeds(self, seeds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply deduplication and safety filters to Tier 3 seeds"""
        filtered_seeds = []
        
        for seed in seeds:
            seed_text = seed.get("seed_text", "").strip()
            
            # Length validation
            if len(seed_text) < self.config.min_seed_length or len(seed_text) > self.config.max_seed_length:
                continue
            
            # Deduplication check
            seed_hash = hashlib.md5(seed_text.lower().encode()).hexdigest()
            if seed_hash in self.seed_hashes:
                continue
            
            # Safety filter (basic check for medical advice)
            if self._contains_unsafe_content(seed_text):
                continue
            
            self.seed_hashes.add(seed_hash)
            filtered_seeds.append(seed)
        
        return filtered_seeds
    
    def _contains_unsafe_content(self, text: str) -> bool:
        """Check if text contains potentially unsafe medical content"""
        unsafe_patterns = [
            "diagnose", "prescription", "medical advice", "cure", "treat",
            "doctor", "physician", "clinical", "symptoms", "disease",
            "medication", "drug", "therapy", "treatment"
        ]
        
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in unsafe_patterns)
    
    def _save_tier1_to_file(self, data: List[str]):
        """Save Tier 1 data to JSON file"""
        with open(self.tier1_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_tier1_from_file(self) -> List[str]:
        """Load Tier 1 data from JSON file"""
        with open(self.tier1_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_tier2_to_file(self, data: List[Dict[str, Any]], file_path: Path):
        """Save Tier 2 data to CSV file"""
        if not data:
            return
        
        fieldnames = ["tier1_name", "tier2_name"]
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "tier1_name": item["tier1_name"],
                    "tier2_name": item["tier2_name"]
                })
    
    def _load_tier2_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load Tier 2 data from CSV file"""
        if not file_path.exists():
            return []
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "tier1_name": row["tier1_name"],
                    "tier2_name": row["tier2_name"]
                })
        return data
    
    def _save_tier3_to_file(self, data: List[Dict[str, Any]], file_path: Path):
        """Save Tier 3 data to CSV file"""
        if not data:
            return
        
        fieldnames = ["tier1_name", "tier2_name", "seed_text"]
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "tier1_name": item["tier1_name"],
                    "tier2_name": item["tier2_name"],
                    "seed_text": item["seed_text"]
                })
    
    def _load_tier3_from_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load Tier 3 data from CSV file"""
        if not file_path.exists():
            return []
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "tier1_name": row["tier1_name"],
                    "tier2_name": row["tier2_name"],
                    "seed_text": row["seed_text"]
                })
        return data
    
    def _create_aggregated_tier2_file(self, all_tier2_data: List[Dict[str, Any]]):
        """Create aggregated Tier 2 CSV file with all data"""
        if not all_tier2_data:
            return
        
        logger.info(f"Creating aggregated Tier 2 file with {len(all_tier2_data)} items")
        
        fieldnames = ["tier1_name", "tier2_name"]
        with open(self.tier2_aggregated_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in all_tier2_data:
                writer.writerow({
                    "tier1_name": item["tier1_name"],
                    "tier2_name": item["tier2_name"]
                })
        
        logger.info(f"Aggregated Tier 2 file saved: {self.tier2_aggregated_file}")
    
    def _create_aggregated_tier3_file(self, all_tier3_data: List[Dict[str, Any]]):
        """Create aggregated Tier 3 CSV file with all data"""
        if not all_tier3_data:
            return
        
        logger.info(f"Creating aggregated Tier 3 file with {len(all_tier3_data)} seeds")
        
        fieldnames = ["tier1_name", "tier2_name", "seed_text"]
        with open(self.tier3_aggregated_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in all_tier3_data:
                writer.writerow({
                    "tier1_name": item["tier1_name"],
                    "tier2_name": item["tier2_name"],
                    "seed_text": item["seed_text"]
                })
        
        logger.info(f"Aggregated Tier 3 file saved: {self.tier3_aggregated_file}")
