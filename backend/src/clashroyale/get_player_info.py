import requests

from ..get_envs import get_envs

envs = get_envs()
API_URL = envs["royale_api_url"]
API_KEY = envs["royale_api_key"]


def get_player_info(player_id: str):
    """
    Function to get player information from the OpenAI API.
    This function retrieves player information based on the provided player_id.
    """

    if not player_id:
        raise ValueError("Player ID cannot be None or empty")

    # Replace '#' with '%23' in player_id to ensure it is URL-safe
    id = player_id.replace("#", "%23")

    url = f"{API_URL}/v1/players/{id}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url=url, headers=headers)
    return response
