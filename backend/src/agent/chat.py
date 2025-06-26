import mlflow
import requests

from openai import OpenAI
from pydantic import BaseModel, ValidationError
from ..clashroyale import get_player_info, player_to_md
from ..clashroyale.schemas import Player
from ..get_envs import get_envs
from ..meta_decks import decks, decks_to_md

envs = get_envs()
PROMPTS_FOLDER = envs["prompts_dir"]

# region: openai
OPENAI_API_KEY = envs["openai_api_key"]
# Initialize OpenAI client with the API key
openai = OpenAI(api_key=OPENAI_API_KEY)
# endregion

# region: mlflow
# Set up MLflow tracking URI and experiment
TRACKING_URI = envs["mlflow_uri"]
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment("deck_royale")
mlflow.openai.autolog()
# endregion


class AgentResponseJSON(BaseModel):
    deck_name: str
    average_elixir_cost: float
    cards: list[str]
    comment: str


@mlflow.trace
def ask_agent(user_input: str, player_id: str = None):
    """
    Function to ask for deck advice from the OpenAI API.
    Args:
        user_input (str): The input from the user.
        player_id (str, optional): The player ID to get additional information. Defaults to None.
    Returns:
        response: AgentResponseJSON | None: The response from the OpenAI API parsed into a structured format.
    """

    # Load the prompt instructions from a markdown file
    with open(f"{PROMPTS_FOLDER}/developer_prompt.md", "r") as file:
        instructions = file.read()
        popular_decks = decks.get_popular_decks()
        # Replace placeholders in the instructions with actual data
        instructions = instructions.replace(
            "{{current_meta_decks}}",
            decks_to_md(popular_decks),
        )

    input = "User input:\n"
    input += f"{user_input}\n\n"

    if player_id:
        player_resp = get_player_info(player_id)

        try:
            player_resp.raise_for_status()  # Raises HTTPError for bad status codes
        except requests.HTTPError as e:
            print(f"HTTP error occurred: {e} - Response content: {player_resp.text}")
            return None

        try:
            player_json = player_resp.json()
            player = Player.model_validate(player_json, strict=False)
        except ValidationError as e:
            print(f"Pydantic validation error: {e}")
            return None

        input += player_to_md(player)

    response = openai.responses.parse(
        model="gpt-4.1",
        instructions=instructions,
        input=input,
        text_format=AgentResponseJSON,
    )

    return {
        "id": response.id,
        "output": response.output_parsed,
    }
