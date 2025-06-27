from fastapi import FastAPI, Request
from format_checker import validate_ai_output
from wandb_logger import log_to_wandb
from gpt_simulator import call_gpt_evaluator
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

# Prometheus metrics
VALID_RESPONSES = Counter("valid_ai_outputs_total", "Valid outputs from GPT")
INVALID_RESPONSES = Counter("invalid_ai_outputs_total", "Invalid outputs from GPT")
HATEFUL_RESPONSES = Counter(
    "hateful_outputs_total", "AI responses with detected hate speech"
)


@app.post("/evaluate")
async def evaluate_deck(request: Request):
    deck = await request.json()

    response_text = call_gpt_evaluator(deck)

    valid, parsed, reason = validate_ai_output(response_text)

    is_hateful = any(
        word in response_text.lower()
        for word in ["hate", "kill", "racist", "sexist", "nazi"]
    )

    if valid:
        VALID_RESPONSES.inc()
    else:
        INVALID_RESPONSES.inc()

    if is_hateful:
        HATEFUL_RESPONSES.inc()
        reason += " | Detected potential hate speech"

    log_to_wandb(deck, parsed, valid, reason)

    return {
        "valid": valid,
        "reason": reason,
        "parsed_output": parsed if valid else None,
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
