import requests
from django.conf import settings
from .rag_service import store_research, retrieve_similar

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def research_topic(topic, user_id):
    context = retrieve_similar(topic, user_id)
    
    if context:
        system_message = f"""You are a helpful research assistant. You have access to the user's previous research which may be relevant.

Previous relevant research:
{context}

Use this context to give a more informed and connected answer. Always provide a clear structured summary with overview, key points, important facts, and conclusion."""
    else:
        system_message = "You are a helpful research assistant. When given a topic, provide a clear and structured research summary including an overview, key points, important facts, and a conclusion."

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": system_message
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
            result = response.json()['choices'][0]['message']['content']
            store_research(topic, result, user_id)
            return result

        elif response.status_code == 429:
            return "Rate limit reached. Please wait a moment and try again."

        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."

    except Exception as e:
        return f"Something went wrong: {str(e)}"