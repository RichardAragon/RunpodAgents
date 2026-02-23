import os
import requests
from typing import Any, Dict, Optional

DEFAULT_API_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:8000/generate")

def call_generate(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.2,
    api_url: Optional[str] = None,
    timeout_s: int = 1200,
) -> Dict[str, Any]:
    url = api_url or DEFAULT_API_URL
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    r = requests.post(url, json=payload, timeout=timeout_s)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, dict):
        raise ValueError("Server returned non-JSON-object response")
    return data
