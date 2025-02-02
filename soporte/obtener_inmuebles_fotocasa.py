import requests
import re
import json
import time
import random
from datetime import datetime

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "max-age=0",
    "cookie": 'cu=es-es; ajs_anonymous_id=e24007b4-48cf-4707-9efa-c7d2a0c14e6d; _fbp=fb.1.1738339157798.520247286968388148; didomi_token=eyJ1c2VyX2lkIjoiMTk0YmQxNjgtMzcwYi02MzQwLTkwZjctZjU4Mzc4MzYyNmM3IiwiY3JlYXRlZCI6IjIwMjUtMDEtMzFUMTU6NTk6MTYuODQ4WiIsInVwZGF0ZWQiOiIyMDI1LTAxLTMxVDE1OjU5OjIwLjU5MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmFkZXZpbnRhLW1vdG9yLW1vdG9yIiwiYzptZXRhcGxhdGYtTlJlVnBtTFEiLCJjOmNyaXRlby1QNDhlR1QydyIsImM6Z29vZ2xlaXJlLWZmS2FQYVJEIl19LCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiLCJnZW9sb2NhdGlvbl9kYXRhIiwidHJhbnNmZXItdG8tbW90b3IiLCJ1c29kZWxvcy1RcExwTThqVyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwidmVyc2lvbiI6Mn0=; euconsent-v2=CQMGLkAQMGLkAAHABBENBaFsAP_gAEPgAAiQKxtX_G__bWlr8X73aftkeY1P99h77sQxBhbJE-4FzLvW_JwXx2E5NA36tqIKmRIAu3TBIQNlHJDURVCgaogVrSDMaEyUoTNKJ6BkiFMRI2dYCFxvm4tjeQCY5vr991dx2B-t7dr83dzyy4hHn3a5_2S0WJCdA5-tDfv9bROb-9IOd_x8v4v4_F7pE2_eT1l_tWvp7D9-cts_9XW99_fbff9Pn_-uB_-_X_vf_H37gq-ASYaFRAGWBISEGgYQQIAVBWEBFAgCAABIGiAgBMGBTsDABdYSIAQAoABggBAACDIAEAAAEACEQAQAFAgAAgECgADAAgGAgAIGAAEAFgIBAACA6BimBBAIFgAkZkVCmBCEAkEBLZUIJAECCuEIRZ4BEAiJgoAAAAACkAAQFgsDiSQEqEggC4gmgAAIAEAggAKEEnJgACAM2WoPBk2jK0wDB8wSIaYBkARBGQkGgAAA.f_wACHwAAAAA; _gcl_au=1.1.1003412851.1738339161; segment_ga=GA1.1.791422271.1738339161; kanirante-adv-aauid=7a883939-7e66-4c32-8804-3d7c807589c0; adit-xandr-id=761685332701469910; _lr_env_src_ats=false; sui_1pc=1738339161130135AF0DD180BFA49ED5B8F2F54CD24C4D1AE7B89BEB; __gsas=ID=3602a79559ea2bbd:T=1738339161:RT=1738339161:S=ALNI_MYNf_9-bq_3mvQCyBeoBaw0Woqfhw; ASP.NET_SessionId=td3n2pvybdw1jz1o2hpzw0o4; auth=td3n2pvybdw1jz1o2hpzw0o4; _hjSessionUser_89611=eyJpZCI6ImZmYjFkNDNjLTAxODgtNTdhNi05MDA5LTVhN2JiNTRmNmFmNiIsImNyZWF0ZWQiOjE3MzgzNDEzMDU5MzIsImV4aXN0aW5nIjp0cnVlfQ==; _lr_sampling_rate=100; usunico=01/02/2025:19-0986645; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C20122%7CMCMID%7C50316837995770300660582095743361496031%7CMCAAMLH-1739091796%7C6%7CMCAAMB-1739091796%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1738494196s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjoxLCJwdXJwb3NlIjp7ImNvbnNlbnRzIjp7IjEiOnRydWUsIjIiOnRydWUsIjMiOnRydWUsIjQiOnRydWUsIjUiOnRydWUsIjYiOnRydWUsIjciOnRydWUsIjgiOnRydWUsIjkiOnRydWUsIjEwIjp0cnVlfX0sInNwZWNpYWxGZWF0dXJlcyI6eyIxIjp0cnVlfX0=; _csrf=SxXMaWEckyoir5zd1mLvhiNWf1RTQeAM08ooNOZXa/YKW63ULP/FIxDnqdm8XYuxy9DDEDRWmKAyroJODjslI7eR81WitLZ+TbJz+qaD7bg=; ab.storage.deviceId.c9f9127d-989c-45fe-96f2-f36434db5025=g%3A2a822b2e-c4d7-40c9-359c-23b7b4a3088b%7Ce%3Aundefined%7Cc%3A1738339157252%7Cl%3A1738486997210; ShowMap=false; segment_ga_MH0GDRSFGC=GS1.1.1738486996.7.0.1738492034.60.0.0; ab.storage.sessionId.c9f9127d-989c-45fe-96f2-f36434db5025=g%3Abbb56631-c416-8b76-b1fc-85ab05f1fa01%7Ce%3A1738493836082%7Cc%3A1738486997209%7Cl%3A1738492036082; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22tLrNk5Sy9sMhG1XbzbjN%22%2C%22expiryDate%22%3A%222026-02-02T10%3A27%3A16.176Z%22%7D; cto_bundle=10XhFF9wZmdSTmZUUVpBcm1wbXh6bkpFOHRSUWNiYjFzaXZZNUk3S2RLM01UV1h6cXBaWXRhRlJycXF0d3NUOHBvJTJGUXY2M2N4ZVBOak9rUUNTWEJXa0NkJTJGdWE4cVUwSDI1aWd0eHBFVVRFVzBBN3VZTjlDNFhEbm9HaGJFa21QcWk5QWpjR09SWmlwZXVHbGNjMGsyOHh3RjVBJTNEJTNE; __gads=ID=109f959d72de702f:T=1738339161:RT=1738492036:S=ALNI_MbYXbQHld9Xeq2RgSGGq8iMEjhDHg; __gpi=UID=0000102acbadd9f5:T=1738339161:RT=1738492036:S=ALNI_MYhDQA1l8gbr7ZxE3NWCoyzn3JHtA; __eoi=ID=3d7ca7519b1918d9:T=1738339161:RT=1738492036:S=AA-AfjbXQnfwCBirWxkc7rAbyh2B; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-02-02T10%3A27%3A19.897Z%22%7D; reese84=3:YkX60PLlnHMwMy344+DTaA==:LkSr0Vybp9mTbfKQCUs0ko/BzcNZSZLVS0GR4H70xjuoY/O690XOM2a4+XCjTk1XCDa2BRX7H99oVA2EFU9omadcs1zykrsgh9XFaaT1gkelEkEg4/xbPC5zh3kbi+8EBNwVZbPdas6HWn11CQT8BBo+6Ei9rRUIOazDqWKRX37Rbqx9MULBjipRZoYVqptJv2MkfEgJazNB74oGvBkXDKbxSYMyIHDBm3YcN8X+lQ2Wg87CqK7QIxDqIdoyNqtliI0g/jgmV4R28HrtlkmEY0VihxLp/4mstnC6gQ8rK4DVFJZWi6jVkRQAR6EO0HkxMPKaYcwKZgT/18RYVk7DWU5uNj4iP3p3qC5Uv+69smREy6BTiSbDCtkqxcCZpMtWjeoB/UrdcsJsjd9/SKJEWuciTajOsPTwVd8so3mW43gGhBP8KZsx6KsCt48eR/mowd4uaJxvVvqsBz2A5NuDIQ==:aCusWdida3XSp5XWB7fQvylXfawtD4XhNUbFoxAkEPE='.encode('utf-8'),
    "Referer": "https://www.fotocasa.es/es/alquiler/viviendas/murcia-provincia/todas-las-zonas/l",
    "Sec-Ch-Device-Memory": "4",
    "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.120", "Chromium";v="127.0.6533.120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "X-Height": "9999",  # Establece el valor de height
    "X-Width": "1920",   # Puedes agregar otros parámetros, como width
    "X-Depth": "500",    # Ejemplo de parámetro depth, si es necesario
    "X-Color": "blue",   # Ejemplo de parámetro de color, si lo deseas
    "X-Orientation": "landscape"  # Otro ejemplo, si necesitas un parámetro de orientación
}

# Variable global para la URL base de la API
api_base_url = "http://euspay.com/api/v1/euspay.php"
auth_credentials = ("promurcia", "Pr0Murc14")  # Sustituye por tu usuario y contraseña


# ==========================
# 🔹 FUNCIONES AUXILIARES
# ==========================

def obtener_tipo_inmueble(buildingType, buildingSubtype):
    tipos = {
        "Flat": "Piso",
        "House": "Casa",
        "Duplex": "Dúplex",
        "Penthouse": "Ático",
        "Studio": "Estudio",
        "Villa": "Villa"
    }
    
    subtipos = {
        "Apartment": "Apartamento",
        "TerracedHouse": "Casa adosada",
        "DetachedHouse": "Casa independiente",
        "SemidetachedHouse": "Casa Semi-Independiente",
        "Loft": "Loft",
        "Farmhouse": "Casa de campo",
        "Townhouse": "Casa de pueblo"
    }

    return subtipos.get(buildingSubtype, tipos.get(buildingType, "Desconocido"))

def obtener_tipo_contacto(clientTypeId):
    tipos_contacto = {
        1: "Particular",
        2: "Promotora",
        3: "Inmobiliaria",
        4: "Banco"
    }
    return tipos_contacto.get(clientTypeId, "Desconocido")

def obtener_estado(conservationStatus):
    estados = {
        1: "Desconocido",
        2: "Muy Bien",
        3: "Bien",
        4: "Desconocido",
        8: "Reformado"
    }
    return estados.get(conservationStatus, "Desconocido")

def obtener_antiguedad(antiguedad):
    tipos_antiguedad = {
        1: "Menos de 1 año",
        2: "1 a 5 años",
        3: "5 a 10 años",
        4: "10 a 20 años",
        5: "20 a 30 años",
        6: "30 a 50 años"
    }
    return tipos_antiguedad.get(antiguedad, "Desconocido")

def obtener_orientacion(orientacion):
    tipos_orientacion = {
        1: "Norte",
        4: "Sur",
        7: "Este",
        10: "Oeste"
    }
    return tipos_orientacion.get(orientacion, "Desconocido")

# ==========================
# 🔹 EXTRACCIÓN DE DATOS DEL INMUEBLE
# ==========================

def extract_property_info(data):
    try:
        traducciones = {
            "parking": "Plaza de aparcamiento",
            "elevator": "Ascensor",
            "furnished": "Amueblado",
            "washing_machine": "Lavadora",
            "fridge": "Frigorífico",
            "bathrooms": "Baños",
            "floor": "Planta",
            "rooms": "Habitaciones",
            "surface": "Superficie",
            "balcony": "Balcón",
            "air_conditioning": "Aire acondicionado",
            "air_conditioner": "Aire acondicionado",
            "heating": "Calefacción",
            "wardrobes": "Armarios empotrados",
            "garden": "Jardín privado",
            "pool": "Piscina",
            "terrace": "Terraza",
            "storage_room": "Trastero",
            "community_zone": "Zona comunitaria",
            "kitchen_office": "Cocina Office",
            "patio": "Patio",
            "suite_bathroom": "Suite con baño",
            "appliances": "Electrodomésticos",
            "oven": "Horno",
            "microwave": "Microondas",
            "tv": "TV",
            "armored_door": "Puerta blindada",
            "community_pool": "Piscina comunitaria",
            "laundry": "Lavadero",
            "pets_allowed": "Mascotas Permitidas",
            "community_expenses_included": "Gastos de comunidad incluidos",
            "household_appliances": "Electrodomésticos",
            "yard": "Patio",
            "private_garden": "Jardín Privado",
            "swimming_pool": "Piscina"
        }

        def obtener_caracteristica(key, default=None):
            return next((f['value'] for f in data.get("features", []) if f['key'] == key), default)

        # Extraer características traducidas
        caracteristicas = [
            f"{traducciones.get(f['key'], f['key'].replace('_', ' ').capitalize())}"
            for f in data.get("features", [])
            if f['value'] is not None and f['key'] not in [
                'floor', 
                'surface', 
                'elevator', 
                'furnished',
                'rooms',
                'wardrobes',
                'bathrooms',
                'conservationStatus',
                'antiquity',
                'orientation'
                ]
        ] 
        caracteristicas_str = json.dumps(
            caracteristicas, ensure_ascii=False).replace('"', "'")
        tipo_inmueble = obtener_tipo_inmueble(data.get("buildingType"), data.get("buildingSubtype"))
        calle = data.get('location', '') or ''
        precio = int(data.get("rawPrice", 0) or 0)
        superficie = obtener_caracteristica("surface")
        precio_metro = precio / superficie if precio and superficie else None
        return {
            "id_fotocasa": data.get("id"),
            "tipo": tipo_inmueble,
            "tipo_transaccion": "Alquiler" if data.get("transactionTypeId") == 3 else "Venta",
            "titulo": f"{tipo_inmueble} en {calle}",
            "calle": calle,
            "barrio": data["address"].get("neighborhood") or '',
            "zona": data["address"].get("district") or '',
            "ciudad": data["address"].get("city") or '',
            "localizacion": ", ".join(filter(None, [
                data["address"].get("neighborhood"),
                data["address"].get("district"),
                data["address"].get("city"),
                data["address"].get("county"),
                data["address"].get("regionLevel1")
            ])),
            "precio": precio,
            "precio_metro": precio_metro,
            "caracteristicas": caracteristicas_str,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fuente": "fotocasa",
            "disponibilidad": "disponible",
            "superficie": superficie,
            "habitaciones": obtener_caracteristica("rooms"),
            "banos": obtener_caracteristica("bathrooms"),
            "estado": obtener_estado(obtener_caracteristica('conservationStatus')),
            "orientacion": obtener_orientacion(obtener_caracteristica('orientation')),
            "construccion": obtener_antiguedad(obtener_caracteristica('antiquity')),
            "amueblado": "Amueblado" if obtener_caracteristica("furnished") else None,
            "tipo_contacto": obtener_tipo_contacto(data.get("clientTypeId")),
            "nombre_contacto": data.get("clientAlias", 'No indicado') or 'No indicado',
            "telefono_contacto": data.get("phone", "0") or 0,
            "enlace": f"https://www.fotocasa.es{data.get('detail', {}).get('es-ES', '')}"
        }
    except Exception as e:
        print(f"Error extrayendo datos del inmueble: {e}")
        return None

# ==========================
# 🔹 SCRAPING Y EXTRACCIÓN DE DATOS
# ==========================

def obtener_inmuebles(base_url, num_paginas=2):
    session = requests.Session()
    session.headers.update(headers)
    inmuebles = []
    for page in range(1, num_paginas + 1):
        try:
            print(f"Procesando página {page}...")
            response = session.get(f"{base_url}l/{page}?sortType=publicationDate")
            response.raise_for_status()
            json_data = re.search(r'window\.__INITIAL_PROPS__ = JSON\.parse\("((?:[^"\\]|\\.)*)"\);', response.text)
            if json_data:
                json_data = json.loads(json_data.group(1).encode('utf-8').decode('unicode_escape'))
                for inmueble in json_data.get('initialSearch', {}).get('result', {}).get('realEstates', []):
                    info = extract_property_info(inmueble)
                    if info:
                        inmuebles.append(info)
            time.sleep(random.uniform(5, 10))
        except Exception as e:
            print(f"Error en página {page}: {e}")
            break

    return inmuebles

def inmueble_existe(id_fotocasa):
    """
    Verifica si un inmueble con un ID de Fotocasa ya existe en la base de datos a través de la API.

    Args:
        id_fotocasa (int): ID de Fotocasa del inmueble a verificar.

    Returns:
        bool: True si el inmueble existe, False en caso contrario.
    """
    try:
        # Construir la URL para consultar por ID Fotocasa
        url = f"{api_base_url}/inmuebles?id_fotocasa={id_fotocasa}"
        # Realizar la solicitud GET con autenticación
        response = requests.get(url, auth=auth_credentials)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()
            # Verificar si la API responde con "success" y contiene datos
            if data.get("status") == "success" and data.get("data"):
                return True  # El inmueble existe
            else:
                print(f"⚠️ Inmueble {id_fotocasa} no encontrado en la BD.")
                return False
        else:
            # Manejar otros códigos de estado HTTP
            print(f"⚠️ Error en la API: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        # Manejar errores de conexión o solicitud
        print(f"🚨 Error al conectar con la API: {e}")
        return False
    
def verificar_insertar_contacto(nombre, telefono, tipo_contacto):
    """
    Verifica si un contacto existe en la base de datos a través de la API. Si no existe, lo crea.
    Si el número de teléfono es 0 o -1, se crea siempre un contacto nuevo.
    
    Args:
        nombre (str): Nombre del contacto.
        telefono (str): Teléfono del contacto.
        tipo_contacto (str): Tipo del contacto.

    Returns:
        int: ID del contacto existente o recién creado, o None en caso de error.
    """
    try:
        # Si el teléfono es 0 o -1, crear siempre un contacto nuevo, ya que no
        # sabemos por el teléfono si ya lo tenemos (Dos Antonios, pero sin teléfono)
        if telefono in ['0', '-1']:
            create_url = f"{api_base_url}/contactos"
            payload = {
                "nombre": nombre,
                "telefono": telefono,
                "tipo_contacto": tipo_contacto
            }
            post_response = requests.post(create_url, auth=auth_credentials, json=payload)

            if post_response.status_code in [200, 201]:
                created_data = post_response.json()
                if created_data.get("status") == "success" and created_data.get("data"):
                    return created_data["data"]["id"]  # Devuelve el ID del contacto recién creado
                else:
                    print(f"Error al procesar la creación: {created_data.get('message', 'Mensaje no disponible')}")
                    return None
            else:
                print(f"Error al crear el contacto: {post_response.status_code} - {post_response.text}")
                return None

        # Construir la URL para buscar contactos por nombre y teléfono
        url = f"{api_base_url}/contactos"
        params = {"nombre": nombre, "telefono": telefono}

        # Realizar la solicitud GET para buscar el contacto
        response = requests.get(url, auth=auth_credentials, params=params)

        # Manejo de la respuesta GET
        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "success":
                if data.get("data"):  # Si 'data' no está vacío, el contacto existe
                    return data["data"][0]["id_contacto"]  # Devuelve el ID del primer contacto encontrado
                else:
                    # Si el 'data' está vacío, proceder a crear el contacto
                    print("No se encontró ningún contacto con los filtros dados. Procediendo a crear el contacto.")
            else:
                print(f"Error en la búsqueda: {data.get('message', 'Mensaje no disponible')}")
                return None
        elif response.status_code == 404:
            # Si el código es 404, el contacto no existe, proceder a crearlo
            print("El contacto no existe. Procediendo a crear el contacto.")
        else:
            # Manejar códigos de estado inesperados
            print(f"Error inesperado al buscar el contacto: {response.status_code} - {response.text}")
            return None

        # Si llegamos aquí, significa que el contacto no existe. Procedemos a crearlo.
        create_url = f"{api_base_url}/contactos"
        payload = {
            "nombre": nombre,
            "telefono": telefono,
            "tipo_contacto": tipo_contacto
        }

        # Realizar la solicitud POST para crear el contacto
        post_response = requests.post(create_url, auth=auth_credentials, json=payload)

        if post_response.status_code in [200, 201]:
            created_data = post_response.json()
            if created_data.get("status") == "success" and created_data.get("data"):
                return created_data["data"]["id"]  # Devuelve el ID del contacto recién creado
            else:
                print(f"Error al procesar la creación: {created_data.get('message', 'Mensaje no disponible')}")
                return None
        else:
            print(f"Error al crear el contacto: {post_response.status_code} - {post_response.text}")
            return None

    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def insertar_inmueble(data):
    """
    Inserta un inmueble en la base de datos a través de la API.
    Args:
        data (dict): Diccionario con los datos del inmueble.
    Returns:
        int: ID del inmueble recién creado, o None en caso de error.
    """
    # Filtrar solo los campos especificados
    allowed_keys = [
        "id_fotocasa", "id_contacto", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion", "precio",
        "precio_metro", "superficie", "habitaciones", "banos", "armarios", "trastero", "orientacion", "amueblado",
        "calefaccion", "planta", "ascensor", "construccion", "movilidad_reducida", "exterior_interior", "fecha",
        "estado", "caracteristicas", "fuente", "disponibilidad", "tipo_transaccion", "enlace"
    ]
    filtered_data = {key: value for key, value in data.items() if key in allowed_keys}
    try:
        # Construir la URL para insertar un inmueble
        url = f"{api_base_url}/inmuebles"
        # Realizar la solicitud POST con los datos del inmueble
        response = requests.post(url, auth=auth_credentials, json=filtered_data)
        # Verificar si la inserción fue exitosa
        if response.status_code in [200, 201]:
            created_data = response.json()
            if created_data.get("status") == "success":
                # Obtener el ID del inmueble creado desde 'data'
                inmueble_id = created_data.get("data", {}).get("id")
                if inmueble_id:
                    print(f"ID {inmueble_id} guardado en la base de datos.")
                    return inmueble_id  # Devuelve el ID del inmueble recién creado
                else:
                    print("No se pudo obtener el ID del inmueble creado.")
                    return None
            else:
                print(f"Error en la respuesta: {created_data.get('message', 'Mensaje no disponible')}")
                return None
        else:
            print(f"Error al insertar el inmueble: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None

def procesar_inmuebles(base_url, max_repetidos=5, num_paginas=10):
    """
    Procesa los inmuebles desde Fotocasa y los inserta en la base de datos.
    Detiene el proceso si se encuentran demasiados repetidos seguidos.

    Args:
        base_url (str): URL base de Fotocasa.
        max_repetidos (int): Número máximo de inmuebles consecutivos repetidos antes de detener el proceso.
        num_paginas (int): Número máximo de páginas a procesar.
    """
    session = requests.Session()
    session.headers.update(headers)
    repetidos_consecutivos = 0  # Contador de repetidos seguidos
    inmuebles_insertados = 0  # Contador de inmuebles insertados correctamente

    for page in range(1, num_paginas + 1):
        try:
            print(f"Procesando página {page}...")
            response = session.get(f"{base_url}l/{page}?sortType=publicationDate")
            
            if response.status_code in [403, 429]:
                print(f"⚠️ Acceso bloqueado ({response.status_code}). Deteniendo scraping.")
                break

            response.raise_for_status()  # Lanza error si la request falla

            # Extraer JSON de la página
            json_data = re.search(r'window\.__INITIAL_PROPS__ = JSON\.parse\("((?:[^"\\]|\\.)*)"\);', response.text)
            if json_data:
                json_data = json.loads(json_data.group(1).encode('utf-8').decode('unicode_escape'))
                inmuebles = json_data.get('initialSearch', {}).get('result', {}).get('realEstates', [])

                for inmueble_data in inmuebles:
                    id_fotocasa = inmueble_data.get("id")
                    # 🔍 **Verificar si ya existe en la base de datos**
                    if inmueble_existe(id_fotocasa):
                        repetidos_consecutivos += 1
                        print(f"🔁 Inmueble {id_fotocasa} ya en la BD. Contador: {repetidos_consecutivos}")
                        if repetidos_consecutivos >= max_repetidos:
                            print("🚨 Máximo de repetidos alcanzado. Deteniendo scraping.")
                            return
                        continue  # Salta al siguiente inmueble
                    else:
                        repetidos_consecutivos = 0  # Reiniciar contador si encontramos un nuevo inmueble
                    # Extraer y limpiar datos del inmueble
                    inmueble_info = extract_property_info(inmueble_data)
                    if inmueble_info:
                        # 🏡 **Gestión del contacto**
                        id_contacto = verificar_insertar_contacto(
                            inmueble_info.get("nombre_contacto"),
                            str(inmueble_info.get("telefono_contacto")),
                            str(inmueble_info.get("tipo_contacto"))
                        )
                        if id_contacto:
                            inmueble_info['id_contacto'] = id_contacto
                            insertar_inmueble(inmueble_info)
                        # **Insertar el inmueble en la BD**
                        inmuebles_insertados += 1
                        print(f"✅ Inmueble {id_fotocasa} insertado correctamente.")
            # Espera aleatoria para evitar bloqueos
            time.sleep(random.uniform(5, 10))
        except requests.RequestException as e:
            print(f"⚠️ Error en página {page}: {e}")
            break  # Detener el scraping si hay errores de red graves
    print(f"🎯 Proceso completado. {inmuebles_insertados} inmuebles insertados en la base de datos.")

procesar_inmuebles('https://www.fotocasa.es/es/alquiler/viviendas/murcia-provincia/todas-las-zonas/', 5, 1)