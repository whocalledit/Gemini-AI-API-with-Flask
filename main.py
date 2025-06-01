from pathlib import Path
import hashlib
import json
import os
from datetime import datetime
from typing import Optional, Literal

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import base64
import threading
from dotenv import load_dotenv

# Load .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in environment.")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# FastAPI app
app = FastAPI()
lock = threading.Lock()

# Create required directories
CACHE_DIR = Path("cache")
IMAGES_DIR = CACHE_DIR / "images"
LOGS_DIR = CACHE_DIR / "logs"
for d in [IMAGES_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

QUERIES_LOG = LOGS_DIR / "queries.json"
RESPONSES_LOG = LOGS_DIR / "responses.json"
ERRORS_LOG = LOGS_DIR / "errors.json"
for log in [QUERIES_LOG, RESPONSES_LOG, ERRORS_LOG]:
    if not log.exists():
        log.write_text("[]")

# Input schema
class AIRequest(BaseModel):
    task: Literal["code_explain", "idea_generator", "image_caption", "tone_detector"]
    input: str
    extra_params: Optional[dict] = None

# Helpers
def get_timestamp():
    return datetime.utcnow().isoformat()

def sha256_hash(task: str, input_data: str):
    return hashlib.sha256(f"{task}_{input_data}".encode()).hexdigest()

def append_json_log(filepath: Path, entry: dict):
    with lock:
        try:
            data = json.loads(filepath.read_text())
        except json.JSONDecodeError:
            data = []
        data.append(entry)
        filepath.write_text(json.dumps(data, indent=2))

async def query_gemini(prompt: str) -> str:
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Gemini API error {response.status_code}: {response.text}")
        output = response.json()
        return output["candidates"][0]["content"]["parts"][0]["text"]

def process_image_input(input_str: str) -> str:
    filename = f"{get_timestamp().replace(':', '-')}.jpg"
    filepath = IMAGES_DIR / filename
    if input_str.startswith("http"):
        response = httpx.get(input_str)
        image = Image.open(BytesIO(response.content))
    else:
        image_data = base64.b64decode(input_str)
        image = Image.open(BytesIO(image_data))
    image.save(filepath)
    return str(filepath)

def generate_prompt(task: str, input_data: str) -> str:
    if task == "code_explain":
        return f"Explain the following code in plain English:\n\n{input_data}"
    elif task == "idea_generator":
        return f"Generate creative startup ideas for:\n\n{input_data}"
    elif task == "tone_detector":
        return f"Analyze the emotional tone of this text:\n\n{input_data}"
    elif task == "image_caption":
        return f"Describe this image: {input_data}"
    return input_data

# Main endpoint
@app.post("/ai-multitool")
async def ai_multitool(request: AIRequest):
    timestamp = get_timestamp()
    input_hash = sha256_hash(request.task, request.input)

    # Check for cache
    try:
        cached = json.loads(RESPONSES_LOG.read_text())
        for item in cached:
            if sha256_hash(item["task"], item["input"]) == input_hash:
                return {**item, "cached": True}
    except Exception:
        pass

    try:
        input_data = request.input
        if request.task == "image_caption":
            input_data = process_image_input(request.input)

        prompt = generate_prompt(request.task, input_data)
        output = await query_gemini(prompt)

        result = {
            "status": "success",
            "task": request.task,
            "input": request.input,
            "output": output,
            "cached": False,
            "timestamp": timestamp
        }

        append_json_log(QUERIES_LOG, {
            "task": request.task,
            "input": request.input,
            "params": request.extra_params,
            "timestamp": timestamp
        })

        append_json_log(RESPONSES_LOG, result)

        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        error = {
            "status": "error",
            "message": str(e),
            "task": request.task,
            "timestamp": timestamp
        }
        append_json_log(ERRORS_LOG, {**error, "input": request.input})
        return JSONResponse(status_code=500, content=error)

@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local dev
    app.run(host="0.0.0.0", port=port)
