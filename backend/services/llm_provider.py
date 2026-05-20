"""
LLM Provider Abstraction.
Supports switching between Ollama (local) and external APIs.
"""

import httpx
import os
from typing import Any


class LLMProvider:
    """Unified interface for calling different LLM providers."""

    PROVIDERS = {
        "ollama": {
            "base_url": os.getenv("OLLAMA_URL", "http://ollama:11434"),
            "model": os.getenv("OLLAMA_MODEL", "qwen2.5:14b"),
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
            "api_key_env": "OPENAI_API_KEY",
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com/v1",
            "model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            "api_key_env": "ANTHROPIC_API_KEY",
        },
        "groq": {
            "base_url": "https://api.groq.com/openai/v1",
            "model": os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
            "api_key_env": "GROQ_API_KEY",
        },
    }

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> str:
        """Send chat completion request to the configured LLM provider."""
        if self.provider == "ollama":
            return await self._call_ollama(messages, temperature, max_tokens)
        elif self.provider == "anthropic":
            return await self._call_anthropic(messages, temperature, max_tokens)
        else:
            # OpenAI-compatible (openai, groq)
            return await self._call_openai_compatible(messages, temperature, max_tokens)

    async def embed(self, text: str) -> list[float]:
        """Generate embedding vector for text."""
        config = self.PROVIDERS["ollama"]
        url = f"{config['base_url']}/api/embeddings"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json={
                "model": "nomic-embed-text",
                "prompt": text,
            })
            response.raise_for_status()
            return response.json()["embedding"]

    async def _call_ollama(self, messages, temperature, max_tokens) -> str:
        config = self.PROVIDERS["ollama"]
        url = f"{config['base_url']}/api/chat"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json={
                "model": config["model"],
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            })
            response.raise_for_status()
            return response.json()["message"]["content"]

    async def _call_openai_compatible(self, messages, temperature, max_tokens) -> str:
        config = self.PROVIDERS[self.provider]
        api_key = os.getenv(config.get("api_key_env", ""), "")
        url = f"{config['base_url']}/chat/completions"

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": config["model"],
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def _call_anthropic(self, messages, temperature, max_tokens) -> str:
        config = self.PROVIDERS["anthropic"]
        api_key = os.getenv(config.get("api_key_env", ""), "")
        url = f"{config['base_url']}/messages"

        # Convert messages format for Anthropic
        system_msg = ""
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                user_messages.append(msg)

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": config["model"],
                    "system": system_msg,
                    "messages": user_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]


# Singleton instance
llm = LLMProvider()
