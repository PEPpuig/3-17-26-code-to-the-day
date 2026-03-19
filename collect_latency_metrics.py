#!/usr/bin/env python3
import requests
import time
import re
import os
import csv

METRICS_URL = "http://localhost:8000/metrics"
CSV_FILE = "vllm_latency_metrics.csv"
INTERVAL = 0.1
THROUGHPUT_INTERVAL = 1.0

start_time = time.time()

# Crear el archivo y la cabecera si no existe
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['t_rel', 'num_reqs_running', 'Inter_Token_Latency', 'kv_cache_perc', 'e2e_latency'])

def get_value(lines, metric_substr):
    for line in lines:
        if metric_substr in line:
            match = re.search(r'\{[^}]+\}\s+([\d.e+-]+)', line)
            if match:
                return float(match.group(1))
    return 0.0

prev_tokens = 0
prev_time = time.time()
throughput = 0.0
prev_throughput = 0.0
iteration = 1.0
e2e_latency = 0.0  # INICIALIZACIÓN: Evita que falle en las primeras iteraciones

while True:
    try:
        resp = requests.get(METRICS_URL, timeout=2)
        lines = resp.text.splitlines()

        running = get_value(lines, 'vllm:num_requests_running')
        Inter_Token_Latency = get_value(lines, 'vllm:inter_token_latency_seconds_sum')/iteration
        kv_perc = get_value(lines, 'vllm:kv_cache_usage_perc')
        e2e_latency_sum = get_value(lines, 'vllm:e2e_request_latency_seconds_sum')
        current_time = time.time()
        e2e_latency = (e2e_latency_sum) / iteration
        t_rel = round(time.time() - start_time, 2)
        iteration = iteration + 1
        
        # Guardar en el CSV
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                t_rel,
                round(running, 5),
                round(Inter_Token_Latency, 5),
                round(kv_perc, 5),
                round(e2e_latency_sum, 5)
            ])

    except Exception as e:
        # Imprime el error por pantalla en lugar de fallar silenciosamente
        print(f"Error capturado: {e}")

    time.sleep(INTERVAL)
