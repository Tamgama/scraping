import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    'obtencion_inmuebles.py',
    # 'alquileres.py',
    # 'ventas.py',
    # 'correccion-numeros.py',
    # 'limpieza.py',
    'particulares/particulares.py',
    'obtener_inmuebles_fotocasa.py',
    'obtencion_almeria.py',
    'obtencion_alicante.py',
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