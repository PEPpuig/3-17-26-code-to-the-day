#!/bin/bash

source ~/venv/bin/activate

MODEL_NAME="Qwen/Qwen1.5-4B-Chat-AWQ"
GPU_MEM_UTIL=0.75
MAX_MODEL_LEN=512
MAX_NUM_SEQS=8
OPT_LEVEL=3
MAX_LOGPROBS=-1
STREAM_INTERVAL=10
API_KEY="key123456"
HOST="0.0.0.0"
PORT=8000

echo "Iniciando servidor vLLM en segundo plano..."
vllm serve "$MODEL_NAME" \
  --gpu-memory-utilization "$GPU_MEM_UTIL" \
  --max-model-len "$MAX_MODEL_LEN" \
  --max-num-seqs "$MAX_NUM_SEQS" \
  --optimization-level "$OPT_LEVEL" \
  --max-logprobs "$MAX_LOGPROBS" \
  --stream-interval "$STREAM_INTERVAL" \
  --api-key "$API_KEY" \
  --host "$HOST" \
  --port "$PORT" &

VLLM_PID=$!

while ! curl -s http://localhost:8000/health > /dev/null; do
  sleep 5
done

python3 vllm_max_metrics.py &
MAX_METRICS_PID=$!

python3 collect_latency_metrics.py &
LATENCY_PID=$!

python3 vllm_collect_metrics_csv.py &
METRICS_PID=$!

bash my_Script1.bash

kill $LATENCY_PID $METRICS_PID $MAX_METRICS_PID

python3 model_params_dump.py \
  --model "$MODEL_NAME" \
  --gpu-memory-utilization "$GPU_MEM_UTIL" \
  --max-model-len "$MAX_MODEL_LEN" \
  --max-num-seqs "$MAX_NUM_SEQS" \
  --optimization-level "$OPT_LEVEL" \
  --max-logprobs "$MAX_LOGPROBS" \
  --stream-interval "$STREAM_INTERVAL"

python3 latency_graph_gen_from_csv.py
python3 graph_gen_from_csv.py

echo "Finalizado"

kill $VLLM_PID $LATENCY_PID $METRICS_PID
