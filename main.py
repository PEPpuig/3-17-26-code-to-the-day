# import model_init
# import prompt_loader
# import prompt_generator
import torch
import subprocess


def init_vllm(model_hf: str, local_api_port: int = 8000, api_key: str = "key123456", precision: str = "float16"):
    cmd = [
        "vllm", "serve", model_hf ,
        "--gpu-memory-utilization", "0.65",
        "--max-model-len", "2048",
        "--max-num-seqs", "64",
        "--optimization-level", "3",
        "--max-logprobs", "-1",
        "--stream-interval", "5",
        "--api-key", api_key,
        "--chat-template", "{% for message in messages %}{{ message['role'] }}: {{ message['content'] }}\n{% endfor %}{% if add_generation_prompt %}{{ '<|assistant|>' }}{% endif %}",  # Inline simple
        "--host", "0.0.0.0", "--port", str(local_api_port)



    ]
    _vllm_process = subprocess.run(cmd)


    # while(True):
    #     print("")
    #     sleep(10)
    #     pass
    # time.sleep(450)  # Más tiempo para cargar
    
    # # Verifica health
    # try:
    #     requests.get(f"http://localhost:{local_api_port}/health", timeout=5)
    # except:
    #     raise RuntimeError("vLLM server no responde en http://localhost:8000/health")
    
    # _client = OpenAI(
    #     base_url=f"http://localhost:{local_api_port}/v1",
    #     api_key=api_key
    # )
    
    # def kill_vllm():
    #     global _vllm_process
    #     if _vllm_process:
    #         _vllm_process.terminate()
    #         _vllm_process.wait()
    
    # atexit.register(kill_vllm)
    # return client_call


if __name__ == "__main__":
    #print("hola")
    torch.cuda.empty_cache()
    init_vllm(model_hf = "jinaai/reader-lm-0.5b")


#prompt_dict = {}


#prompt_dict = prompt_generator.generate_prompts()


#prompt_loader.load_prompt(prompts_dict = prompt_dict, num_prompts = 10, model = "arnir0/Tiny-LLM")


