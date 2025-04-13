import requests
from django.conf import settings
import random

def generate_quote(user_feeling):
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"
    }
    randomizer = random.randint(1, 99)
    payload = {
        "inputs": f'Come up with an short wise saying of your own for someone who says they feel: \"{user_feeling}\" Don\'t use anyone else\'s quote, come with your own {randomizer*"."}',
        "parameters": {
            "temperature": 0.65,
            "max_new_tokens": 50,
            "top_p": 0.85,
            "return_full_text": False
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        print(response.json())  # see actual response
        generated = response.json()[0]['generated_text']
        return generated.strip()
    except Exception as e:
        return f"Oops! Couldn't generate a quote. ({e})"
    
#maybe summarize category of the quote function here (by ai too)? 
