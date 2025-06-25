import mlflow
import requests
import json

from openai import OpenAI
from pydantic import ValidationError
from ..clashroyale import get_player_info, player_to_md
from ..clashroyale.schemas import Player
from ..get_envs import get_envs
from ..meta_decks import decks, decks_to_md

envs = get_envs()
PROMPTS_FOLDER = envs["prompts_dir"]

OPENAI_API_KEY = envs["openai_api_key"]
openai = OpenAI(api_key=OPENAI_API_KEY)
MODEL_NAME = "gpt-3.5-turbo-1106"

mlflow.set_tracking_uri(envs["mlflow_uri"])
mlflow.set_experiment("deck_royale")
mlflow.openai.autolog()


def generate_deck(user_input: str, player_id: str = None):
    with open(f"{PROMPTS_FOLDER}/developer_prompt.md", "r", encoding="utf-8") as f:
        developer_prompt = f.read()

    meta_md = decks_to_md(decks.get_popular_decks())
    developer_prompt = developer_prompt.replace("{{current_meta_decks}}", meta_md)

    input_section = f"User input:\n{user_input.strip()}\n\n"

    if player_id:
        try:
            player_resp = get_player_info(player_id)
            player_resp.raise_for_status()
            player_data = Player.model_validate(player_resp.json(), strict=False)
            input_section += player_to_md(player_data)
        except (requests.HTTPError, ValidationError) as e:
            print(f"Player data error: {e}")
            return None

    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": input_section},
        ],
    )

    try:
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print("Deck JSON parsing failed:", e)
        return None


def evaluate_deck(deck_json: dict):
    # Load prompt
    with open(f"{PROMPTS_FOLDER}/evaluator_prompt.md", "r", encoding="utf-8") as f:
        evaluator_prompt = f.read()

    # Inject deck JSON
    filled_prompt = evaluator_prompt.replace(
        "{{deck_json}}", json.dumps(deck_json, indent=2)
    )

    print("🟡 EVALUATION PROMPT BEING SENT:\n", filled_prompt)

    try:
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": filled_prompt},
                {"role": "user", "content": "Evaluate the above deck."},
            ],
        )
    except Exception as e:
        print("🔴 OpenAI call failed:", e)
        return {"error": "OpenAI call failed", "details": str(e)}

    raw_content = response.choices[0].message.content.strip()

    print("🟢 RAW GPT RESPONSE:\n", raw_content)

    try:
        parsed = json.loads(raw_content)
        print("✅ Parsed Evaluation JSON")
        return parsed
    except Exception as e:
        print("⚠️ JSON parsing failed:", e)
        return {"error": "Parsing failed", "raw_output": raw_content}


@mlflow.trace
def ask_deck_advice(user_input: str, player_id: str = None):
    deck = generate_deck(user_input, player_id)
    if not deck:
        return {"error": "Deck generation failed"}

    evaluation = evaluate_deck(deck)
    return {"suggested_deck": deck, "evaluation": evaluation}
