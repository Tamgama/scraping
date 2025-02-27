import requests
import time
import random
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Verifica si un inmueble existe en la base de datos a través de la API.
def inmueble_existe(id_inmueble):
    """
    Verifica si un inmueble existe en la base de datos a través de la API.
    Args:
        id_inmueble (int): ID del inmueble a verificar.

    Returns:
        bool: True si el inmueble existe, False en caso contrario.
    """
    try:
        # Construir la URL para consultar el inmueble por ID
        url = f"{api_base_url}/inmuebles?id_idealista={id_inmueble}"
        # Realizar la solicitud GET con autenticación
        response = requests.get(url, auth=auth_credentials)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Analizar el contenido de la respuesta
            data = response.json()
            
            # Verificar el campo 'status' en la respuesta
            if data.get("status") == "success":
                # Si hay datos en 'data', el inmueble existe
                return bool(data.get("data"))
            else:
                # Si el status no es 'success', asumir que no existe
                print(f"Error en la respuesta: {data.get('message', 'Mensaje no disponible')}")
                return False
        else:
            # Manejar otros códigos de estado HTTP
            print(f"Error inesperado: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        # Manejar errores de conexión
        print(f"Error al conectar con la API: {e}")
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
        "id_idealista", "id_contacto", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion", "provincia", "precio",
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

# Configuración de directorios y archivos
base_dir = os.path.dirname(os.path.abspath(__file__))

# Variable global para la URL base de la API
api_base_url = "http://euspay.com/api/v1/euspay.php"
auth_credentials = ("promurcia", "Pr0Murc14")  # Sustituye por tu usuario y contraseña

# Leer cookie desde un archivo JSON
with open(os.path.join(base_dir, 'cookie.json'), 'r') as cookie_file:
    config = json.load(cookie_file)
    cookie = config['cookie']
cookie = cookie.encode('utf-8')

# Configuración de headers y sesión de requests
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": cookie,
    "Referer": "https://www.idealista.com/alquiler-viviendas/almeria-provincia/",
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
}
session = requests.Session()
session.headers.update(headers)

# Clasificación de elementos de ubicación
ciudades_almeria = {
    "Abla": "Abla",
    "Abrucena": "Abrucena",
    "Adra": "Adra",
    "Albánchez": "Albánchez",
    "Alboloduy": "Alboloduy",
    "Albox": "Albox",
    "Alcolea": "Alcolea",
    "Alcóntar": "Alcóntar",
    "Alcudia de Monteagud": "Alcudia de Monteagud",
    "Alhabia": "Alhabia",
    "Alhama de Almería": "Alhama de Almería",
    "Alicún": "Alicún",
    "Almería": "Almería",
    "Almócita": "Almócita",
    "Alsodux": "Alsodux",
    "Antas": "Antas",
    "Arboleas": "Arboleas",
    "Armuña de Almanzora": "Armuña de Almanzora",
    "Bacares": "Bacares",
    "Balanegra": "Balanegra",
    "Bayárcal": "Bayárcal",
    "Bayarque": "Bayarque",
    "Bédar": "Bédar",
    "Beires": "Beires",
    "Benahadux": "Benahadux",
    "Benitagla": "Benitagla",
    "Benizalón": "Benizalón",
    "Bentarique": "Bentarique",
    "Berja": "Berja",
    "Canjáyar": "Canjáyar",
    "Cantoria": "Cantoria",
    "Carboneras": "Carboneras",
    "Castro de Filabres": "Castro de Filabres",
    "Chercos": "Chercos",
    "Chirivel": "Chirivel",
    "Cóbdar": "Cóbdar",
    "Cuevas del Almanzora": "Cuevas del Almanzora",
    "Dalías": "Dalías",
    "El Ejido": "El Ejido",
    "Enix": "Enix",
    "Felix": "Felix",
    "Fines": "Fines",
    "Fiñana": "Fiñana",
    "Fondón": "Fondón",
    "Gádor": "Gádor",
    "Los Gallardos": "Los Gallardos",
    "Garrucha": "Garrucha",
    "Gérgal": "Gérgal",
    "Huécija": "Huécija",
    "Huércal de Almería": "Huércal de Almería",
    "Huércal-Overa": "Huércal-Overa",
    "Íllar": "Íllar",
    "Instinción": "Instinción",
    "Laroya": "Laroya",
    "Laujar de Andarax": "Laujar de Andarax",
    "Líjar": "Líjar",
    "Lubrín": "Lubrín",
    "Lucainena de las Torres": "Lucainena de las Torres",
    "Lúcar": "Lúcar",
    "Macael": "Macael",
    "María": "María",
    "Mojácar": "Mojácar",
    "La Mojonera": "La Mojonera",
    "Nacimiento": "Nacimiento",
    "Níjar": "Níjar",
    "Ohanes": "Ohanes",
    "Olula de Castro": "Olula de Castro",
    "Olula del Río": "Olula del Río",
    "Oria": "Oria",
    "Padules": "Padules",
    "Partaloa": "Partaloa",
    "Paterna del Río": "Paterna del Río",
    "Pechina": "Pechina",
    "Pulpí": "Pulpí",
    "Purchena": "Purchena",
    "Rágol": "Rágol",
    "Rioja": "Rioja",
    "Roquetas de Mar": "Roquetas de Mar",
    "Santa Cruz de Marchena": "Santa Cruz de Marchena",
    "Santa Fe de Mondújar": "Santa Fe de Mondújar",
    "Senés": "Senés",
    "Serón": "Serón",
    "Sierro": "Sierro",
    "Somontín": "Somontín",
    "Sorbas": "Sorbas",
    "Suflí": "Suflí",
    "Tabernas": "Tabernas",
    "Taberno": "Taberno",
    "Tahal": "Tahal",
    "Terque": "Terque",
    "Tíjola": "Tíjola",
    "Las Tres Villas": "Las Tres Villas",
    "Turre": "Turre",
    "Turrillas": "Turrillas",
    "Uleila del Campo": "Uleila del Campo",
    "Urrácal": "Urrácal",
    "Velefique": "Velefique",
    "Vélez-Blanco": "Vélez-Blanco",
    "Vélez-Rubio": "Vélez-Rubio",
    "Vera": "Vera",
    "Viator": "Viator",
    "Vícar": "Vícar",
    "Zurgena": "Zurgena"
}

# Expresiones regulares para clasificación de ubicaciones
barrio_regex = re.compile(r"^barrio\s+.+", re.IGNORECASE)
distrito_regex = re.compile(r"^distrito\s+.+", re.IGNORECASE)
zonas = ["Los Vélez", "Bajo Almanzora", "Valle de Almanzora", "Filabres", "Campo de Tabernas", "Levante", "Cabo de Gata", "Alpujarras", "Almería", "Poniente"]
direccion_regex = re.compile(
    r"^(Calle|Avda\.?|Avenida|Carril|Plaza|Camino|Carretera|C\.|Paseo|Pza\.?|de|Ronda|Senda|Donantes|Arroyo|Atlántico)\s+.+",
    re.IGNORECASE
)

# Fecha de ejecución
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Número de páginas a recorrer
num_paginas = 40

def clasificar_elementos(lista_elementos):
    clasificacion = {
        "direccion": None,
        "barrio": None,
        "distrito": None,
        "ciudad": None,
        "zona": None,
        "otros": []
    }
    categorias_asignadas = {
        "direccion": False,
        "barrio": False,
        "distrito": False,
        "ciudad": False,
        "zona": False,
    }
    for elemento in lista_elementos:
        elemento_strip = elemento.strip()
        elemento_lower = elemento_strip.lower()
        if not categorias_asignadas["direccion"] and direccion_regex.match(elemento_strip):
            clasificacion["direccion"] = elemento_strip
            categorias_asignadas["direccion"] = True
            continue
        if not categorias_asignadas["barrio"] and barrio_regex.match(elemento_strip):
            clasificacion["barrio"] = elemento_strip
            categorias_asignadas["barrio"] = True
            continue
        if not categorias_asignadas["distrito"] and distrito_regex.match(elemento_strip):
            clasificacion["distrito"] = elemento_strip
            categorias_asignadas["distrito"] = True
        if not categorias_asignadas["ciudad"] and any(ciudad.lower() in elemento_lower for ciudad in ciudades_almeria):
            ciudad_match = next(ciudad for ciudad in ciudades_almeria if ciudad.lower() in elemento_lower)
            clasificacion["ciudad"] = ciudad_match
            categorias_asignadas["ciudad"] = True
            continue
        if not categorias_asignadas["zona"] and any(zona.lower() in elemento_lower for zona in zonas):
            ciudad_match = next(zona for zona in zonas if zona.lower() in elemento_lower)
            clasificacion["zona"] = ciudad_match
            categorias_asignadas["zona"] = True
            break
        clasificacion["otros"].append(elemento_strip)
    return clasificacion

def procesar_inmuebles(base_url, tipo_transaccion, max_repetidos=5):
    """
    Procesa los inmuebles de una URL base según el tipo de transacción.
    Detiene el proceso si se alcanzan un número consecutivo de inmuebles repetidos.

    Args:
        base_url (str): URL base a procesar.
        tipo_transaccion (str): Tipo de transacción ("Alquiler" o "Venta").
        max_repetidos (int): Número máximo de inmuebles consecutivos repetidos antes de detener el proceso.
    """
    repetidos_consecutivos = 0  # Contador de inmuebles repetidos consecutivos

    for i in range(1, num_paginas + 1):
        url = base_url.format(i)
        try:
            r = session.get(url)
            if r.status_code in [403, 429]:
                print(f"Deteniendo proceso debido a un status_code {r.status_code} en la página {url}")
                break
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al intentar acceder a {url}: {e}")
            continue

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            articles = soup.find_all('article')
            for article in articles:
                data_element_id = article.get('data-element-id')
                if not data_element_id:
                    continue
                data_element_id = int(data_element_id)

                # Verificar si el inmueble ya existe
                if inmueble_existe(data_element_id):
                    repetidos_consecutivos += 1
                    print(f"Inmueble {data_element_id} ya existe. Contador de repetidos: {repetidos_consecutivos}")
                    # Detener si se supera el umbral de repetidos consecutivos
                    if repetidos_consecutivos >= max_repetidos:
                        print("Se alcanzó el número máximo de inmuebles repetidos consecutivos. Deteniendo proceso.")
                        return
                    continue  # Saltar al siguiente inmueble
                else:
                    repetidos_consecutivos = 0  # Reiniciar contador de repetidos si se encuentra uno nuevo

                # Procesar y limpiar los datos del inmueble
                time.sleep(random.uniform(1, 3))  # Añadir un retraso

                inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
                try:
                    r = session.get(inmueble_url)
                    if r.status_code in [403, 429]:
                        print(f"Deteniendo proceso debido a un status_code {r.status_code} en la URL del inmueble {inmueble_url}")
                        break
                    r.raise_for_status()
                except requests.RequestException as e:
                    print(f"Error al intentar acceder a {inmueble_url}: {e}")
                    continue

                soup = BeautifulSoup(r.text, 'lxml')
                titulo = soup.find("span", {"class": "main-info__title-main"})
                titulo_text = titulo.get_text(strip=True) if titulo else "N/A"

                price_info = soup.find("span", {"class": "info-data-price"})
                price_text = price_info.get_text(strip=True) if price_info else "N/A"

                meter_container = soup.find("p", {"class": "flex-feature squaredmeterprice"})
                meter = [me.text for me in meter_container.find_all("span")] if meter_container else []
                meter_price = meter[1] if len(meter) > 1 else "N/A"

                reference_container = soup.find("div", {"class": "ad-reference-container"})
                if reference_container:
                    reference = reference_container.find("p", {"class": "txt-ref"})
                    ref_num = reference.get_text(strip=True) if reference else "N/A"
                else:
                    ref_num = "N/A"
                # Extraer última actualización
                actual_container = soup.find("div", {"id" : "stats"})
                actual = actual_container.find("p").get_text(strip=True) if actual_container else "N/A"
                # Extraer anunciante
                anun_container = soup.find("div", {"class": "professional-name"})
                if anun_container:
                    anun = anun_container.find("div", {"class": "name"})
                    anunciante = anun.get_text(strip=True) if anun else "N/A"
                    nombre_anun = anun_container.find("span").get_text(strip=True) if anun else "N/A"
                else:
                    anunciante = "N/A"
                    nombre_anun = "N/A"

                location = soup.find("div", {"id": "headerMap"})
                if location:
                    loc = [lo.text.strip() for lo in location.find_all("li")]
                    direccion_clasificada = clasificar_elementos(loc)
                    street = direccion_clasificada['direccion'] or "N/A"
                    ciudad = direccion_clasificada['ciudad'] or "N/A"
                    barrio = direccion_clasificada['barrio'] or "N/A"
                    zona = direccion_clasificada['zona'] or "N/A"
                    direccion_completa = ', '.join(loc)
                else:
                    street = barrio = zona = "N/A"
                    direccion_completa = "N/A"

                c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})
                basics = [caract.text.strip() for caract in c1.find_all("li")] if c1 else []

                phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"
                telefono = "N/A"
                try:
                    res_phone = session.get(phone_url)
                    res_phone.raise_for_status()
                    telefono_res = res_phone.json()
                    if 'phone1' in telefono_res:
                        if telefono_res['phone1'] and telefono_res['phone1'].get('number'):
                            telefono = telefono_res['phone1']['number']
                        else:
                            telefono = -1
                except requests.RequestException as e:
                    print(f"Error al intentar acceder al teléfono para {data_element_id}: {e}")

                # Limpieza y extracción adicional de datos
                titulo_text = titulo_text.replace('Alquiler de ', '').replace('en venta ', '').strip()
                tipo_inmueble = titulo_text.split(' ')[0]
                street = street.replace('\n', '').strip()
                ciudad = ciudad.replace('\n', '').strip()
                direccion_completa = direccion_completa.replace('\n', '').strip()
                price_text = price_text.replace('\n', '').replace('€/mes', '').replace('€', '').replace('.', '').strip()
                meter_price = meter_price.replace('\n', '').replace('€/m²', '').replace('.', '').strip()
                barrio = barrio.replace('Barrio ', '').strip()

                try:
                    telefono = int(telefono)
                except ValueError:
                    telefono = 0
                try:
                    precio = int(price_text)
                except ValueError:
                    precio = 0
                try:
                    precio_metro = float(meter_price.replace(',', '.'))
                except ValueError:
                    precio_metro = 0.0

                # Inicializar columnas adicionales para características extraídas
                columnas_extra = [
                    'superficie', 'habitaciones', 'banos', 'terraza', 'garaje', 'estado',
                    'armarios', 'trastero', 'orientacion', 'calefaccion', 'planta',
                    'ascensor', 'construccion', 'amueblado', 'movilidad_reducida'
                ]
                extra_data = {col: None for col in columnas_extra}

                # Patrones regex para características
                patterns = {
                    'superficie': re.compile(r'(\d+)\s*m² construidos', re.IGNORECASE),
                    'habitaciones': re.compile(r'(\d+)\s*habitaciones?', re.IGNORECASE),
                    'banos': re.compile(r'(\d+)\s*baños?', re.IGNORECASE),
                    'terraza': re.compile(r'(Terraza|Balcón)', re.IGNORECASE),
                    'garaje': re.compile(r'(Plaza de garaje)', re.IGNORECASE),
                    'estado': re.compile(r'(Segunda mano\b.*buen estado)', re.IGNORECASE),
                    'armarios': re.compile(r'(Armarios empotrados)', re.IGNORECASE),
                    'trastero': re.compile(r'(Trastero)', re.IGNORECASE),
                    'orientacion': re.compile(r'Orientación\s([\w\s]+)', re.IGNORECASE),
                    'calefaccion': re.compile(r'Calefacción (central|individual|No disponible calefaccion)', re.IGNORECASE),
                    'planta': re.compile(r'Planta\s+(\d+)[ªº]?(?:\s+(exterior|interior))?', re.IGNORECASE),
                    'ascensor': re.compile(r'(Con ascensor|Sin ascensor)', re.IGNORECASE),
                    'construccion': re.compile(r'Construido en (\d{4})', re.IGNORECASE),
                    'amueblado': re.compile(r'\b(?!.*\b(no|sin)\b.*)(?=.*\bamueblado\b).*', re.IGNORECASE),
                    'movilidad_reducida': re.compile(r'(Solo acceso exterior adaptado para personas con movilidad reducida)', re.IGNORECASE)
                }

                # Extraer características con regex
                caracteristicas_texto = ', '.join(basics)
                for key, pattern in patterns.items():
                    match = pattern.search(caracteristicas_texto)
                    if match:
                        extra_data[key] = match.group(1) if key != 'terraza' else 'Sí'

                inmueble_data = {
                    "id_inmueble": data_element_id,
                    "id_idealista": data_element_id,
                    "tipo": tipo_inmueble,
                    "tipo_transaccion": tipo_transaccion,
                    "titulo": titulo_text,
                    "calle": street,
                    "barrio": barrio,
                    "zona": zona,
                    "ciudad": ciudad,
                    "localizacion": direccion_completa,
                    "provincia": 'Almería',
                    "precio": precio,
                    "precio_metro": precio_metro,
                    "caracteristicas": str(basics),
                    "referencia": ref_num,
                    "tipo_contacto": anunciante,
                    "nombre": nombre_anun,
                    "telefono": telefono,
                    "enlace": inmueble_url,
                    "fecha": fecha_actual,
                    'fuente': 'idealista',
                    'disponibilidad': 'disponible',
                }
                inmueble_data.update(extra_data)
                contacto = verificar_insertar_contacto(
                    inmueble_data.get("nombre"),
                    str(inmueble_data.get("telefono")),
                    str(inmueble_data.get("tipo_contacto"))
                )
                if contacto:
                    inmueble_data['id_contacto'] = contacto
                    insertar_inmueble(inmueble_data)

                time.sleep(random.uniform(1, 3))

# Procesar inmuebles en alquiler
procesar_inmuebles(
    base_url="https://www.idealista.com/alquiler-viviendas/almeria-provincia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc",
    tipo_transaccion="Alquiler",
    max_repetidos=5,
)

# Procesar inmuebles en venta
procesar_inmuebles(
    base_url="https://www.idealista.com/venta-viviendas/almeria-provincia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc",
    tipo_transaccion="Venta",
    max_repetidos=5,
)

# Procesar inmuebles en venta
procesar_inmuebles(
    base_url="https://www.idealista.com/alquiler-habitacion/almeria-provincia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc",
    tipo_transaccion="Habitación",
    max_repetidos=5,
)
