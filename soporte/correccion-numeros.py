import pandas as pd
import requests
import time
import random
import json
import sys

# Cargar las cookies desde el archivo 'cookie.json'
# try:
#     with open('cd cookie.json', 'r') as cookie_file:
#         config = json.load(cookie_file)
#         cookie = config['cookie']
#     cookie = cookie.encode('utf-8')
# except FileNotFoundError:
#     print("Error: No se encontró el archivo 'cookie.json'.")
#     sys.exit(1)

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
    "cookie": "userUUID=354ebf7b-4a28-495f-badd-716c43f9e8a2; SESSION=733bddb87ea43a90~b331161f-0456-4eb1-86a1-9bd28074b218; utag_main__sn=1; utag_main_ses_id=1747737852267%3Bexp-session; utag_main__prevTsUrl=https%3A%2F%2Fwww.idealista.com%2F%3Bexp-1747741452281; utag_main__prevTsReferrer=%3Bexp-1747741452281; utag_main__prevTsSource=Direct traffic%3Bexp-1747741452281; utag_main__prevTsCampaign=organicTrafficByTm%3Bexp-1747741452281; utag_main__prevTsProvider=%3Bexp-1747741452281; utag_main__ss=0%3Bexp-session; utag_main__prevEventLink=; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1xa3N4Nzl1fG1hd2R6cHh1In0%3D; _pcid=%7B%22browserId%22%3A%22mawdzpxax7479akr%22%2C%22_t%22%3A%22mqksx7fk%7Cmawdzq3k%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAI4BrCAA8A7ADN%2BAH36EA7qwBeggMz8QAXyA; didomi_token=eyJ1c2VyX2lkIjoiMTk2ZWQ0YjMtOGFiMS02MTExLTg0NjgtMWJhZGNkOTJiNzZhIiwiY3JlYXRlZCI6IjIwMjUtMDUtMjBUMTA6NDQ6MTIuMDc1WiIsInVwZGF0ZWQiOiIyMDI1LTA1LTIwVDEwOjQ0OjEzLjM2OVoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQRtbwAQRtbwAAHABBENBrFgAAAAAAAAAAAAAAAAAACkoAMAAQWbKQAYAAgs2QgAwABBZsdABgACCzYSADAAEFmw.YAAAAAAAAAAA; utag_main__pn=2%3Bexp-session; utag_main__se=5%3Bexp-session; utag_main__st=1747739850233%3Bexp-session; utag_main__prevEventView=010-idealista/home > portal > > > > viewHome%3Bexp-1747741650243; utag_main__prevLevel2=010-idealista/home%3Bexp-1747741650243; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-05-20T10%3A47%3A30.295Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22MSdZjYtqZNWgXOhJRdn5%22%2C%22expiryDate%22%3A%222026-05-20T10%3A47%3A30.296Z%22%7D; datadome=YPAzPkTiX7aiOHjsx_ubo~tvu23I_Xs1XBznDO5AJ~7EkFawl_KXkzF5O495Qhax87PG3Zkavi5Il_BNQ~lW~Gy0YiI3DGU7Nii2ERjgswudGiD02hDsFF7Xl1KW0stg",
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
    Dado un id_inmueble, obtiene el número de tlf asociado.
    Retorna el número de tlf como string, o -1 si no se encuentra.
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
                # Verificar si los datos del tlf están presentes y son válidos
                if 'phone1' in data and data['phone1'] and 'number' in data['phone1']:
                    phone_number = data['phone1']['number']
                    print(f"tlf {phone_number} asignado para el ID de inmueble: {id_inmueble}")
                    return phone_number
                else:
                    print(f"No se encontró el número de tlf para el ID de inmueble: {id_inmueble}. "
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
    # Validar que las columnas 'tlf' e 'id_inmueble' existen
    if 'tlf' not in df.columns or 'id_inmueble' not in df.columns:
        print("Error: Las columnas 'tlf' o 'id_inmueble' no se encontraron en el archivo CSV.")
        continue
    # Filtrar solo las filas donde el tlf esté vacío, sea 'N/A' o 0
    df_faltante = df[df['tlf'].isna() | (df['tlf'] == 'N/A') | (df['tlf'] == 0)]
    # Iterar sobre las filas filtradas
    for index, row in df_faltante.iterrows():
        id_inmueble = int(row['id_inmueble'])
        telefono = obtener_numero_telefono(id_inmueble)
        if telefono is not None:
            df.at[index, 'tlf'] = telefono
            # Guardar el archivo CSV actualizado después de cada cambio
            df.to_csv(csv_path, index=False)
    df.sort_values(by="fecha", ascending=False, inplace=True)
    df.to_csv(csv_path, index=False)
    print(f"Archivo CSV '{csv_path}' actualizado y guardado correctamente.")
