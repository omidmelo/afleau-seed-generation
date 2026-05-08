"""
Bedrock client for data generation
"""

import json
import boto3
import asyncio
from typing import Dict, Any, Optional, Tuple
from botocore.exceptions import ClientError, BotoCoreError
import logging

from lib.base_client import LLMClient, LLMError

logger = logging.getLogger(__name__)

# Approximate USD pricing per 1M tokens.
# Update these values as provider pricing changes.
MODEL_PRICING_PER_1M_TOKENS = {
    "us.anthropic.claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "global.anthropic.claude-haiku-4-5-20251001-v1:0": {"input": 1.00, "output": 5.00},
    "amazon.nova-micro-v1:0": {"input": 0.035, "output": 0.14},
}


class BedrockClient(LLMClient):
    """Bedrock client wrapper for data generation"""
    
    def __init__(self, region: str = "us-east-1"):
        self.region = region
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def _extract_usage_tokens(self, response: Dict[str, Any], response_body: Dict[str, Any]) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """Extract input/output/total token usage from Bedrock response."""
        usage = response_body.get("usage", {}) if isinstance(response_body, dict) else {}

        input_tokens = usage.get("input_tokens")
        if input_tokens is None:
            input_tokens = usage.get("inputTokens")

        output_tokens = usage.get("output_tokens")
        if output_tokens is None:
            output_tokens = usage.get("outputTokens")

        total_tokens = usage.get("total_tokens")
        if total_tokens is None:
            total_tokens = usage.get("totalTokens")

        # Fallback to Bedrock headers when body usage is absent.
        headers = response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
        if input_tokens is None:
            header_val = headers.get("x-amzn-bedrock-input-token-count")
            if header_val is not None:
                input_tokens = int(header_val)
        if output_tokens is None:
            header_val = headers.get("x-amzn-bedrock-output-token-count")
            if header_val is not None:
                output_tokens = int(header_val)

        if total_tokens is None and input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens

        return input_tokens, output_tokens, total_tokens

    def _estimate_cost_usd(self, model_id: str, input_tokens: Optional[int], output_tokens: Optional[int]) -> Optional[float]:
        """Estimate invocation cost in USD from token counts."""
        pricing = MODEL_PRICING_PER_1M_TOKENS.get(model_id)
        if pricing is None or input_tokens is None or output_tokens is None:
            return None

        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
    
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
            model_id: Bedrock model ID (e.g., "amazon.nova-micro-v1:0" or "us.anthropic.claude-sonnet-4-6")
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
        # Bedrock supports multiple model providers that do not share the exact same
        # request schema. In particular, Anthropic models on Bedrock use the
        # Anthropic Messages schema (snake_case fields like max_tokens).
        is_anthropic = model_id.startswith("us.anthropic.") or ".anthropic." in model_id

        if is_anthropic:
            # Anthropic Messages API (Bedrock) schema
            # Note: some Anthropic Bedrock model versions reject specifying both
            # temperature and top_p simultaneously. We prefer temperature and
            # omit top_p in that case.
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        else:
            # Bedrock "converse/messages" style schema (e.g. Nova)
            request_body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    "topP": top_p,
                },
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
                
                # Handle different response formats across providers
                content = None
                if "output" in response_body and "message" in response_body["output"]:
                    # Standard format
                    content = response_body["output"]["message"]["content"][0]["text"]
                elif "content" in response_body and isinstance(response_body["content"], list):
                    # Anthropic-on-Bedrock format:
                    # { "content": [{"type":"text","text":"..."}], ... }
                    text_parts = []
                    for block in response_body["content"]:
                        if isinstance(block, dict) and block.get("type") == "text":
                            t = block.get("text")
                            if isinstance(t, str) and t.strip():
                                text_parts.append(t)
                    if text_parts:
                        content = "\n".join(text_parts)
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
                
                # Clean the content — remove markdown code blocks if present
                # _clean_response is inherited from LLMClient base class
                clean_content = self._clean_response(content)

                # Log token usage + rough cost estimate for terminal visibility.
                input_tokens, output_tokens, total_tokens = self._extract_usage_tokens(response, response_body)
                estimated_cost_usd = self._estimate_cost_usd(model_id, input_tokens, output_tokens)
                logger.info(
                    "Usage — input_tokens=%s output_tokens=%s total_tokens=%s estimated_cost_usd=%s",
                    input_tokens if input_tokens is not None else "n/a",
                    output_tokens if output_tokens is not None else "n/a",
                    total_tokens if total_tokens is not None else "n/a",
                    f"{estimated_cost_usd:.6f}" if estimated_cost_usd is not None else "n/a",
                )
                
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
    
class BedrockError(LLMError):
    """Exception raised when Bedrock API calls fail after all retries."""
    pass

