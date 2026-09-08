"""
Runs the frozen prompt against all three models, in the same item order, and
logs one row per (model, item) to results/per_item.csv.

Both Groq and vLLM expose an OpenAI-compatible /chat/completions endpoint, so
we use the `openai` client for both — just pointed at different base_urls.

Requires:
  - GROQ_API_KEY in .env (for "top" and "cheap")
  - a running vLLM server at config.MODELS["local"]["base_url"] (for "local")

Run with: python run.py [model_key ...]
  e.g.    python run.py top cheap
"""

import csv
import json
import time
from pathlib import Path

from openai import APIError, APITimeoutError, OpenAI

from config import DATA_PATH, MAX_TOKENS, MODELS, RESULTS_DIR, RUN_DATE, TEMPERATURE, require_groq_key
from prompt import build_prompt
from score import score_item

PER_ITEM_CSV = RESULTS_DIR / "per_item.csv"
REQUEST_TIMEOUT_S = 30

FIELDNAMES = [
    "model_key",
    "provider",
    "model_name",
    "item_id",
    "expected",
    "raw_output",
    "parsed",
    "status",
    "correct",
    "latency_ms",
    "input_tokens",
    "output_tokens",
    "run_date",
]


def load_items(path: Path = DATA_PATH) -> list[dict]:
    items = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            items.append({"id": raw["id"], "code": raw["code"], "expected": raw["expected"]})
    return items


def make_client(model_key: str) -> OpenAI:
    cfg = MODELS[model_key]
    if cfg["provider"] == "groq":
        return OpenAI(api_key=require_groq_key(), base_url="https://api.groq.com/openai/v1")
    elif cfg["provider"] == "vllm":
        return OpenAI(api_key="not-needed", base_url=cfg["base_url"])
    else:
        raise ValueError(f"Unknown provider for {model_key!r}: {cfg['provider']}")


def call_model(client: OpenAI, model_name: str, prompt_text: str) -> dict:
    """
    Single call, timed. Returns raw_output, token usage, latency, and an
    `error` tag ("timeout" | "refusal" | "api_error") if something went wrong.
    """
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt_text}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            timeout=REQUEST_TIMEOUT_S,
        )
        latency_ms = (time.perf_counter() - start) * 1000

        choice = response.choices[0]
        raw_output = choice.message.content
        finish_reason = choice.finish_reason

        error = "refusal" if finish_reason == "content_filter" else None

        usage = response.usage
        input_tokens = usage.prompt_tokens if usage else None
        output_tokens = usage.completion_tokens if usage else None

        return {
            "raw_output": raw_output,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": latency_ms,
            "error": error,
        }

    except APITimeoutError as e:
        print(f"  [TIMEOUT] {e}")
        return {
            "raw_output": None, "input_tokens": None, "output_tokens": None,
            "latency_ms": (time.perf_counter() - start) * 1000, "error": "timeout",
        }
    except APIError as e:
        print(f"  [API_ERROR] {e}")
        return {
            "raw_output": None, "input_tokens": None, "output_tokens": None,
            "latency_ms": (time.perf_counter() - start) * 1000, "error": "api_error",
        }


def run_model(model_key: str, items: list[dict]) -> list[dict]:
    cfg = MODELS[model_key]
    client = make_client(model_key)
    rows = []

    print(f"\n=== Running {model_key} ({cfg['model']}) over {len(items)} items ===")
    for i, item in enumerate(items, 1):
        prompt_text = build_prompt(item["code"])
        result = call_model(client, cfg["model"], prompt_text)
        scored = score_item(item["expected"], result["raw_output"], error=result["error"])

        rows.append({
            "model_key": model_key,
            "provider": cfg["provider"],
            "model_name": cfg["model"],
            "item_id": item["id"],
            "expected": item["expected"],
            "raw_output": result["raw_output"],
            "parsed": scored["parsed"],
            "status": scored["status"],
            "correct": scored["correct"],
            "latency_ms": round(result["latency_ms"], 2),
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "run_date": RUN_DATE,
        })

        if i % 10 == 0 or i == len(items):
            print(f"  {i}/{len(items)} done")

    return rows


def write_csv(rows: list[dict], path: Path = PER_ITEM_CSV, append: bool = False) -> None:
    mode = "a" if append and path.exists() else "w"
    write_header = not (append and path.exists())
    with path.open(mode, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def main(model_keys: list[str]):
    items = load_items()
    print(f"Loaded {len(items)} items from {DATA_PATH}")

    all_rows = []
    for model_key in model_keys:
        rows = run_model(model_key, items)
        all_rows.extend(rows)
        write_csv(rows, append=True)

    print(f"\nWrote {len(all_rows)} rows to {PER_ITEM_CSV}")


if __name__ == "__main__":
    import sys

    requested = sys.argv[1:] if len(sys.argv) > 1 else ["top", "cheap", "local"]
    main(requested)
