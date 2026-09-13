
# bakeoff

Same 50 code snippets, same frozen prompt, three models: one top-tier API model, one cheap API model, and one open-weights model we run ourselves.

The task is simple — guess the programming language from a short code snippet — and we score it with exact string match, no human or LLM judging.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the repo root with your API key:

```env
OPENAI_API_KEY=sk-...
```

Start a local model server before running `local`:

```bash
ollama pull qwen3:4b-instruct-2507-q4_K_M

ollama serve
```

Before running `top` or `cheap`: the model names in `src/config.py` (`gpt-5.6-sol`, `gpt-5.6-luna`) are placeholders. Check the real, current model IDs at [platform.openai.com/docs/models](https://platform.openai.com/docs/models) and the current prices at [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing), then update `config.py` and `RUN_DATE`.

## Run

```bash
cd src

python run.py top cheap local
```

Or just run the models you still need:

```bash
python run.py top
python run.py cheap
python run.py local
```

Rebuild the results summary:

```bash
python summarize.py
```

## Important Notes

- `run.py` appends to `results/per_item.csv`. If you re-run a model you already ran, delete its old rows first, or you'll get duplicates.
- The 50 `local` rows are already saved. The notebook knows not to re-run it.
- The prompt, temperature, max tokens, and item order are frozen in `src/prompt.py` and `src/config.py`.
- Don't change any of these settings per model — that's the whole point of a fair comparison.

## Results

Only `local` has been run so far. `top` and `cheap` are waiting on a real API key and the model-ID check above.

| Model | Accuracy | p50 latency | p95 latency | Avg tokens in/out |
|---|---|---|---|---|
| local (qwen3:4b-instruct-2507-q4_K_M) | 48/50 (96%) | 3120 ms | 4990 ms | 130.9 / 2.4 |
| cheap | not run yet | — | — | — |
| top | not run yet | — | — | — |

Full numbers: `results/summary.csv`

Per-item detail: `results/per_item.csv`

### Local Model Errors

Both of the local model's wrong answers (items 15 and 25) are the same issue: the "C" snippet is also valid C++, so nothing in the code actually rules C++ out.

More detail in:

- `data/labeling_note.md`
- `postmortem.md`

## Cost Analysis

Cost per 1k requests, cost at 100x traffic, and the break-even point between local and API are all set up in `src/cost.py`.

These calculations need real `top` and `cheap` token usage before the numbers mean anything.

## Contributions

### Eya

- Built the 50-item dataset (`data/items.jsonl`)
- Wrote the prompt template (`src/prompt.py`)
- Ran the local-model benchmark (`src/run.py` against Ollama)

### Asma Ganner

- Set up the repo structure
- Wrote `src/config.py` (model settings, label loading)
- Wrote `src/score.py` (exact-match scoring)

### Asma Aouiti

- Built the analysis notebook (`notebook/bakeoff.ipynb`)
- Wrote `src/cost.py` (cost and break-even math)
- Wrote `src/summarize.py` (results table generator)

### Nouha

- Wrote the documentation:
  - `README.md`
  - `postmortem.md`
  - `results/hardware_note.md`
  - The report
