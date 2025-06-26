import mlflow
import requests
import json

from openai import OpenAI
from pydantic import BaseModel, ValidationError
from typing import Any
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

class EvaluationResponseJSON(BaseModel):
    overall: float
    defense: float
    attack: float
    synergy: float
    versatility: float
    avg_elixir: float
    difficulty: float
    deck_type: str
    comments: str


@mlflow.trace
def evaluation(prompt: str, deck_data: AgentResponseJSON):
    """
    Function to evaluate a Clash Royale deck using OpenAI API.
    """

    # Load the prompt instructions from a markdown file
    with open(f"{PROMPTS_FOLDER}/evaluation_prompt.md", "r") as file:
        prompt_input = file.read()
        # Replace placeholders in the instructions with actual data
        prompt_input = prompt_input.replace(
            "{{deck_json}}",
            json.dumps(deck_data.__dict__),
        )
    
    completion = openai.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a Clash Royale deck evaluation assistant.",
            },
            {
                "role": "user",
                "content": prompt_input,
            }
        ],
    )

    content = completion.choices[0].message.content
    print("Raw model output:", repr(content))

    # Attempt to parse the content as JSON
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse evaluation response as JSON: {e}")
        print("Raw content:", content)
        raise

    try:
        evaluation_result = EvaluationResponseJSON.model_validate(parsed)
    except ValidationError as e:
        print(f"Validation error for evaluation response: {e}")
        print("Parsed content:", parsed)
        raise

    with mlflow.start_run():
        mlflow.log_param("user prompt", prompt)
        mlflow.log_param("deck_name", deck_data.deck_name)
        mlflow.log_param("average_elixir_cost", deck_data.average_elixir_cost)
        mlflow.log_param("cards", deck_data.cards)

        mlflow.log_metric("eval_overall", evaluation_result.overall)
        mlflow.log_metric("eval_defense", evaluation_result.defense)
        mlflow.log_metric("eval_attack", evaluation_result.attack)
        mlflow.log_metric("eval_synergy", evaluation_result.synergy)
        mlflow.log_metric("eval_versatility", evaluation_result.versatility)
        mlflow.log_metric("eval_avg_elixir", evaluation_result.avg_elixir)
        mlflow.log_metric("eval_difficulty", evaluation_result.difficulty)

    return evaluation_result


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

    response = openai.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": instructions },
            {"role": "user", "content": input},
        ],
        text={"format": {"type": "json_object"}}
    )
    content = response.output_text
    print("Raw model output:", repr(content))

    # Attempt to parse the content as JSON
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse agent response as JSON: {e}")
        print("Raw content:", content)
        raise

    try:
        agent_resp = AgentResponseJSON.model_validate(parsed)
    except ValidationError as e:
        print(f"Validation error for agent response: {e}")
        print("Parsed content:", parsed)
        raise

    eval_resp = evaluation(user_input, agent_resp)

    return {
        "id": response.id,
        "output": agent_resp,
        "evaluation": eval_resp,
    }
