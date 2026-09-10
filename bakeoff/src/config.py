# model names, API settings, label list

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

# --- Models ---
# top / cheap: real OpenAI API (proprietary, satisfies "best model a provider
# sells" / "small fast model"). local: your teammate's vLLM server.
#
# CHECK these model IDs against https://platform.openai.com/docs/models
# right before you run, then update the date below to match.
MODELS = {
    "top": {
        "provider": "openai",
        "model": "gpt-5.6-sol",
        "base_url": "https://api.openai.com/v1",
    },
    "cheap": {
        "provider": "openai",
        "model": "gpt-5.6-luna",
        "base_url": "https://api.openai.com/v1",
    },
    "local": {
        "provider": "vllm",
        "model": "<placeholder — teammate fills this in>",
        "base_url": "http://localhost:8000/v1",  # vLLM's OpenAI-compatible endpoint
    },
}

# OpenAI list price, USD per 1M tokens — CHECK against
# https://platform.openai.com/docs/pricing before you run, prices move fast.
API_PRICING_PER_1M = {
    "top": {"input": 5.00, "output": 30.00},     # gpt-5.6-sol
    "cheap": {"input": 0.20, "output": 1.20},    # gpt-5.6-luna
}

RUN_DATE = "2026-09-09"  # update this to the actual day you run the benchmark
# --- Generation settings: identical across all three models, no exceptions ---
TEMPERATURE = 0
MAX_TOKENS = 16  # a language name is 1-3 tokens; enough headroom, no more

# --- API keys ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def require_openai_key() -> str:
    if not OPENAI_API_KEY:
        raise EnvironmentError("OPENAI_API_KEY not set — add it to .env before running")
    return OPENAI_API_KEY
 
