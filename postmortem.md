# Postmortem

## What went wrong
Two of our "C" items (id 15 and id 25) don't actually contain anything that's C-specific — no `stdio.h`, no `printf`, no pointers, nothing that would fail to compile as C++. So when the local model called both of them "C++", it wasn't really wrong, our dataset was just ambiguous and we didn't catch it. Two people agreed on the label, and it still slipped through, because the code itself never ruled out the other answer.

We also only got the `local` model run before writing this up. `results/per_item.csv` has all 50 rows for `local` but nothing yet for `top` or `cheap` — we got ahead of ourselves running the open-weights model and didn't loop back to do the API ones in the same sitting like we should have.

On top of that, the model names sitting in `config.py` right now (`gpt-5.6-sol`, `gpt-5.6-luna`) are placeholders we never actually checked against OpenAI's current model list or pricing page. There's already a comment in the file reminding us to do that — we just hadn't gotten to it.

One more small thing: if you naively compute tokens/sec for the local model as `output_tokens / latency`, you get something like 0.8 tok/s, which looks awful. But the answer is only 2-3 tokens long, so almost all of that time is the model reading the prompt, not generating text. Left alone, that number would make the local model look way slower at generating than it actually is.

## What we'd do differently
- Bake a distinguishing feature into every item when we write it, not just check for ambiguity when we review it — two reviewers agreeing doesn't catch a case where the code genuinely fits two languages.
- Actually look up the real model IDs and current prices before writing them into the config, instead of leaving placeholders in and forgetting about them.
- Run all three models back-to-back in one sitting so the results file is never sitting there half-finished.
- Report tokens/sec next to a note on why it's low for this task, so nobody reads it as "the local model is slow" when really the task just barely uses any generation.

## What we learned
Exact-match scoring works really well here — a 1-3 token answer doesn't leave much room for "close enough," so we're not accidentally mixing up real mistakes with scoring noise.

A 4B open-weights model running on a laptop already got 48/50 on this. That's honestly a bit humbling — it means this task is close to maxed out for all three model sizes, and if we want to actually see a difference between models in Project 1, we need something harder or more ambiguous than "guess the language."

Freezing the prompt and the item list before running anything made it painless to add the local results without touching anything else — `write_csv(..., append=True)` meant we could run models on different days without redoing work.