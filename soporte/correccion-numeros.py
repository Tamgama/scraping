import pandas as pd
import requests
import time
import random
import json
import sys

# Cargar las cookies desde el archivo 'cookie.json'
try:
    with open('cookie.json', 'r') as cookie_file:
        config = json.load(cookie_file)
        cookie = config['cookie']
    cookie = cookie.encode('utf-8')
except FileNotFoundError:
    print("Error: No se encontró el archivo 'cookie.json'.")
    sys.exit(1)

# Configurar la sesión de requests con los headers necesarios
headers = {
    "authority": "www.idealista.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": cookie,
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-device-memory": "8",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/127.0.0.0 Safari/537.36"
}
session = requests.Session()
session.headers.update(headers)

def obtener_numero_telefono(id_inmueble):
    """
    Dado un id_inmueble, obtiene el número de teléfono asociado.
    Retorna el número de teléfono como string, o -1 si no se encuentra.
    """
    url = f"https://www.idealista.com/es/ajax/ads/{id_inmueble}/contact-phones"
    print(f"Procesando ID: {id_inmueble} - URL: {url}")

    try:
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud para el ID {id_inmueble}: {e}")
        return None

    # Verificar códigos de estado prohibidos
    if response.status_code in [403, 429]:
        print(f"Error {response.status_code}: Acceso prohibido o demasiadas solicitudes. "
              "El programa se detendrá.")
        sys.exit(1)

    # Introducir un retraso aleatorio entre solicitudes para evitar bloqueos
    time.sleep(random.uniform(1, 5))

    if response.status_code == 200:
        try:
            # Verificar si la respuesta es JSON válida
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                # Verificar si los datos del teléfono están presentes y son válidos
                if 'phone1' in data and data['phone1'] and 'number' in data['phone1']:
                    phone_number = data['phone1']['number']
                    print(f"Teléfono {phone_number} asignado para el ID de inmueble: {id_inmueble}")
                    return phone_number
                else:
                    print(f"No se encontró el número de teléfono para el ID de inmueble: {id_inmueble}. "
                          "Asignado -1.")
                    return -1
            else:
                print(f"Recibido HTML en lugar de JSON para el ID: {id_inmueble}")
                return -1
        except ValueError:
            print(f"Error al parsear la respuesta JSON para el ID de inmueble: {id_inmueble}")
            return -1
    else:
        print(f"Error {response.status_code} al obtener los datos para el ID de inmueble: {id_inmueble}.")
        # Detener el programa si se recibe un código de estado de error serio
        if response.status_code >= 400:
            print("El programa se detendrá debido a un error en la solicitud.")
            sys.exit(1)
        return -1

# Lista de archivos CSV a procesar
csv_files = ["../src/alquileres.csv", "../src/ventas.csv"]

for csv_path in csv_files:
    try:
        print(f"\nIntentando leer el archivo CSV en la ruta: {csv_path}")
        df = pd.read_csv(csv_path)
        print("Archivo CSV leído correctamente.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo CSV en la ruta {csv_path}")
        continue
    # Validar que las columnas 'Teléfono' e 'ID_Inmueble' existen
    if 'Teléfono' not in df.columns or 'ID_Inmueble' not in df.columns:
        print("Error: Las columnas 'Teléfono' o 'ID_Inmueble' no se encontraron en el archivo CSV.")
        continue
    # Filtrar solo las filas donde el teléfono esté vacío, sea 'N/A' o 0
    df_faltante = df[df['Teléfono'].isna() | (df['Teléfono'] == 'N/A') | (df['Teléfono'] == 0)]
    # Iterar sobre las filas filtradas
    for index, row in df_faltante.iterrows():
        id_inmueble = int(row['ID_Inmueble'])
        telefono = obtener_numero_telefono(id_inmueble)
        if telefono is not None:
            df.at[index, 'Teléfono'] = telefono
            # Guardar el archivo CSV actualizado después de cada cambio
            df.to_csv(csv_path, index=False)
    df.sort_values(by="fecha", ascending=False, inplace=True)
    df.to_csv(csv_path, index=False)
    print(f"Archivo CSV '{csv_path}' actualizado y guardado correctamente.")
