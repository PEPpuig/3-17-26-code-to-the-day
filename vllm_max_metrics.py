import requests
import time
import csv
import sys

# Tus diccionarios de mapeo
VLLM_METRIC_MAP = {
    "vllm_kv_cache_utilization": "vllm:kv_cache_usage_perc",
    "vllm_prefix_cache_hits": "vllm:prefix_cache_hits_total",
    "vllm_prefix_cache_queries": "vllm:prefix_cache_queries_total",
    "vllm_num_preemptions": "vllm:num_preemptions",
    "vllm_prompt_tokens_recomputed": "vllm:prompt_tokens_recomputed",
    "vllm_num_requests_running": "vllm:num_requests_running",
    "vllm_num_requests_waiting": "vllm:num_requests_waiting",
}

VLLM_METRIC_FALLBACKS = {
    "vllm_num_preemptions": ("vllm:num_preemptions_total",),
    "vllm_prefix_cache_hits": ("vllm:prefix_cache_hits",),
    "vllm_prefix_cache_queries": ("vllm:prefix_cache_queries",),
    "vllm_prompt_tokens_recomputed": ("vllm:prompt_tokens_recomputed_total",),
}

VLLM_MFU_METRIC_MAP = {
    "vllm_estimated_flops_per_gpu_total": "vllm:estimated_flops_per_gpu_total",
    "vllm_estimated_read_bytes_per_gpu_total": "vllm:estimated_read_bytes_per_gpu_total",
    "vllm_estimated_write_bytes_per_gpu_total": "vllm:estimated_write_bytes_per_gpu_total",
}

# Configuración
METRICS_URL = "http://localhost:8000/metrics"
POLL_INTERVAL = 1.0  # Frecuencia de muestreo en segundos
CSV_FILENAME = "max_metrics.csv"

def main():
    # 1. Recopilar todas las claves de Prometheus posibles (principales y fallbacks)
    prom_keys = list(VLLM_METRIC_MAP.values()) + list(VLLM_MFU_METRIC_MAP.values())
    for fallbacks in VLLM_METRIC_FALLBACKS.values():
        prom_keys.extend(fallbacks)
        
    # Inicializar el rastreador de valores máximos a 0.0
    max_prom_values = {key: 0.0 for key in set(prom_keys)}

    print(f"[*] Iniciando monitor de métricas vLLM en {METRICS_URL}")
    print(f"[*] Frecuencia de actualización: {POLL_INTERVAL}s")
    print("[*] Presiona Ctrl+C o cierra el servidor vLLM para finalizar y guardar el CSV...\n")

    try:
        while True:
            try:
                # Obtener métricas expuestas
                response = requests.get(METRICS_URL, timeout=2)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                print("\n[!] Conexión perdida con vLLM. Asumiendo que el proceso terminó.")
                break

            # 2. Parsear el texto plano de Prometheus
            for line in response.text.split('\n'):
                line = line.strip()
                # Ignorar comentarios o líneas vacías
                if not line or line.startswith('#'):
                    continue
                
                # Las líneas de Prometheus tienen el formato: metric_name{labels="x"} value
                parts = line.split()
                if len(parts) >= 2:
                    metric_expr = parts[0]
                    value_str = parts[1]
                    
                    # Extraer solo el nombre de la métrica (limpiando las etiquetas)
                    metric_name = metric_expr.split('{')[0]
                    
                    if metric_name in max_prom_values:
                        if value_str.lower() != 'nan':
                            val = float(value_str)
                            # Si es un modelo multi-GPU, Prometheus emite la misma métrica con distintas labels.
                            # Nos quedamos con el máximo global detectado.
                            if val > max_prom_values[metric_name]:
                                max_prom_values[metric_name] = val

            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n[!] Monitoreo interrumpido manualmente por el usuario.")

    # 3. Mapear de vuelta a tus nombres internos resolviendo fallbacks
    final_metrics = {}
    all_internal_maps = {**VLLM_METRIC_MAP, **VLLM_MFU_METRIC_MAP}
    
    for internal_name, prom_name in all_internal_maps.items():
        # Valor base de la métrica principal
        best_val = max_prom_values.get(prom_name, 0.0)
        
        # Comprobar si los fallbacks tienen un valor mayor
        if internal_name in VLLM_METRIC_FALLBACKS:
            for fallback_prom_name in VLLM_METRIC_FALLBACKS[internal_name]:
                fallback_val = max_prom_values.get(fallback_prom_name, 0.0)
                if fallback_val > best_val:
                    best_val = fallback_val
                    
        final_metrics[internal_name] = best_val

    # 4. Guardar resultados en CSV
    with open(CSV_FILENAME, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["metric_key", "max_value"])
        for k, v in final_metrics.items():
            writer.writerow([k, v])
            
    print(f"[*] Resultados máximos guardados exitosamente en '{CSV_FILENAME}'.")

if __name__ == "__main__":
    main()
