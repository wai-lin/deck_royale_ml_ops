import openai
import os
import json

# You must set your API key in an environment variable or directly (not recommended for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load evaluator prompt template
with open("evaluator_prompt.md", "r", encoding="utf-8") as f:
    EVALUATOR_PROMPT_TEMPLATE = f.read()


def call_gpt_evaluator(deck_json: dict) -> str:
    # Insert the deck JSON into the template
    final_prompt = EVALUATOR_PROMPT_TEMPLATE.replace(
        "{{deck_json}}", json.dumps(deck_json, indent=2)
    )

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a Clash Royale deck evaluator."},
            {"role": "user", "content": final_prompt},
        ],
        temperature=0.2,
    )

    # Return only the assistant's reply (we expect it to be JSON)
    return response.choices[0].message["content"]
