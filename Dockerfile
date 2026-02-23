FROM python:3.11-slim

WORKDIR /app

# System deps (optional but helpful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts
COPY README.md ./
COPY .env.example ./

EXPOSE 8000

# Start API server by default
CMD ["python", "scripts/serve_local.py"]
