import requests
import json
import sys
from vllm.engine.arg_utils import EngineArgs

def main():
    config = {}
    
    try:
        # Intentar leer del servidor vLLM real
        print("Leyendo config del servidor vLLM...")
        models_resp = requests.get("http://localhost:8000/v1/models", timeout=5)
        health_resp = requests.get("http://localhost:8000/health", timeout=5)
        
        if models_resp.status_code == 200:
            config['models'] = models_resp.json()['data']
            config['model_name'] = config['models'][0]['id'] if config['models'] else 'unknown'
        config['health'] = health_resp.json()
        print(f"✓ Modelo real: {config.get('model_name', 'unknown')}")
        
    except Exception as e:
        print(f"✗ Error servidor: {e}. Usando fallback EngineArgs.")
        # Fallback: los params ORIGINALES hardcodeados (o pasa desde bash)
        engine_args = EngineArgs(
            model="Qwen/Qwen1.5-4B-Chat-AWQ",
            gpu_memory_utilization=0.75,  # ← CAMBIA A LOS DE TU BASH
            max_model_len=512,
            max_num_seqs=8,
            optimization_level=3,
            max_logprobs=-1,
            stream_interval=10
        )
        config = engine_args.__dict__
    
    # SIEMPRE guardar
    with open("run_config.json", "w") as f:
        json.dump(config, f, indent=2, default=str)
    
    print("\nConfig guardada:")
    print(json.dumps(config, indent=2, default=str))

if __name__ == "__main__":
    main()
