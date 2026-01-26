from __future__ import annotations
import os, json
from typing import Optional, Dict, Any
import httpx

# Minimal, provider-agnostic client. Fill in base URLs per your provider.
# By default, attempts OpenAI-compatible /chat/completions.
class LLMClient:
    def __init__(self, model: str, temperature: float = 0.1, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.model = model
        self.temperature = temperature
        self.base_url = base_url or os.getenv("LLM_BASE_URL","https://api.openai.com/v1")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER","openai")

    async def chat(self, system: str, user: str, max_tokens: int = 600) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": max_tokens,
            "messages": [{"role":"system","content":system},{"role":"user","content":user}]
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        # OpenAI-compatible shape
        return data["choices"][0]["message"]["content"]

def parse_llm_json(s: str) -> Dict[str, Any]:
    # Attempt to recover JSON even if model added text; be strict first.
    try:
        return json.loads(s)
    except Exception:
        # Fallback: find first/last braces
        start = s.find("{")
        end = s.rfind("}")
        if start >= 0 and end > start:
            return json.loads(s[start:end+1])
        raise
