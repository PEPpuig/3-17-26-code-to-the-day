from vllm.engine.arg_utils import EngineArgs
import json

engine_args = EngineArgs(
    model="arnir0/Tiny-LLM",
    gpu_memory_utilization = 0.35,
    max_model_len=256,
)

config_dict = engine_args.__dict__
with open("run_config.json", "w") as f:
    json.dump(config_dict, f, indent=2, default=str)

print(json.dumps(config_dict, indent=2, default=str))
