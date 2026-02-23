import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # Server
    host: str = Field(default_factory=lambda: os.getenv("AGENT_HOST", "0.0.0.0"))
    port: int = Field(default_factory=lambda: int(os.getenv("AGENT_PORT", "8000")))

    # LLM endpoint your agent calls (can be a local model server, OpenAI-compatible server, etc.)
    # In your current setup this is usually http://localhost:8000/generate (agent server itself),
    # but you can point it at another backend if you want.
    backend_url: str = Field(default_factory=lambda: os.getenv("BACKEND_URL", "").strip())

    # Behavior
    default_max_tokens: int = Field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "512")))
    default_temperature: float = Field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.2")))
    request_timeout_s: int = Field(default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT_S", "1200")))

    # Task folders (optional)
    tasks_incoming: str = Field(default_factory=lambda: os.getenv("TASKS_INCOMING", "tasks/incoming"))
    tasks_outgoing: str = Field(default_factory=lambda: os.getenv("TASKS_OUTGOING", "tasks/outgoing"))
    artifacts_dir: str = Field(default_factory=lambda: os.getenv("ARTIFACTS_DIR", "artifacts"))

settings = Settings()
