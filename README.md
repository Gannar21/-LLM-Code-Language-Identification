# bakeoff

Same 50 code snippets, same frozen prompt, three models: one top-tier API model, one cheap API model, and one open-weights model we run ourselves.

The task is simple — guess the programming language from a short code snippet — and we score it using exact string match, with no human or LLM judging.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the repo root with your API key:

```env
OPENAI_API_KEY=sk-...
```

For the local model, make sure Ollama is running with:

```bash
ollama pull qwen3:4b-instruct-2507-q4_K_M
ollama serve
```

Before running `top` or `cheap`, update the placeholder model names in `src/config.py` with the current model IDs and update `RUN_DATE`.

## Run

```bash
cd src && python run.py top cheap local && python summarize.py
```

The prompt, temperature, max tokens, and item order are frozen in `src/prompt.py` and `src/config.py` to keep the comparison fair.

If a model is run again, remove its previous rows from `results/per_item.csv` first to avoid duplicates.

## Results

Only `local` has been run so far. `top` and `cheap` are waiting on a real API key and model-ID check.

| model | accuracy | p50 latency | p95 latency | avg tokens in/out |
|---|---|---|---|---|
| local (qwen3:4b-instruct-2507-q4_K_M) | 48/50 (96%) | 3120 ms | 4990 ms | 130.9 / 2.4 |
| cheap | not run yet | — | — | — |
| top | not run yet | — | — | — |

Full results are available in `results/summary.csv`.

Per-item results are available in `results/per_item.csv`.

The two local-model errors (items 15 and 25) have the same issue: the "C" snippet is also valid C++, so nothing in the code rules C++ out.

More details are available in `data/labeling_note.md` and `postmortem.md`.

## Contributions

- **Eya Bedoui** — Built the 50-item dataset (`data/items.jsonl`), wrote the prompt template (`src/prompt.py`), and ran the local-model benchmark using Ollama.

- **Asma Ganner** — Set up the repository structure, wrote `src/config.py` for model settings and label loading, and wrote `src/score.py` for exact-match scoring.

- **Asma Aouiti** — Built the analysis notebook (`notebook/bakeoff.ipynb`), wrote `src/cost.py` for cost and break-even calculations, and wrote `src/summarize.py` for the results table.

- **Nouha Aouiti** — Wrote the documentation, including `README.md`, `postmortem.md`, `results/hardware_note.md`, and the report.
