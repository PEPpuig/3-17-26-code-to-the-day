import torch
import subprocess


def init_vllm_ngram(max_num_seqs: str= "32", local_api_port: int = 8000, api_key: str = "key123456", precision: str = "float16", spec_model_id: str = None):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen3-8B-AWQ",
        #"--model", "Qwen/Qwen3-8B",
        "--quantization", "awq",
        "--gpu-memory-utilization", "0.85", 
        "--max-model-len", "512",
        "--max-num-seqs", max_num_seqs,
        "--api-key", api_key,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--speculative-config", '{"method": "ngram", "num_speculative_tokens": 5, "prompt_lookup_max": 4}'
    ]
    _vllm_process = subprocess.run(cmd)



def init_vllm_eagle( local_api_port: int = 8000, max_num_seqs: str = "32", api_key: str = "key123456", precision: str = "float16", spec_model_id: str = None):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen3-8B-AWQ",
        #"--model", "Qwen/Qwen3-8B",
        "--quantization", "awq",
        "--gpu-memory-utilization", "0.85", 
        "--max-model-len", "512",
        "--max-num-seqs", max_num_seqs,
        "--api-key", api_key,
        "--host", "0.0.0.0",
        "--port", "8000",
        "--speculative-config", '{"method": "EAGLE-3", "model": "RedHatAI/Qwen3-8B-speculator.eagle3", "num_speculative_tokens": 5}'
    ]
    _vllm_process = subprocess.run(cmd)



def vllm_speculative_decoding_draft(local_api_port: int = 8000, max_num_seqs: str = "128", api_key: str = "key123456", precision: str = "float16", spec_model_id: str = "Qwen/Qwen3-0.6B"):
    cmd = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", "Qwen/Qwen3-4B-Thinking-2507",
        "--gpu-memory-utilization", "0.8", 
        "--max-model-len", "2048",
        "--max-num-seqs", str(max_num_seqs),
        "--api-key", api_key,
        "--host", "0.0.0.0",
        "--port", str(local_api_port),
        "--speculative-model", spec_model_id,
        "--num-speculative-tokens", "5",
        "--use-v2-block-manager"
    ]
    _vllm_process = subprocess.run(cmd)


if __name__ == "__main__":
    #print("hola")
    torch.cuda.empty_cache()
    init_vllm_ngram()
    #init_vllm_eagle()

