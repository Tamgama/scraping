import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    'alquileres.py',
    'ventas.py',
    'limpieza.py',
    'actualizar_web.py',
]

for script in scripts:
    try:
        print(f"Ejecutando {script}...")
        # Llamar a los scripts con el intérprete del entorno virtual activo
        result = subprocess.run(['python3', script], check=True, capture_output=True, text=True)
        print(result.stdout)  # Imprime la salida estándar del script
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script}: {e}")
        print(e.stderr)  # Imprime el error estándar si ocurre