"""
Bedrock client for data generation
"""

import json
import boto3
import asyncio
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, BotoCoreError
import logging

logger = logging.getLogger(__name__)


class BedrockClient:
    """Bedrock client wrapper for data generation"""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = boto3.client("bedrock-runtime", region_name=region)
    
    async def invoke_model(
        self,
        model_id: str,
        prompt: str,
        temperature: float = 0.1,
        top_p: float = 0.9,
        max_tokens: int = 4000,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Invoke Bedrock model with retry logic
        
        Args:
            model_id: Bedrock model ID (e.g., "amazon.nova-micro-v1:0")
            prompt: Input prompt
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate
            max_retries: Number of retry attempts
            
        Returns:
            Parsed response from Bedrock
            
        Raises:
            BedrockError: If all retries fail
        """
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p
            }
        }
        
        last_error = None
        for attempt in range(max_retries):
            try:
                logger.info(f"Invoking Bedrock model {model_id} (attempt {attempt + 1}/{max_retries})")
                
                response = self.client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(request_body)
                )
                
                # Parse the response
                response_body = json.loads(response["body"].read())
                logger.debug(f"Raw response body: {response_body}")
                
                # Handle different response formats
                content = None
                if "output" in response_body and "message" in response_body["output"]:
                    # Standard format
                    content = response_body["output"]["message"]["content"][0]["text"]
                elif "completion" in response_body:
                    # Alternative format
                    content = response_body["completion"]
                elif "text" in response_body:
                    # Another alternative format
                    content = response_body["text"]
                else:
                    logger.error(f"Unexpected response format: {response_body}")
                    raise BedrockError(f"Unexpected response format from Bedrock")
                
                if content is None:
                    logger.error("Content is None after parsing response")
                    raise BedrockError("Empty content in Bedrock response")
                
                # Clean the content - remove markdown code blocks if present
                clean_content = self._clean_response(content)
                
                logger.info(f"Bedrock model {model_id} responded successfully")
                return {
                    "content": clean_content,
                    "raw_response": response_body,
                    "model_id": model_id,
                    "attempt": attempt + 1
                }
                
            except (ClientError, BotoCoreError) as e:
                last_error = e
                logger.warning(f"Bedrock invocation failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                
                if attempt < max_retries - 1:
                    # Wait before retry (exponential backoff)
                    await asyncio.sleep(2 ** attempt)
                else:
                    logger.error(f"All Bedrock retry attempts failed: {str(e)}")
                    raise BedrockError(f"Bedrock invocation failed after {max_retries} attempts: {str(e)}") from e
        
        raise BedrockError(f"Bedrock invocation failed: {str(last_error)}") from last_error
    
    def _clean_response(self, content: str) -> str:
        """Clean response content by removing markdown code blocks"""
        clean_content = content.strip()
        if clean_content.startswith('```json'):
            clean_content = clean_content[7:]  # Remove ```json
        if clean_content.endswith('```'):
            clean_content = clean_content[:-3]  # Remove ```
        return clean_content.strip()


class BedrockError(Exception):
    """Custom exception for Bedrock-related errors"""
    pass

