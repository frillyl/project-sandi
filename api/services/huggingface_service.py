# services/huggingface_service.py
import requests
import os

HUGGINGFACE_API_TOKEN = os.getenv("HF_API_TOKEN")
# print("HF TOKEN:", HUGGINGFACE_API_TOKEN)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
INDOBART_API_URL = "https://api-inference.huggingface.co/models/gaduhhartawan/indobart-base"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def mistral_abstractive_summary(prompt: str) -> str:
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "do_sample": True,
            "temperature": 0.7,
            "return_full_text": False
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]['generated_text'].strip()
    else:
        raise Exception(f"HuggingFace API error: {response.status_code} - {response.text}")

def summarize_with_indobart(text: str) -> str:
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 200,  # karakteristik summarization IndoBART
            "min_length": 30,
            "do_sample": False
        }
    }

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }

    response = requests.post(INDOBART_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]['summary_text'].strip()
    else:
        raise Exception(f"HuggingFace IndoBART API error: {response.status_code} - {response.text}")
