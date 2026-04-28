# AI Guess Service

This project is a simple AI-powered web service that takes a short description and tries to guess the object in one word.

It was built as a small exploration of how a backend service can interact with a large language model running on a separate machine, while keeping the system simple, observable, and easy to extend.

---

##  What it does

- Accepts a natural language description from a user  
- Sends it to a large language model (DeepSeek-R1 via Ollama)  
- Returns a **single-word guess**  
- Measures how long the whole process takes  
- Keeps basic usage statistics  

Example:

**Input**
```json
{
  "description": "A furry animal with whiskers that purrs"
}

Output

{
  "guess": "cat"
}
 How it works (Architecture)

The system is intentionally simple but follows a distributed setup:

Browser → FastAPI → SSH Tunnel → Remote Ollama → Response

Frontend is a minimal HTML/JavaScript frontend that accepts user descriptions and displays model predictions. The interface emphasizes simplicity and human-readable feedback.
The backend is a FastAPI service running locally
The LLM runs on a remote server (to avoid heavy local setup)
An SSH tunnel connects the backend to the remote model securely

This separation made it possible to work with a large model without needing powerful local hardware.

 Design decisions

Instead of trying to build something complex, I focused on clarity and incremental progress:

Start simple
I avoided databases and frameworks at first to focus on getting the full pipeline working end-to-end.
Use a remote model
Running DeepSeek-R1 locally was not practical, so I used a remote server and connected via SSH.
SSH tunneling over direct deployment
This was the simplest way to securely connect my local API to the remote LLM without changing infrastructure.
Post-processing model output
The model sometimes returns reasoning (<think>...</think>), so I added a cleaning step to enforce a one-word answer.
Basic observability
I tracked response time and request count to understand system behavior and performance.

 How to run it
 
1. Clone the repository
git clone https://github.com/Kelly-Franck-Ishaka/ai-guess-service.git
cd ai-guess-service
2. Create and activate a virtual environment
python -m venv venv

On Windows:

venv\Scripts\activate

On Mac/Linux:

source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Connect to the remote model (SSH tunnel)
ssh -L 11434:localhost:11434 agentic@<server-ip>

This step is important — it links your local API to the remote Ollama service.

5. Run the API
python -m uvicorn main:app --reload
6. Open in your browser
http://localhost:8000
 API
POST /guess

Request

{
  "description": "A large grey animal with a trunk"
}

Response

{
  "description": "A large grey animal with a trunk",
  "guess": "elephant",
  "response_time_ms": 8979.33,
  "stats": {
    "total_requests": 2,
    "average_time": 16790
  }
}
 Limitations

Response time can be high (10–30 seconds) due to the model size
No persistent storage (statistics reset on restart)
Single-user / single-instance design
Depends on an active SSH tunnel
 What I would improve next

If I had more time, I would:

Add persistent storage (Redis or database)
Introduce caching for repeated queries
Reduce latency using smaller or optimized models
Containerize and deploy fully (Docker/Kubernetes)
Replace SSH tunneling with a proper service architecture

 Technologies used

FastAPI
Ollama
DeepSeek-R1 (32B)
Python (requests, pydantic)
SSH

 Author

Kelly Franck Ishaka

 License

MIT