source ~/venv/bin/activate

# Capturamos el T0 (Epoch en segundos con decimales)
T0=$(date +%s.%N)

for i in {1..512}
do
    python3 model_init_random.py $i $T0 &
done

wait
echo "Todas las llamadas finalizadas."
