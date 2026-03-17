import torch
import subprocess
import time
import atexit

_vllm_process = None

def init_vllm_speculative(
    model_hf: str, 
    speculative_method: str = "none", # "ngram", "eagle", "draft"
    spec_model_id: str = None, 
    local_api_port: int = 8000, 
    api_key: str = "key123456"
):
    global _vllm_process
    
    # Comandos base de tu archivo
    cmd = [
        "vllm", "serve", model_hf,
        "--gpu-memory-utilization", "0.85", 
        "--max-model-len", "2048",
        "--max-num-seqs", "128",
        "--api-key", api_key,
        "--host", "0.0.0.0", 
        "--port", str(local_api_port)
    ]

    # 1. Configuración: Prompt Lookup Decoding (N-gram)
    # No requiere un segundo modelo, perfecto para 8GB VRAM.
    if speculative_method == "ngram":
        cmd.extend([
            "--speculative-model", "[ngram]",
            "--num-speculative-tokens", "5",
            "--ngram-prompt-lookup-max", "4"
        ])

    # 2. Configuración: Modelo de Cabecera (EAGLE o Medusa)
    # Requiere descargar los pesos de la cabecera acoplada al modelo base.
    elif speculative_method == "eagle" and spec_model_id:
        cmd.extend([
            "--speculative-model", spec_model_id,
            "--num-speculative-tokens", "5"
        ])

    # 3. Configuración: Draft tradicional (Draft-Target)
    # Peligroso para 8GB VRAM, requiere un modelo ultra pequeño (ej. 0.5B).
    elif speculative_method == "draft" and spec_model_id:
        cmd.extend([
            "--speculative-model", spec_model_id,
            "--num-speculative-tokens", "5",
            # Habilitar especulación entre distintos vocabularios si no son la misma familia
            "--speculative-draft-tensor-parallel-size", "1" 
        ])

    print(f"Lanzando vLLM con comando:\n{' '.join(cmd)}\n")
    _vllm_process = subprocess.Popen(cmd) # Usamos Popen para no bloquear el script main
    return _vllm_process

def kill_vllm():
    global _vllm_process
    if _vllm_process:
        print("Cerrando servidor vLLM...")
        _vllm_process.terminate()
        _vllm_process.wait()

atexit.register(kill_vllm)

if __name__ == "__main__":
    torch.cuda.empty_cache()
    
    TARGET_MODEL = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
    
    print("Elige el método de Speculative Decoding a lanzar (descomenta uno):")
    #OPCIÓN A: Modelo sin speculative decoding
    init_vllm_speculative(
        model_hf=TARGET_MODEL,
        speculative_method="none"
    )


    
    # OPCIÓN B: N-Gram / Prompt Lookup (La mejor opción para tus 8GB VRAM)
    #init_vllm_speculative(
    #    model_hf=TARGET_MODEL,
    #    speculative_method="ngram"
    #)
    
    # OPCIÓN C: EAGLE (Cabeceras predictivas)
    # init_vllm_speculative(
    #     model_hf=TARGET_MODEL,
    #     speculative_method="eagle",
    #     spec_model_id="yuhuili/EAGLE-Mistral-7B-Instruct-v0.2"
    # )
    
    # OPCIÓN D: Modelo Draft pequeño (Usando un modelo de 0.5B como borrador)
    # init_vllm_speculative(
    #     model_hf=TARGET_MODEL,
    #     speculative_method="draft",
    #     spec_model_id="Qwen/Qwen1.5-0.5B-Chat" # Modelo minúsculo que cabe junto al Mistral
    # )

    try:
        # Mantenemos el script vivo
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Interrupción detectada. Cerrando...")



#prompt_loader.load_prompt(prompts_dict = prompt_dict, num_prompts = 10, model = "arnir0/Tiny-LLM")


