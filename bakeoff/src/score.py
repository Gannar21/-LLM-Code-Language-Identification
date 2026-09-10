# strict parser + exact-match scoring — TBD
# strict parser + exact-match scoring — TBD
"""
Strict, deterministic scoring. No human, no LLM judge.
A parse error, refusal, or timeout always counts as wrong.
"""

from config import LABELS

_LABEL_LOOKUP = {label.strip().lower(): label for label in LABELS}


def parse_output(raw_output):
    if raw_output is None:
        return None

    cleaned = raw_output.strip()
    cleaned = cleaned.strip(" \t\n\r.\"'`")

    if "\n" in cleaned or len(cleaned) == 0:
        return None

    return _LABEL_LOOKUP.get(cleaned.lower())


def score_item(expected: str, raw_output, error: str = None) -> dict:
    if error is not None:
        return {"status": error, "parsed": None, "correct": False}

    parsed = parse_output(raw_output)
    if parsed is None:
        return {"status": "parse_error", "parsed": None, "correct": False}

    return {
        "status": "ok",
        "parsed": parsed,
        "correct": parsed == expected,
    }


if __name__ == "__main__":
    assert score_item("Python", "Python")["correct"] is True
    assert score_item("Python", "python.")["correct"] is True
    assert score_item("Python", "  Python  ")["correct"] is True
    assert score_item("Python", "It's Python")["status"] == "parse_error"
    assert score_item("Python", None, error="timeout")["status"] == "timeout"
    assert score_item("Python", "Java")["correct"] is False
    print("score.py sanity checks passed")
