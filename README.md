# Runpod Agent Node

A lightweight, container-friendly autonomous agent runtime designed for GPU infrastructure (Runpod, Kubernetes, or any Docker host).

This project provides a **persistent agent execution node** that exposes a simple HTTP interface for task execution and supports:

* Local or remote model backends
* CLI interaction
* HTTP API interaction
* File-based task queues
* Continuous watcher mode
* Artifact logging
* Container deployment
* Horizontal scaling

It is designed to function as a **modular building block for distributed agent systems**, orchestration layers, or research automation environments.

---

# Core Concept

This system separates **task orchestration** from **model inference**.

```
User / System
     │
     ▼
Agent Node (this repo)
     │
     ▼
Model Backend (local or remote)
```

The agent node handles:

* input routing
* task formatting
* request execution
* response storage
* workflow integration

The model backend handles:

* actual inference
* reasoning
* generation

This separation makes the node reusable across different models, providers, and architectures.

---

# Features

## Runtime Modes

### 1. HTTP Server Mode

Expose an inference endpoint:

```
POST /generate
```

This is the primary interaction interface.

---

### 2. CLI Task Execution

Submit tasks directly from shell:

```
python scripts/task_runner.py "analyze market trends"
```

---

### 3. File Queue Mode (Autonomous Loop)

Drop text files into:

```
tasks/incoming/
```

Agent processes them automatically and writes results to:

```
tasks/outgoing/
```

---

### 4. Docker / Runpod Deployment

Runs as a persistent container with exposed port.

---

# Architecture

```
runpod-agent-node/
│
├── src/
│   ├── server.py        FastAPI agent interface
│   ├── client.py        HTTP request wrapper
│   ├── watcher.py       task queue processor
│   ├── config.py        environment configuration
│   └── utils.py         helper utilities
│
├── scripts/
│   ├── serve_local.py   start agent server
│   ├── task_runner.py   CLI interaction
│   └── watch_tasks.py   autonomous loop
│
├── tasks/
│   ├── incoming/
│   └── outgoing/
│
├── artifacts/
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Installation

## Local Python Environment

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Docker

```
docker build -t runpod-agent .
docker run -p 8000:8000 runpod-agent
```

---

## Docker Compose

```
cp .env.example .env
docker compose up --build
```

---

# Running the Agent

## Start HTTP Server

```
python scripts/serve_local.py
```

Server default:

```
http://localhost:8000
```

---

## Submit Task (CLI)

```
python scripts/task_runner.py "summarize latest AI research"
```

Save result:

```
python scripts/task_runner.py \
  --out artifacts/result.json \
  "market analysis"
```

---

## Submit Task (HTTP)

```
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "hello",
    "max_tokens": 200,
    "temperature": 0.2
  }'
```

---

## Start Autonomous File Watcher

```
python scripts/watch_tasks.py
```

Then drop a task:

```
echo "write a poem about entropy" > tasks/incoming/task1.txt
```

Result appears:

```
tasks/outgoing/task1.json
```

---

# API Specification

## POST /generate

### Request

```
{
  "prompt": string,
  "max_tokens": integer,
  "temperature": float
}
```

### Response

```
{
  "text": string,
  "meta": object
}
```

---

## GET /ping

Health check.

---

# Environment Configuration

Copy `.env.example` → `.env`.

| Variable       | Purpose                   |
| -------------- | ------------------------- |
| AGENT_HOST     | bind address              |
| AGENT_PORT     | server port               |
| BACKEND_URL    | external model server     |
| LOCAL_LLM_URL  | CLI target endpoint       |
| MAX_TOKENS     | default generation length |
| TEMPERATURE    | default sampling          |
| TASKS_INCOMING | queue input path          |
| TASKS_OUTGOING | queue output path         |

---

# Connecting a Real Model Backend

By default, the server includes a simple built-in stub engine.

To connect a real model:

```
BACKEND_URL=http://your-model-server:port
```

The agent will forward:

```
POST /generate
```

to:

```
<BACKEND_URL>/generate
```

---

# Runpod Deployment

## Recommended Setup

1. Build container
2. Expose port 8000
3. Persistent volume mounted at:

```
/workspace/tasks
/workspace/artifacts
```

4. Start command:

```
python scripts/serve_local.py
```

---

## Interacting from Outside Runpod

```
curl http://<RUNPOD_PUBLIC_IP>:8000/generate
```

Or use Runpod proxy URL.

---

# Scaling Architecture

Multiple agent nodes can run simultaneously:

```
Load Balancer
      │
 ┌────┼────┐
 │    │    │
Agent Agent Agent
```

Each node statelessly forwards tasks to model backend.

---

# Security Notes

For production deployment:

* add authentication middleware
* restrict exposed ports
* validate prompt size
* rate limit requests
* isolate model backend network

---

# Logging and Artifacts

All outputs can be persisted to:

```
artifacts/
```

Queue processing automatically writes structured JSON.

---

# Extending the System

Possible extensions:

* memory layer
* multi-agent routing
* priority queues
* distributed task scheduler
* streaming responses
* tool calling
* vector retrieval
* workflow graphs

---

# Typical Use Cases

* research automation
* distributed inference nodes
* agent swarms
* lead generation systems
* monitoring bots
* experiment orchestration
* enterprise task routing

---

# Troubleshooting

## Connection refused

Server not running or wrong port.

## Empty responses

Backend not configured.

## Tasks not processed

Watcher not running.

## Container unreachable

Port not exposed in Runpod.

---

# License

MIT License

---

# Contributing

Pull requests welcome.

Suggested contribution areas:

* streaming support
* GPU memory management
* async batching
* orchestration adapters

---

# Philosophy

This project treats agents as **infrastructure primitives**.

Not applications.
Not chatbots.

Execution nodes.

Composable. Replaceable. Scalable.


Just say the word.
