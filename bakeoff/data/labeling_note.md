# Labeling Note

## Source
We wrote all 50 snippets ourselves — didn't scrape or copy them from anywhere. Each one is a small, realistic-looking chunk of code (a function, a class, a couple of lines) in one of 10 languages: Python, Java, JavaScript, TypeScript, C, C++, C#, Go, Rust, PHP. Five snippets per language. Nothing fancy or tricky on purpose — just the kind of code you'd see in a tutorial or a small script.

## Verification
Two of us checked every single label before it went into `items.jsonl`. If we didn't independently agree on the language, we either rewrote the snippet to make it clearer or threw it out.

That said, we missed something: two of the "C" snippets (id 15 and id 25) turned out to also be perfectly valid C++ — nothing in them actually rules out C++ (no `printf`, no pointers, nothing C-specific). Both of us agreed on "C" when we wrote them, so it slipped through. It only showed up once we looked at what the model actually got wrong. More on that in `postmortem.md`.

## Dev/test split
There isn't one. Project 0 wants one frozen test set, not a tuned model, so all 50 items are just the test set. Same items, same order, for every model. We locked the prompt before running anything and didn't touch it after seeing outputs.