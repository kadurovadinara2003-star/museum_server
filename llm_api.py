import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "sk-or-v1"  


def ask_llm(prompt, max_tokens=500):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://127.0.0.1:8000/ask"
    }
    payload = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.8
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    # можно убрать print или оставить для отладки
    if "choices" not in data:
        error_msg = data.get("error", {}).get("message", str(data))
        return f"Ошибка LLM API: {error_msg}"
    return data["choices"][0]["message"]["content"]