import requests
from django.conf import settings
import random
import re

def generate_quote(user_feeling):
    url = "https://api-inference.huggingface.co/models/tiiuae/Falcon3-1B-Instruct"

    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"
    }

    randomizer = random.randint(1, 9)
    prompt = (
        f'Come up with a short wise saying of your own for someone who says they feel: "{user_feeling}". '
        f'Make it original and meaningful. Don\'t use anyone else\'s quote. Your answer should be only the quote. {randomizer*"."}'
    )

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.9,
            "max_new_tokens": 50,
            "top_p": 0.95
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        raw = response.json()[0]['generated_text']

        # Remove the prompt part if the model included it in the response
        if prompt in raw:
            raw = raw.replace(prompt, '')

        # Remove signatures like "- Unknown" or "– Unknown"
        cleaned = re.sub(r'\s*[-–—]\s*Unknown.*$', '', raw.strip())

        # Remove leftover "<|assistant|>" tokens if present
        cleaned = cleaned.replace("<|assistant|>", "").strip()

        return cleaned

    except Exception as e:
        return f"Oops! Couldn't generate a quote. ({e})"

    
#maybe summarize category of the quote function here (by ai too)? 
