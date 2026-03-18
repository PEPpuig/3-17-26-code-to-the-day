import csv
import matplotlib.pyplot as plt

CSV_FILE = "prompt_timings.csv"

def main():
    prompts_original = []
    starts = []
    durations = []
    ends = []
    # Leer y extraer los datos del CSV
    try:
        with open(CSV_FILE, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p_id = int(row['prompt'])
                start_time = float(row['start'])
                end_time = float(row['end'])
                
                prompts_original.append(p_id)
                starts.append(start_time)
                durations.append(end_time - start_time)
                ends.append(end_time)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {CSV_FILE}")
        return

    
    datos = sorted(zip(starts, duration, ends, prompts_original))
    starts, duration, ends, prompts_ordenados = zip(*datos)

    # Crear la figura
    fig, ax = plt.subplots(figsize=(12, 8))

    posiciones_y = range(len(prompts_ordenados))

    # Generar colores de la paleta tab20
    cmap = plt.get_cmap('tab20')
    colores = [cmap(i % 20) for i in range(len(prompts_ordenados))]

    ax.barh(posiciones_y, durations, left=starts, height=0.5, color=colores, 
            edgecolor='black', linewidth=0.5, alpha=0.9)

    etiquetas_y = [f"P-{pid}" for pid in prompts_ordenados]
    ax.set_yticks(posiciones_y)
    ax.set_yticklabels(etiquetas_y, fontsize=10)

    # Configurar el resto del diseño
    ax.set_xlabel('Tiempo relativo (segundos)', fontsize=12)
    ax.set_ylabel('Prompts', fontsize=12)
    ax.set_title('Tiempos de Procesamiento (Ordenados por Final)', fontsize=14)
    
    # Invertir el eje Y (para que el que empieza antes quede arriba del todo)
    ax.invert_yaxis()
    
    # Añadir cuadrícula
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()

    # Guardar y mostrar
    output_image = 'gantt_prompts_orden_inicio.png'
    plt.savefig(output_image, dpi=300)
    print(f"Gráfico guardado como '{output_image}'.")
    
    plt.show()

if __name__ == "__main__":
    main()
