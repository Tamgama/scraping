import pandas as pd
import requests
import time
import random

headers = {
    "authority": "www.idealista.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": "userUUID=f784004d-fd85-40c5-bfa0-3d2a9ad1c125; _last_search=officialZone; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1oMzJva2g5fG0xZW5yMzU5In0%3D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22xUju80WjymLwBmCZIvDM%22%7D; _pcid=%7B%22browserId%22%3A%22m1enr357f2d4699a%22%2C%22_t%22%3A%22mh32ol01%7Cm1enr3o1%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbABYBmAEyVUABmEAffgEYoSGMMrCQAXyA; didomi_token=eyJ1c2VyX2lkIjoiMTkyMWRhZTQtMzVlOS02YmUxLWI2NzYtYjA4ZDQwYWU0NzNjIiwiY3JlYXRlZCI6IjIwMjQtMDktMjNUMDc6MDA6MTIuNzY2WiIsInVwZGF0ZWQiOiIyMDI0LTA5LTIzVDA3OjQxOjU5Ljk0MFoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQFZtsAQFZtsAAHABBENBHFgAAAAAAAAAAAAAAAAAACkoAMAAQU3KQAYAAgpuQgAwABBTcdABgACCm4SADAAEFNw.YAAAAAAAAAAA; utag_main__sn=2; contact95d1e63a-7d07-4e75-a334-5860d75d2119=\"{'maxNumberContactsAllow':10}\"; send95d1e63a-7d07-4e75-a334-5860d75d2119=\"{}\"; SESSION=1b732e08a8140e05~95d1e63a-7d07-4e75-a334-5860d75d2119; cookieSearch-1=\"/alquiler-viviendas/murcia/pedanias-norte/espinardo/:1727077339696\"; utag_main__prevCompleteClickName=005-idealista/portal > portal > seePhotos; datadome=i8IBIe6QTKjdIrIVOWXYP9ae0KawHupLGkXY8Ytg0PNAMBH~HzWmXOHtNbBgnj0lBkGKR47I_5gnqBL6fKBs3ZT6~QNb~4pUxsMmtPIrAZq8QR1vo_mzcRcc8bNDLd2m",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-device-memory": "8",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.88\", \"Chromium\";v=\"127.0.6533.88\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}


# Crear sesión
session = requests.Session()
session.headers.update(headers)

# Leer el archivo CSV
df = pd.read_csv("scraping/src/data.csv")

# Definir la URL base para obtener el número de teléfono
url_base = "https://www.idealista.com/es/ajax/ads/{}/contact-phones"

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    # Verificar si falta el número de teléfono (vacío o N/A)
    if pd.isna(row['tlf']) or row['tlf'] == 'N/A':
        id_inmueble = int(row['id'])
        url = url_base.format(id_inmueble)   
        
        # Hacer la solicitud para obtener el número de teléfono
        print(f"Procesando ID: {id_inmueble} - URL: {url}")
        response = session.get(url)
        
        # Introducir un retraso aleatorio entre solicitudes para evitar bloqueos
        time.sleep(random.uniform(1, 5))  
        
        if response.status_code == 200:
            try:
                # Intentar obtener y parsear los datos JSON
                data = response.json()
                # Verificar si los datos del teléfono están presentes
                if 'phone1' in data and data['phone1'] and 'number' in data['phone1']:
                    phone_number = data['phone1']['number']
                    df.at[index, 'tlf'] = phone_number  # Actualizar en el DataFrame
                    print(f"Teléfono {phone_number} asignado para el ID de inmueble: {id_inmueble}")
                else:
                    print(f"No se encontró el número de teléfono para el ID de inmueble: {id_inmueble}")
            except ValueError:
                print(f"Error al parsear la respuesta JSON para el ID de inmueble: {id_inmueble}")
        else:
            print(f"Error {response.status_code} al obtener los datos para el ID de inmueble: {id_inmueble}")

# Guardar el archivo CSV actualizado solo una vez después de procesar todos los inmuebles
df.to_csv('scraping/src/data.csv', index=False)
print("Archivo CSV actualizado guardado correctamente.")
