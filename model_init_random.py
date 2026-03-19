import subprocess
import atexit
import requests
from openai import OpenAI
import time
import prompt_generator
import csv
import os
import fcntl
import sys  

if len(sys.argv) < 3:
    print("Uso: python3 model_init_random.py <prompt_id> <t0>")
    sys.exit(1)

prompt_id = sys.argv[1]
t0 = float(sys.argv[2])

def client_call(prompt_id: str, prompt: str, model: str, max_tokens: int = 256, local_port: int = 8000, api_key: str = "key123456"):
    _client = OpenAI(
        base_url=f"http://localhost:{local_port}/v1",
        api_key=api_key
    )

    start_rel = round(time.time() - t0, 2)
    
    completion = _client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    
    end_rel = round(time.time() - t0, 2)
    
    csv_filename = "prompt_timings.csv"
    file_exists = os.path.exists(csv_filename)
    
    with open(csv_filename, mode='a', newline='') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['prompt', 'start', 'end'])
        
        writer.writerow([prompt_id, f"{start_rel:.2f}", f"{end_rel:.2f}"])
        fcntl.flock(f, fcntl.LOCK_UN)
        
    return completion.choices[0].message.content


prompt = prompt_generator.generate_prompts(num_prompts=1)[0]
client_call(prompt_id, prompt, "Qwen/Qwen3-8B")
