import json

from client import query
from prompt import pocPrompt

def pocGenerator(context):
    prompt = pocPrompt(context=context)

    rsp = query("qwen3:latest", prompt)
    return json.loads(rsp)

