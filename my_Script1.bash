#!/bin/bash
source ~/venv/bin/activate

# Capturamos el T0 (Epoch en segundos con decimales)
T0=$(date +%s.%N)

# Supongamos que tenías 200 llamadas en tu archivo original. 
# Lanzamos 200 procesos concurrentes pasando su ID (i) y el T0 ($T0)
for i in {1..256}
do
    python3 model_init_random.py $i $T0 &
done

# Esperamos a que todos los procesos de fondo terminen
wait
echo "Todas las llamadas finalizadas."
