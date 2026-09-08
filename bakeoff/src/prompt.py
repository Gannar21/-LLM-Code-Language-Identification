# frozen prompt template — TBD
"""
The one frozen prompt. Every model sees exactly this text, in this order,
for every item. Do not special-case any model.
"""

from config import LABELS

PROMPT_TEMPLATE = """You are a programming language classifier.

Identify the programming language used in the code snippet.

Choose exactly one language from this list:

{label_list}

Return ONLY the language name, spelled exactly as it appears in the list above.
Do not provide an explanation, punctuation, or any other text.

Code:
{code}
"""


def build_prompt(code: str) -> str:
    label_list = "\n".join(LABELS)
    return PROMPT_TEMPLATE.format(label_list=label_list, code=code)


if __name__ == "__main__":
    sample = 'print("hello world")'
    print(build_prompt(sample))
