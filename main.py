import torch
import subprocess


def init_vllm_ngram(max_num_seqs: str= "128", local_api_port: int = 8000, api_key: str = "key123456", precision: str = "float16", spec_model_id: str = None):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen3-8B",
        "--gpu-memory-utilization", "0.85", 
        "--max-model-len", "512",
        "--max-num-seqs", max_num_seqs,
        "--api-key", api_key,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--speculative-config", '{"method": "ngram", "num_speculative_tokens": 5, "prompt_lookup_max": 4}'
    ]
    _vllm_process = subprocess.run(cmd)



def init_vllm_eagle( local_api_port: int = 8000, max_num_seqs: str = 128, api_key: str = "key123456", precision: str = "float16", spec_model_id: str = None):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen3-8B",
        "--gpu-memory-utilization", "0.85", 
        "--max-model-len", "512",
        "--max-num-seqs", max_num_seqs,
        "--api-key", api_key,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--speculative-config", '{"method": "EAGLE-3", "model": "RedHatAI/Qwen3-8B-speculator.eagle3", "num_speculative_tokens": 5}'
    ]
    _vllm_process = subprocess.run(cmd)


if __name__ == "__main__":
    #print("hola")
    torch.cuda.empty_cache()
    init_vllm_ngram()
    #init_vllm_eagle()

