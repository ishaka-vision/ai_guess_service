# AI Guess Service

A simple, distributed AI-powered web service that takes a description and guesses the object in a single word.

This project explores how a backend service can interact with a large language model on a separate machine while remaining simple, observable, and easy to extend.

## What it does

- Accepts a natural language description from a user
- Sends it to a large language model (DeepSeek-R1 via Ollama)
- Returns a **single-word guess**
- Measures response time and performance
- Tracks basic usage statistics

### Example

**Input:**
```json
{
  "description": "A furry animal with whiskers that purrs"
}
```

**Output:**
```json
{
  "guess": "cat"
}
```

## How it works

## How it works

### Architecture

```
Browser → FastAPI → SSH Tunnel → Remote Ollama → Response
```

The system follows a distributed architecture:

- **Frontend:** A minimal HTML/JavaScript interface that accepts descriptions and displays predictions
- **Backend:** A FastAPI service running locally
- **LLM:** DeepSeek-R1 running on a remote server (to avoid heavy local hardware requirements)
- **Connection:** SSH tunnel for secure communication between the backend and remote model

This separation makes it possible to work with large models without needing powerful local hardware.

## Design decisions

## Design decisions

I focused on clarity and incremental progress instead of building something overly complex:

**Start simple** — I avoided databases and frameworks initially to focus on getting the full pipeline working end-to-end.

**Use a remote model** — Running DeepSeek-R1 locally wasn't practical, so I used a remote server connected via SSH instead.

**SSH tunneling over direct deployment** — The simplest way to securely connect my local API to the remote LLM without changing infrastructure.

**Post-processing model output** — The model sometimes returns reasoning tokens (`<think>...</think>`), so I added a cleaning step to enforce a one-word answer.

**Basic observability** — I track response time and request count to understand system behavior and performance.

## How to run it
## How to run it

### 1. Clone the repository
```bash
git clone https://github.com/ishaka-vision/ai_guess_service.git
cd ai_guess_service
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Connect to the remote model (SSH tunnel)
```bash
ssh -L 11434:localhost:11434 agentic@<server-ip>
```
> This step is essential — it links your local API to the remote Ollama service.

### 5. Run the API
```bash
python -m uvicorn main:app --reload
```

### 6. Open in your browser
```
http://localhost:8000
```

## API

### POST /guess

**Request:**
```json
{
  "description": "A large grey animal with a trunk"
}
```

**Response:**
```json
{
  "description": "A large grey animal with a trunk",
  "guess": "elephant",
  "response_time_ms": 8979.33,
  "stats": {
    "total_requests": 2,
    "average_time": 16790
  }
}
```

## Limitations

## Limitations

- Response time can be high (10–30 seconds) due to model size
- No persistent storage (statistics reset on restart)
- Single-user / single-instance design
- Depends on an active SSH tunnel

## Future improvements

If I had more time, I would:

- Add persistent storage (Redis or database)
- Implement caching for repeated queries
- Reduce latency using smaller or optimized models
- Containerize and deploy fully (Docker/Kubernetes)
- Replace SSH tunneling with a proper service architecture

## Technologies used

- **Framework:** FastAPI
- **LLM Service:** Ollama
- **Model:** DeepSeek-R1 (32B)
- **Languages:** Python (requests, pydantic)
- **Networking:** SSH

## Author

Kelly Franck Ishaka

## License

MIT