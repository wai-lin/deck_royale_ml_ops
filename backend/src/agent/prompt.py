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

# region: openai
OPENAI_API_KEY = envs["openai_api_key"]
openai = OpenAI(api_key=OPENAI_API_KEY)
# endregion

# region: mlflow
TRACKING_URI = envs["mlflow_uri"]
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("deck_royale")
mlflow.openai.autolog()
# endregion


@mlflow.trace
def ask_deck_advice(user_input: str, player_id: str = None):
    """
    Function to generate a Clash Royale deck based on user input,
    then evaluate the generated deck using a structured scoring system.
    """

    # Step 1: Load developer prompt
    with open(f"{PROMPTS_FOLDER}/developer_prompt.md", "r") as file:
        content = file.read()


    popular_decks = decks.get_popular_decks()
    instructions_dev = content.replace("{{current_meta_decks}}", decks_to_md(popular_decks))


    # Build the user input section
    input_section = f"User input:\n{user_input.strip()}\n\n"

    # If player ID is provided, fetch and append player info
    if player_id:
        player_resp = get_player_info(player_id)
        try:
            player_resp.raise_for_status()
            player_json = player_resp.json()
            player = Player.model_validate(player_json, strict=False)
            input_section += player_to_md(player)
        except (requests.HTTPError, ValidationError) as e:
            print(f"Error with player data: {e}")
            return None

    # Step 2: Get deck suggestion from GPT
    response_dev = openai.responses.create(
        model="gpt-4.1",
        instructions=instructions_dev,
        input=input_section
    )

    # Parse the suggested deck JSON from GPT
    try:
        deck_json = json.loads(response_dev.response.strip())
    except Exception as e:
        print(f"Failed to parse deck JSON: {e}")
        return None

    # Step 3: Load evaluator prompt
    with open(f"{PROMPTS_FOLDER}/evaluator_prompt.md", "r") as f:
        instructions_eval = f.read()

    # Prepare input for evaluation
    input_eval = f"Deck Input:\n```json\n{json.dumps(deck_json, indent=2)}\n```"

    # Step 4: Get deck evaluation from GPT
    response_eval = openai.responses.create(
        model="gpt-4.1",
        instructions=instructions_eval,
        input=input_eval
    )

    return {
        "suggested_deck": deck_json,
        "evaluation": response_eval.response
    }
