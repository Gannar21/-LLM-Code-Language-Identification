# bakeoff

Same 50 code snippets, same frozen prompt, three models: one top-tier API model, one cheap API model, and one open-weights model we run ourselves. The task is simple — guess the programming language from a short code snippet — and we score it with exact string match, no human or LLM judging.

## Setup

Install the dependencies:
```
pip install -r requirements.txt
```

Create a `.env` file in the repo root with your API key:
```
OPENAI_API_KEY=sk-...
```

Start a local model server before running `local`:
```
ollama pull qwen3:4b-instruct-2507-q4_K_M
ollama serve
```

Before running `top` or `cheap`: the model names in `src/config.py` (`gpt-5.6-sol`, `gpt-5.6-luna`) are placeholders. Check the real, current model IDs at platform.openai.com/docs/models and the current prices at platform.openai.com/docs/pricing, then update `config.py` and `RUN_DATE`.

## Run

```
cd src
python run.py top cheap local   # or just the models you still need
python summarize.py             # rebuilds results/summary.csv
```

A few things to know:
- `run.py` appends to `results/per_item.csv`. If you re-run a model you already ran, delete its old rows first, or you'll get duplicates.
- The 50 `local` rows are already saved. The notebook knows not to re-run it.
- The prompt, temperature, max tokens, and item order are frozen in `src/prompt.py` and `src/config.py`. Don't change any of it per model — that's the whole point of a fair comparison.

## Results

Only `local` has been run so far. `top` and `cheap` are waiting on a real API key and the model-ID check above.

| model | accuracy | p50 latency | p95 latency | avg tokens in/out |
|---|---|---|---|---|
| local (qwen3:4b-instruct-2507-q4_K_M) | 48/50 (96%) | 3120 ms | 4990 ms | 130.9 / 2.4 |
| cheap | not run yet | — | — | — |
| top | not run yet | — | — | — |

Full numbers: `results/summary.csv`. Per-item detail: `results/per_item.csv`.

Both of the local model's wrong answers (items 15 and 25) are the same issue: the "C" snippet is also valid C++, so nothing in the code actually rules C++ out. More detail in `data/labeling_note.md` and `postmortem.md`.

Cost per 1k requests, cost at 100x traffic, and the break-even point between local and API are all set up in `src/cost.py` — but they need real `top`/`cheap` token usage before the numbers mean anything.

## Contributions

- **Eya** — built the 50-item dataset (`data/items.jsonl`), wrote the prompt template (`src/prompt.py`), ran the local-model benchmark (`src/run.py` against Ollama)
- **Asma Ganner** — set up the repo structure, wrote `src/config.py` (model settings, label loading), wrote `src/score.py` (exact-match scoring)
- **Asma Aouiti** — built the analysis notebook (`notebook/bakeoff.ipynb`), wrote `src/cost.py` (cost and break-even math), wrote `src/summarize.py` (results table generator)
- **Nouha** — wrote the documentation: `README.md`, `postmortem.md`, `results/hardware_note.md`, and the report