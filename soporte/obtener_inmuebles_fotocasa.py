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
    "cookie": 're_uuid=791c856a-2457-4551-8d39-606937e2c694; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; AMCV_05FF6243578784B37F000101%40AdobeOrg=-408604571%7CMCIDTS%7C20123%7CMCMID%7C25593178828150148180448288782706562384%7CMCAAMLH-1739170630%7C6%7CMCAAMB-1739170630%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1738573030s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.6.0; ab.storage.deviceId.c9f9127d-989c-45fe-96f2-f36434db5025=g%3A7ba0421c-7e51-8f3b-d5a5-c7a0bf8dee28%7Ce%3Aundefined%7Cc%3A1738565830821%7Cl%3A1738565830821; ajs_anonymous_id=9d99d39d-0172-42dd-b44a-849a102eaf55; _fbp=fb.1.1738565831107.351341613635226331; didomi_token=eyJ1c2VyX2lkIjoiMTk0Y2E5OTQtNjMyZC02YzI0LTllYmUtYThmYzhkZWNiYmM4IiwiY3JlYXRlZCI6IjIwMjUtMDItMDNUMDY6NTc6MTAuMTk0WiIsInVwZGF0ZWQiOiIyMDI1LTAyLTAzVDA2OjU3OjQwLjMxM1oiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmFkZXZpbnRhLW1vdG9yLW1vdG9yIiwiYzptZXRhcGxhdGYtTlJlVnBtTFEiLCJjOmNyaXRlby1QNDhlR1QydyIsImM6Z29vZ2xlaXJlLWZmS2FQYVJEIl19LCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiLCJnZW9sb2NhdGlvbl9kYXRhIiwidHJhbnNmZXItdG8tbW90b3IiLCJ1c29kZWxvcy1RcExwTThqVyJdfSwidmVuZG9yc19saSI6eyJlbmFibGVkIjpbImdvb2dsZSJdfSwidmVyc2lvbiI6Mn0=; euconsent-v2=CQMQEYAQMQEYAAHABBENBaFsAP_gAEPgAAiQKxtX_G__bWlr8X73aftkeY1P99h77sQxBhbJE-4FzLvW_JwXx2E5NA36tqIKmRIAu3TBIQNlHJDURVCgaogVrSDMaEyUoTNKJ6BkiFMRI2dYCFxvm4tjeQCY5vr991dx2B-t7dr83dzyy4hHn3a5_2S0WJCdA5-tDfv9bROb-9IOd_x8v4v4_F7pE2_eT1l_tWvp7D9-cts_9XW99_fbff9Pn_-uB_-_X_vf_H37gq-ASYaFRAGWBISEGgYQQIAVBWEBFAgCAABIGiAgBMGBTsDABdYSIAQAoABggBAACDIAEAAAEACEQAQAFAgAAgECgADAAgGAgAIGAAEAFgIBAACA6BimBBAIFgAkZkVCmBCEAkEBLZUIJAECCuEIRZ4BEAiJgoAAAAACkAAQFgsDiSQEqEggC4gmgAAIAEAggAKEEnJgACAM2WoPBk2jK0wDB8wSIaYBkARBGQkGgAAA.f_wACHwAAAAA; _gcl_au=1.1.492521579.1738565860; borosTcf=eyJwb2xpY3lWZXJzaW9uIjoyLCJjbXBWZXJzaW9uIjoxLCJwdXJwb3NlIjp7ImNvbnNlbnRzIjp7IjEiOnRydWUsIjIiOnRydWUsIjMiOnRydWUsIjQiOnRydWUsIjUiOnRydWUsIjYiOnRydWUsIjciOnRydWUsIjgiOnRydWUsIjkiOnRydWUsIjEwIjp0cnVlfX0sInNwZWNpYWxGZWF0dXJlcyI6eyIxIjp0cnVlfX0=; segment_ga=GA1.1.1847561627.1738565861; kanirante-adv-aauid=3490fc9d-0a43-4267-a836-64dfdce1d7f9; adit-xandr-id=1541226591830102077; __gads=ID=17b4ca82ddae3ac3:T=1738565860:RT=1738565860:S=ALNI_Maaft8eUvUZRwjlh8hblCyaBF-raA; __gpi=UID=00000fdd489f6fef:T=1738565860:RT=1738565860:S=ALNI_MYwZSHIigfusDRpLXNjIBLlNdzqjQ; __eoi=ID=a40450b77b3e9372:T=1738565860:RT=1738565860:S=AA-AfjYyg3NGH1m9SEiSSP8BT_U0; sui_1pc=1738565861026517C985136EC60A1D7CED0026D579E9B1A25A59EC4D; _lr_retry_request=true; _lr_env_src_ats=false; _csrf=jtfj9vTn9AQM/4/nTdwWHYSQydQwpT1PVz1X5+KKZEjitKFDyHS6z9a4SLedVJDF3x71CJ0qycQJPw79s97cvLeR81WitLZ+TbJz+qaD7bg=; __gsas=ID=de0f99ca5daa3534:T=1738565867:RT=1738565867:S=ALNI_MbnVvvvK18OsJQ72K8-OUIzb5s9tQ; reese84=3:JmkfKPgMwieXiMAiLRNHFg==:7Xh6wkzWMP23bM/BtSHEXguCmNhPld5Z96D8VDlrixmtIAI/qxDuEh7LUrv9NRTs26FQ1akzXhkg0bz/fyl0+tmdhHVG7sLM6ezphbzUC4dg5cgGnqsU4Kyqqm/J3Qlpu8OnUcT59DhYdWnfivByo/Zclqf4D6vSLwBqFaGbIiLh5JWveO6m/FIaeEUFfs52cbnysiMNKhRGt0jrA1HtY38noMCU5HJjMRQBYmfCjk53s55Z7FCufriR4g59+aa/ATRXzGVqeZ7L35/y4SzmB9bVVCEpA0GHSvIbRDTSeJTgsyYrsf6QpbvXCyVLCh3vT9mcTrElb9KeJ3lCImkVDHoWTMFFeiozhDcytOc48Ie3iz4SK8eUN9zCUvuSauPf1f3+q4YCyPG7KygtV03dsv9j+F9XRdQp7/21AYuO6JhVowkueih060gzaBhwghHSh9lY55y9gCDUAOcWoWXypt2QivA1sIn30ldcHk9wVb0=:yklnwVQ4p/7Ru66hhEHFwNRy6TWpqV6sC7yaBwGXxyY=; _lr_sampling_rate=100; segment_ga_MH0GDRSFGC=GS1.1.1738565860.1.1.1738565879.41.0.0; _hjSessionUser_89611=eyJpZCI6ImI5MmMyYzZlLTM1ZjItNWMzYS1iM2RiLTdhOGQ4NjZiMTgyMSIsImNyZWF0ZWQiOjE3Mzg1NjU4ODE1MjEsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_89611=eyJpZCI6IjQ5MTU2ZGM0LTA2NmYtNGEyZC05ODU2LWFlZGY1NWUzNGM3NiIsImMiOjE3Mzg1NjU4ODE1MjIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; ab.storage.sessionId.c9f9127d-989c-45fe-96f2-f36434db5025=g%3A4d461fec-70ff-d960-ed99-cda0983d6a0a%7Ce%3A1738567681740%7Cc%3A1738565830816%7Cl%3A1738565881740; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22kzTateZNYwMPncSKRxs9%22%2C%22expiryDate%22%3A%222026-02-03T06%3A58%3A01.980Z%22%7D; cto_bundle=2Kbh619nZWVvSEpXa3RuWTFNNER6Mkc3OFk0NG1FMFRVOGZSWFU5SnVaaUV5R1FwRVFZUjRGRzRuY1FGTTdJeEJEYzN3Nk43eDVqZTRDYVJSTGZQaGNRVCUyQjFBZndqJTJCQ0ElMkJFaExtVjlHU3ZYTWdrdnd2NFBsRnE4WW53b1ZXNm9TSnN4Uw; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-02-03T06%3A58%3A03.447Z%22%7D'.encode('utf-8'),
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
        1: "Casi Nuevo",
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

procesar_inmuebles('https://www.fotocasa.es/es/alquiler/viviendas/murcia-provincia/todas-las-zonas/', 5, 5)