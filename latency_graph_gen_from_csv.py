import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "vllm_metrics.csv"


df = pd.read_csv(CSV_PATH)
print(f"Datos cargados: {len(df)} filas")


fig, ax1 = plt.subplots(figsize=(15, 7))


fig.subplots_adjust(right=0.75)

# Eje izquierdo: requests (AZUL)
line1 = ax1.plot(df['t_rel'], df['num_reqs_running'], 'b-o', markersize=4, linewidth=2, label='num reqs run')
ax1.set_xlabel('Tiempo relativo (s)')
ax1.set_ylabel('Número de requests', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, alpha=0.3)

# Eje derecho 1 (ax2): Throughput / e2e_latency (MORADO)
ax2 = ax1.twinx()
line2 = ax2.plot(df['t_rel'], df['e2e_latency'], 'm-o', markersize=4, linewidth=2, label='e2e_latency (s)')
ax2.set_ylabel('e2e_latency (s)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

# Eje derecho 2 (ax3): KV Cache % (VERDE)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
line3 = ax3.plot(df['t_rel'], df['kv_cache_perc'], 'g-o', markersize=4, linewidth=2, label='kv cache usage')
ax3.set_ylabel('KV Cache %', color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.set_ylim(0, 1)

# Eje derecho 3 (ax4): Inter Token Latency (NARANJA)
ax4 = ax1.twinx()
ax4.spines['right'].set_position(('outward', 120))
line4 = ax4.plot(df['t_rel'], df['Inter_Token_Latency'], color='darkorange', marker='s', linestyle='-', markersize=4, linewidth=2, label='inter_token_lat')
ax4.set_ylabel('Inter Token Latency', color='darkorange')
ax4.tick_params(axis='y', labelcolor='darkorange')

plt.title('vLLM: Requests vs Latencies vs KV Cache Usage')

# Leyenda combinada para todas las líneas
lines = line1 + line2 + line3 + line4
labels = [l.get_label() for l in lines]
fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
           ncol=4, fontsize=10, frameon=False)


plt.savefig('vllm_grafico_completo.png', dpi=300, bbox_inches='tight')
plt.show()

print("¡Gráfico actualizado guardado como 'vllm_grafico_completo.png'!")
