import pandas as pd
import matplotlib.pyplot as plt


CSV_PATH = "vllm_metrics.csv"

# Leer datos del archivo CSV
df = pd.read_csv(CSV_PATH)
print(f"Datos cargados: {len(df)} filas")


fig, ax1 = plt.subplots(figsize=(14, 7))

# Eje izquierdo: requests (AZUL waiting, ROJO running)
line1 = ax1.plot(df['t_rel'], df['num_reqs_waiting'], 'b-o', markersize=4, linewidth=2, label='num reqs wait')
line2 = ax1.plot(df['t_rel'], df['num_reqs_running'], 'r-o', markersize=4, linewidth=2, label='num reqs run')
ax1.set_xlabel('Tiempo relativo (s)')
ax1.set_ylabel('Número de requests', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True, alpha=0.3)

# Eje derecho 1 (ax2): Throughput (MORADO)
ax2 = ax1.twinx()
line3 = ax2.plot(df['t_rel'], df['throughput'], 'm-o', markersize=4, linewidth=2, label='throughput (tokens/s)')
ax2.set_ylabel('Throughput (tokens/s)', color='purple')
ax2.tick_params(axis='y', labelcolor='purple')

# Eje derecho 2 (ax3) para KV Cache % (VERDE)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
line4 = ax3.plot(df['t_rel'], df['kv_cache_perc'], 'g-o', markersize=4, linewidth=2, label='kv cache usage')
ax3.set_ylabel('KV Cache %', color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.set_ylim(0, 1)


plt.title('Requests vs Throughput vs KV Cache Usage')
lines = line1 + line2 + line3 + line4
labels = [l.get_label() for l in lines]
fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.05),
           ncol=4, fontsize=10, frameon=False)


plt.tight_layout()
plt.savefig('vllm_grafico_completo.png', dpi=300, bbox_inches='tight')
plt.show()

print("¡Gráfico perfecto guardado como 'vllm_grafico_completo.png'!")
