import os

from typing import TypedDict
from dotenv import load_dotenv

load_dotenv()


class EnvVars(TypedDict):
    mlflow_uri: str
    openai_api_key: str
    royale_api_url: str
    royale_api_key: str
    prompts_dir: str
    firebase_sdk_json: str


def get_envs() -> EnvVars:
    """
    Function to retrieve environment variables required for the application.
    It checks for the presence of the required environment variables and raises an error if any are missing.
    """
    mlflow_uri = os.getenv("MLFLOW_URI")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    royale_api_url = os.getenv("ROYALE_API_URL")
    royale_api_key = os.getenv("ROYALE_API_KEY")
    prompts_dir = os.getenv("PROMPTS_DIR")
    firebase_sdk_json = os.getenv("FIREBASE_SDK_JSON")

    if not mlflow_uri:
        raise ValueError("MLFLOW_URI environment variable is not set.")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    if not royale_api_url:
        raise ValueError("ROYALE_API_URL environment variable is not set.")
    if not royale_api_key:
        raise ValueError("ROYALE_API_KEY environment variable is not set.")
    if not prompts_dir:
        raise ValueError("PROMPTS_DIR environment variable is not set.")
    if not firebase_sdk_json:
        raise ValueError("FIREBASE_SDK_JSON environment variable is not set.")

    return {
        "mlflow_uri": mlflow_uri,
        "openai_api_key": openai_api_key,
        "royale_api_url": royale_api_url,
        "royale_api_key": royale_api_key,
        "prompts_dir": prompts_dir,
        "firebase_sdk_json": firebase_sdk_json,
    }
