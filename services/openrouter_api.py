import requests
import json
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL = "https://your-site.com"
SITE_NAME = "Seekho Sakhi Chatbot"

def fetch_openrouter_info(user_query):
    """
    Fetch information using OpenRouter's Python requests API.
    Ensures answers are concise (50-100 words) and factual.
    """
    if not OPENROUTER_API_KEY:
        print("⚠️ OpenRouter API key not found! Check your .env file.")
        return "Sorry, API key not found. Cannot fetch information."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }

    # Updated system prompt for concise answers
    payload = {
        "model": "alibaba/tongyi-deepresearch-30b-a3b:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant providing accurate information on women's "
                    "safety and crimes in India. Keep answers concise, factual, and "
                    "between 50-100 words. Avoid long case stories unless specifically asked."
                )
            },
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return answer.strip()
    except Exception as e:
        print("OpenRouter API error:", e)
        return (
            "Sorry, something went wrong while fetching information. "
            "Safety Tip: Always stay aware of your surroundings. "
            "Helplines: Police 100, Women Helpline 181"
        )
