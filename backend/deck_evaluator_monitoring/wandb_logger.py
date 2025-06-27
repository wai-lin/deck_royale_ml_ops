import wandb
import json


def log_to_wandb(deck_input, output, valid, reason):
    wandb.init(
        project="deck-evaluator",
        name=deck_input.get("deck_type", "unknown"),
        reinit=True,
    )
    wandb.log(
        {
            "deck_input": deck_input,
            "overall": output.get("overall", -1),
            "valid_format": int(valid),
            "validation_reason": reason,
            "raw_output": wandb.Html(f"<pre>{json.dumps(output, indent=2)}</pre>"),
        }
    )
    wandb.finish()
