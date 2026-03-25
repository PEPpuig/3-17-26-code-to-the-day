#!/bin/bash

source ~/venv/bin/activate

echo "Iniciando servidor vLLM en segundo plano..."
vllm serve $1 \
  --gpu-memory-utilization 0.75 \
  --max-model-len $2 \
  --max-num-seqs $3 \
  --optimization-level 3 \
  --max-logprobs -1 \
  --stream-interval 10 \
  --api-key "key123456" \
  --enable-mfu-metrics \
  --host 0.0.0.0 \
  --port 8000 &

VLLM_PID=$!

while ! curl -s http://localhost:8000/health > /dev/null; do
    sleep 5
done



python3 vllm_max_metrics.py &


python3 collect_latency_metrics.py &
LATENCY_PID=$!

python3 vllm_collect_metrics_csv.py &
METRICS_PID=$!


bash my_Script1.bash $4

kill $LATENCY_PID $METRICS_PID


python3 graph_gen_from_csv.py
python3 latency_graph_gen_from_csv.py




python3 model_params_dump.py

echo "Finalizado"

# Matar todos los procesos en segundo plano antes de salir
kill $VLLM_PID 



