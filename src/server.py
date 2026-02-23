from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import requests

from .config import settings

app = FastAPI(title="Runpod Agent Node", version="1.0.0")

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    max_tokens: int = Field(default=settings.default_max_tokens, ge=1, le=8192)
    temperature: float = Field(default=settings.default_temperature, ge=0.0, le=2.0)

class GenerateResponse(BaseModel):
    text: str
    meta: Dict[str, Any] = {}

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    # If user points BACKEND_URL to a separate LLM server, forward requests there.
    if settings.backend_url:
        try:
            r = requests.post(
                settings.backend_url.rstrip("/") + "/generate",
                json=req.model_dump(),
                timeout=settings.request_timeout_s,
            )
            r.raise_for_status()
            data = r.json()
            # accept either {"text": "..."} or {"response": "..."} etc.
            text = data.get("text") or data.get("response") or data.get("output")
            if not text:
                raise HTTPException(status_code=502, detail=f"Backend response missing text field: {data}")
            return GenerateResponse(text=text, meta={"forwarded_to": settings.backend_url})
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail=f"Backend request failed: {e}")

    # Built-in minimal “engine” for smoke tests / placeholder.
    # Replace with your real model call if desired.
    # This intentionally does NOT pretend to be a full LLM.
    prompt = req.prompt.strip()
    text = (
        "Agent Node is running.\n\n"
        f"Received prompt:\n{prompt}\n\n"
        "To connect a real model, set BACKEND_URL to your model server base URL."
    )
    return GenerateResponse(text=text, meta={"engine": "builtin_stub"})
