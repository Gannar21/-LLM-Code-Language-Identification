# Hardware Note

## Hardware spec
Ran on a MacBook Air — fill in the exact chip and RAM here, e.g. "Apple M2, 16 GB". Easiest way to get the exact numbers, in Terminal:
```
sysctl -n machdep.cpu.brand_string   # what chip you have
sysctl hw.memsize                    # RAM, in bytes
```
No dedicated GPU — Apple Silicon Macs run Ollama on the unified memory/CPU+GPU combo, not a separate graphics card. You can check what Ollama's using by running `ollama ps` while a request is in flight.

Model: `qwen3:4b-instruct-2507-q4_K_M` (4B parameters, Q4_K_M quantized), served locally through Ollama at `http://localhost:11434/v1`.

## Measured tokens/sec
Pulled straight from `results/per_item.csv` (the 50 `local` rows), as `output_tokens / (latency_ms / 1000)` per request, then averaged:

- **0.79 tokens/sec** on average
- Output was tiny either way — averaged 2.4 tokens per answer, since the whole task is just "say the language name"
- Input averaged 130.9 tokens
- Latency: 3120 ms at the median, 4990 ms at p95

Don't take that 0.79 number at face value, though. With only 2-3 output tokens per call, almost all the latency is the model reading the prompt and warming up, not actually generating text — one slow token can wreck the whole ratio. If you want a real read on generation speed, time a longer response separately (e.g. `ollama run qwen3:4b-instruct-2507-q4_K_M --verbose` on a prompt that needs a paragraph back) and report that alongside this one.