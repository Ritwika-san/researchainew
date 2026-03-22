import requests
from django.conf import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def research_topic(topic):
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful research assistant. When given a topic, provide a clear and structured research summary including an overview, key points, important facts, and a conclusion."
            },
            {
                "role": "user",
                "content": f"Research this topic thoroughly: {topic}"
            }
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']

        elif response.status_code == 429:
            return "Rate limit reached. Please wait a moment and try again."

        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

    except Exception as e:
        return f"Something went wrong: {str(e)}"