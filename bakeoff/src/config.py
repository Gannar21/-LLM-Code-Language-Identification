# model names, API settings, label list — TBD

import json
import os
from pathlib import Path
 
from dotenv import load_dotenv

# --- Paths ---
ROOT = Path(__file__).resolve().parent.parent

load_dotenv(ROOT / ".env")
DATA_PATH = ROOT / "data" / "items.jsonl"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)
 
# --- Labels: derived from the dataset itself, never hardcoded twice ---
def load_labels(path: Path = DATA_PATH) -> list[str]:
    with path.open() as f:
        labels = {json.loads(line)["expected"] for line in f if line.strip()}
    return sorted(labels)
 
 
LABELS = load_labels()
 
# --- Models (verified live on your account's model list, checked 2026-09-08) ---
# top / cheap: Groq-hosted API models. local: your teammate's vLLM server.
MODELS = {
    "top": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
    },
    "cheap": {
        "provider": "groq",
        "model": "openai/gpt-oss-20b",
    },
    "local": {
        "provider": "vllm",
        "model": "<placeholder — teammate fills this in>",
        "base_url": "http://localhost:8000/v1",  # vLLM's OpenAI-compatible endpoint
    },
}

# Groq list price, USD per 1M tokens, checked 2026-09-08 at console.groq.com/docs/models
GROQ_PRICING_PER_1M = {
    "top": {"input": 0.15, "output": 0.60},     # openai/gpt-oss-120b
    "cheap": {"input": 0.075, "output": 0.30},  # openai/gpt-oss-20b
}

RUN_DATE = "2026-09-08"  # update this to the actual day you run the benchmark
# --- Generation settings: identical across all three models, no exceptions ---
TEMPERATURE = 0
MAX_TOKENS = 200 # longest label ("JavaScript") is ~3 tokens; headroom without waste
 
# --- API keys ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
 
 
def require_groq_key() -> str:
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY not set — add it to .env before running")
    return GROQ_API_KEY
 
