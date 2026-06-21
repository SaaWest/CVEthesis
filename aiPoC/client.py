import requests
import json

URL = "http://localhost:11434/api/chat"

def query(model: str, msgs: list, temp=0.2):
    global URL
    payload = {
        "model": model,
        "messages": msgs,
        "stream": False,
        "options": {
            "temp": temp
        }
    }
    r = requests.post(URL, json=payload)
    print(r.status_code)
    print(r.text)

    r.raise_for_status()

    return r.json()["message"]["content"]