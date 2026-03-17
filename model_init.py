import subprocess
import atexit
import requests
import asyncio
from typing import Callable
from openai import OpenAI
import time
#import prompt_generator


_vllm_process = None
_client = None

def client_call(prompt: str, model: str, max_tokens: int =256 , local_port: int = 8000, api_key: str = "key123456") -> str:
  
    _client = OpenAI(
        base_url=f"http://localhost:{local_port}/v1",
        api_key=api_key
    )
   # start_time = time.perf_counter()
    completion = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    #end_time = time.perf_counter()
    #completion_tokens = completion.usage.completion_tokens
    #duration = end_time - start_time
    #tokens_per_sec = completion_tokens / duration
    #print(f"Average tokens/s: {tokens_per_sec:.2f} (completion: {completion_tokens}, time: {duration:.2f}s)")
    return completion.choices[0].message.content


#if __name__ == "__main__":
    #client_call(prompt_generator.generate_prompts[0], 'arnir0/Tiny-LLM')


#client_call('Write a as a bullet-point list explanation of how to create a tutorial Roman history in under 200 words.', 'arnir0/Tiny-LLM')
print(client_call("give me anything", 'jinaai/reader-lm-0.5b'))
