import os
import json
import httpx
from typing import AsyncGenerator

class AIProvider:
    """Base class for AI Providers"""
    async def stream_chat(self, messages: list, model: str = None) -> AsyncGenerator[str, None]:
        raise NotImplementedError
        
    async def generate_chat(self, messages: list, model: str = None) -> str:
        raise NotImplementedError


class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.default_model = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")
        self.app_name = os.getenv("OPENROUTER_APP_NAME", "GitVision")
        self.site_url = os.getenv("OPENROUTER_SITE_URL", "")
        
    async def stream_chat(self, messages: list, model: str = None) -> AsyncGenerator[str, None]:
        if not self.api_key:
            yield json.dumps({"error": "OpenRouter API key is not configured."})
            return
            
        target_model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": True
        }
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60.0) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield json.dumps({"error": f"OpenRouter API Error: {response.status_code}"})
                        return
                        
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        yield json.dumps({"content": delta["content"]})
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield json.dumps({"error": f"Connection error: {str(e)}"})

    def stream_chat_sync(self, messages: list, model: str = None):
        if not self.api_key:
            yield json.dumps({"error": "OpenRouter API key is not configured."})
            return
            
        target_model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": True
        }
        
        try:
            with httpx.Client() as client:
                with client.stream("POST", f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60.0) as response:
                    if response.status_code != 200:
                        yield json.dumps({"error": f"OpenRouter API Error: {response.status_code}"})
                        return
                        
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data)
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    # Only stream actual content, skip reasoning/thinking tokens
                                    content = delta.get("content", "")
                                    if content and not delta.get("reasoning"):
                                        yield json.dumps({"content": content})
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            yield json.dumps({"error": f"Connection error: {str(e)}"})

    async def generate_chat(self, messages: list, model: str = None) -> str:
        if not self.api_key:
            raise Exception("OpenRouter API key is not configured.")
            
        target_model = model or self.default_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


def get_ai_provider() -> AIProvider:
    provider_type = os.getenv("AI_PROVIDER", "openrouter").lower()
    
    if provider_type == "openrouter":
        return OpenRouterProvider()
    
    # Fallback to OpenRouter as default for Phase 1
    return OpenRouterProvider()
