import subprocess
import atexit
import requests
import asyncio
from typing import Callable
from openai import OpenAI
import time


_vllm_process = None
_client = None

def client_call(prompt: str, model: str, max_tokens: int =256 , local_port: int = 8000, api_key: str = "key123456") -> str:
  
    _client = OpenAI(
        base_url=f"http://localhost:{local_port}/v1",
        api_key=api_key
    )
    completion = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
  return completion.choices[0].message.content

print(client_call("give me anything", 'jinaai/reader-lm-0.5b'))
