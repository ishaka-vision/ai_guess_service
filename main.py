from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import time
import traceback

import re

def clean_response(text):
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    cleaned = cleaned.strip()
    words = cleaned.split()
    if words:
        return words[-1].replace(".", "").lower()
    
    return cleaned

app = FastAPI()

class GuessRequest(BaseModel):
    description: str

stats = {
    "total_requests": 0,
    "total_time": 0.0,
    "average_time": 0.0
}

@app.get("/")
def home():
    return HTMLResponse(open("index.html").read())

@app.post("/guess")
def guess(request: GuessRequest):
    start_time = time.time()
    
    prompt = f"Answer in ONE WORD only. No explanation. What is this: {request.description}"
    
    try:
        print(f"[DEBUG] Attempting to connect to Ollama at http://localhost:11434")
        print(f"[DEBUG] Prompt: {prompt}")
        print(f"[DEBUG] Model: deepseek-r1:32b")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-r1:32b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        
        print(f"[DEBUG] Response status: {response.status_code}")
        response.raise_for_status()
        
        result = response.json()
        raw_text = result.get("response", "")
        guess_text = clean_response(raw_text)
        elapsed_time = time.time() - start_time
        
        print(f"[DEBUG] Success! Guess: {guess_text}, Time: {elapsed_time}s")
        
        stats["total_requests"] += 1
        stats["total_time"] += elapsed_time
        stats["average_time"] = stats["total_time"] / stats["total_requests"]
        
        return {
            "description": request.description,
            "guess": guess_text,
            "response_time_ms": round(elapsed_time * 1000, 2),
            "stats": stats
        }
        
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Connection error: Cannot reach Ollama at localhost:11434. Is the SSH tunnel active? Details: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return {
            "error": error_msg,
            "description": request.description
        }
        
    except requests.exceptions.Timeout as e:
        error_msg = f"Timeout: Ollama took too long to respond (120s). Server might be busy. Details: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return {
            "error": error_msg,
            "description": request.description
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Request error: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return {
            "error": error_msg,
            "description": request.description
        }
        
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return {
            "error": error_msg,
            "description": request.description
        }