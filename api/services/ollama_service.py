import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"

def abstractive_summary(text: str) -> str:
    prompt = f"Buat ringkasan singkat dari teks berikut:\n\n{text}\n\nRingkasan:"
    
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    
    if response.status_code != 200:
        raise Exception(f"Failed to get summary from Ollama: {response.text}")
    
    result = response.json()
    return result.get("response", "").strip()