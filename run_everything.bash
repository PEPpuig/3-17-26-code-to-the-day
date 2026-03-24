#!/bin/bash

source ~/venv/bin/activate

echo "Iniciando servidor vLLM en segundo plano..."
vllm serve jinaai/reader-lm-0.5b \
  --gpu-memory-utilization 0.75 \
  --max-model-len 512 \
  --max-num-seqs 8 \
  --optimization-level 3 \
  --max-logprobs -1 \
  --stream-interval 10 \
  --api-key "key123456" \
  --host 0.0.0.0 \
  --port 8000 &

VLLM_PID=$!

while ! curl -s http://localhost:8000/health > /dev/null; do
    sleep 5
done

# Iniciar los scripts de métricas y capturar sus PIDs
python3 collect_latency_metrics.py &
LATENCY_PID=$!

python3 vllm_collect_metrics_csv.py &
METRICS_PID=$!

bash my_Script1.bash

python3 model_params_dump.py

echo "Finalizado"

# Matar todos los procesos en segundo plano antes de salir
kill $VLLM_PID $LATENCY_PID $METRICS_PID