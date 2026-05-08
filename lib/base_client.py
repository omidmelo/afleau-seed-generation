"""
Abstract base class and shared error type for LLM clients.
Defines the common interface that all provider clients must implement,
allowing DataGenerator to remain provider-agnostic.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMError(Exception):
    """
    Base exception for all LLM provider errors.
    Both BedrockError and ClaudeError inherit from this,
    so callers only need to catch LLMError regardless of provider.
    """
    pass


class LLMClient(ABC):
    """
    Abstract base class for LLM provider clients.

    All providers (Bedrock, Claude API, etc.) must implement invoke_model()
    with this exact signature and return contract so DataGenerator can
    switch between providers transparently.
    """

    @abstractmethod
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
        Invoke the LLM with a prompt and return the cleaned text response.

        Args:
            model_id:    Provider-specific model identifier
            prompt:      Input prompt string
            temperature: Sampling temperature (0.0 - 1.0)
            top_p:       Nucleus sampling parameter (0.0 - 1.0)
            max_tokens:  Maximum tokens to generate
            max_retries: Number of retry attempts on failure

        Returns:
            Dict containing at minimum:
                "content" (str): Cleaned text response from the model
                "model_id" (str): Model used
                "attempt" (int): Which attempt succeeded (1-based)

        Raises:
            LLMError: If all retry attempts fail
        """
        pass

    def _clean_response(self, content: str) -> str:
        """
        Strip markdown code fences from model responses.
        Shared utility used by all provider implementations.
        """
        clean = content.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return clean.strip()
