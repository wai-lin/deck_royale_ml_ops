import json
import re

REQUIRED_KEYS = [
    "overall",
    "defense",
    "attack",
    "synergy",
    "versatility",
    "avg_elixir",
    "deck_type",
    "difficulty",
    "comments",
]


def validate_ai_output(response_text: str):
    try:
        output = json.loads(response_text)
    except json.JSONDecodeError:
        return False, {}, "Invalid JSON"

    for key in REQUIRED_KEYS:
        if key not in output:
            return False, output, f"Missing key: {key}"

    comment_block = output["comments"]
    card_lines = [
        line
        for line in comment_block.split("\n")
        if re.match(r"^[\-\u2022]\s*\w", line.strip())
    ]
    if len(card_lines) != 8:
        return False, output, f"Expected 8 card comments, found {len(card_lines)}"

    return True, output, "OK"
