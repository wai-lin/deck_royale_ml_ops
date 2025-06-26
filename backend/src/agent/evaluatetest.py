from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load .env file from the backend directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Get the API key from the loaded environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Deck to evaluate
deck_data = {
    "card_1": "Goblin Giant",
    "card_2": "Spear Goblins",
    "card_3": "Dart Goblin",
    "card_4": "Goblin Gang",
    "card_5": "Goblin Barrel",
    "card_6": "Goblin",
    "card_7": "Goblin Hut",
    "card_8": "Goblin Curse",
    "avg_elixir": 3.1,
    "deck_type": "All-Goblin Control",
}
# Load evaluator prompt
current_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(current_dir, "evaluator_prompt.md")

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt_template = f.read()

deck_json_str = json.dumps(deck_data, indent=2)
full_prompt = prompt_template.replace("{{deck_json}}", deck_json_str)

# Call the OpenAI chat model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a Clash Royale deck evaluation assistant.",
        },
        {"role": "user", "content": full_prompt},
    ],
)

# Print the result
print(response.choices[0].message.content)
