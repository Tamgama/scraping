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
    try:
        # Construir la URL para consultar el inmueble por ID
        url = f"{api_base_url}/inmuebles/{id_inmueble}"
        # Realizar la solicitud GET con autenticación
        response = requests.get(url, auth=auth_credentials)
        # Verificar si la respuesta es 200
        if response.status_code == 200:
            # Analizar el contenido de la respuesta
            data = response.json()
            if "error" in data:
                # print(f"Error en la respuesta: {data['error']}")
                return False
            else:
                return True
        # Si la respuesta es 404, el inmueble no existe
        elif response.status_code == 404:
            return False
        # Manejar otros posibles códigos de error
        else:
            print(f"Error inesperado: {response.status_code} - {response.text}")
            return False
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return False
    
def verificar_insertar_contacto(nombre, telefono, tipo_contacto):
    try:
        # Construir la URL para buscar contactos por nombre y teléfono
        url = f"{api_base_url}/contactos"
        # Realizar la solicitud GET con filtros (nombre y teléfono)
        params = {"nombre": nombre, "telefono": telefono}
        response = requests.get(url, auth=auth_credentials, params=params)
        # Verificar si el contacto existe
        if response.status_code == 200:
            data = response.json()
            if data:  # Si la API devuelve datos, el contacto existe
                return data[0]['id_contacto']  # Devuelve el primer contacto encontrado
        # Si el contacto no existe, realizar un POST para crearlo
        if response.status_code == 404 or not data:
            # URL para insertar el contacto
            url = f"{api_base_url}/contactos"
            payload = {
                "nombre": nombre,
                "telefono": telefono,
                "tipo_contacto": tipo_contacto
            }
            post_response = requests.post(url, auth=auth_credentials, json=payload)
            
            if post_response.status_code == 201:
                created_data = post_response.json()
                return created_data['id']  # Devuelve el ID del contacto recién creado
            else:
                print(f"Error al crear el contacto: {post_response.status_code} - {post_response.text}")
                return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
    
def insertar_inmueble(data):
    # Filtrar solo los campos especificados
    allowed_keys = [
        "id_inmueble", "id_contacto", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion", "precio",
        "precio_metro", "superficie", "habitaciones", "banos", "armarios", "trastero", "orientacion", "amueblado",
        "calefaccion", "planta", "ascensor", "construccion", "movilidad_reducida", "exterior_interior", "fecha",
        "estado", "caracteristicas", "fuente", "disponibilidad", "tipo_transaccion"
    ]
    filtered_data = {key: value for key, value in data.items() if key in allowed_keys}
    try:
        # Construir la URL para insertar un inmueble
        url = f"{api_base_url}/inmuebles"
        # Realizar la solicitud POST con los datos del inmueble
        response = requests.post(url, auth=auth_credentials, json=filtered_data)   
        # Verificar si la inserción fue exitosa
        if response.status_code == 201:
            created_data = response.json()
            print(f"ID {created_data['id']} guardado en la base de datos.")
            return created_data['id']  # Devuelve el ID del inmueble recién creado
        else:
            print(f"Error al insertar el inmueble: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return None
    
# FUnción para poder ver que hemos cargado de momento en la base de datos:
# Función para imprimir el contenido de una tabla en la base de datos
def imprimir_tabla(nombre_tabla):
    try:
        # Construir la URL para consultar la tabla
        url = f"{api_base_url}/{nombre_tabla}"
        # Realizar la solicitud GET
        response = requests.get(url, auth=auth_credentials)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            rows = response.json()  # Convertir la respuesta JSON a un objeto Python
            if not rows:
                print(f"La tabla '{nombre_tabla}' está vacía.")
                return
            for fila in rows:
                print(fila)
        else:
            print(f"Error al consultar la tabla '{nombre_tabla}': {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")


# Configuración de directorios y archivos
base_dir = os.path.dirname(os.path.abspath(__file__))

# Variable global para la URL base de la API
api_base_url = "http://euspay.com/api/v1/euspay.php"
auth_credentials = ("promurcia", "Pr0Murc14")  # Sustituye por tu usuario y contraseña

# Definiciones para la clasificación de ubicaciones y patrones regex
ciudades_murcia = {
    "Abanilla": "Abanilla",
    "Abarán": "Abarán",
    "Águilas": "Águilas",
    "Albudeite": "Albudeite",
    "Alcantarilla": "Alcantarilla",
    "Los Alcázares": "Los Alcázares",
    "Aledo": "Aledo",
    "Alguazas": "Alguazas",
    "Alhama de Murcia": "Alhama de Murcia",
    "Archena": "Archena",
    "Beniel": "Beniel",
    "Blanca": "Blanca",
    "Bullas": "Bullas",
    "Calasparra": "Calasparra",
    "Campos del Río": "Campos del Río",
    "Caravaca de la Cruz": "Caravaca de la Cruz",
    "Cartagena": "Cartagena",
    "Cehegín": "Cehegín",
    "Ceutí": "Ceutí",
    "Cieza": "Cieza",
    "Fortuna": "Fortuna",
    "Fuente Álamo de Murcia": "Fuente Álamo de Murcia",
    "Jumilla": "Jumilla",
    "Librilla": "Librilla",
    "Lorca": "Lorca",
    "Lorquí": "Lorquí",
    "Mazarrón": "Mazarrón",
    "Molina de Segura": "Molina de Segura",
    "Moratalla": "Moratalla",
    "Mula": "Mula",
    "Murcia": "Murcia",
    "Ojós": "Ojós",
    "Pliego": "Pliego",
    "Puerto Lumbreras": "Puerto Lumbreras",
    "Ricote": "Ricote",
    "San Javier": "San Javier",
    "San Pedro del Pinatar": "San Pedro del Pinatar",
    "Santomera": "Santomera",
    "Torre-Pacheco": "Torre-Pacheco",
    "Totana": "Totana",
    "Ulea": "Ulea",
    "La Unión": "La Unión",
    "Villanueva del Río Segura": "Villanueva del Río Segura",
    "Yecla": "Yecla",
    "Sucina": "Sucina"
}

barrio_regex = re.compile(r"^barrio\s+.+", re.IGNORECASE)
distrito_regex = re.compile(r"^distrito\s+.+", re.IGNORECASE)
direcciones_cardinales = ["norte", "sur", "este", "oeste", "centro"]
direccion_regex = re.compile(
    r"^(Calle|Avda\.?|Avenida|Carril|Plaza|Camino|Carretera|C\.|Paseo|Pza\.?|de|Ronda|Senda|Donantes|Arroyo|Atlántico)\s+.+",
    re.IGNORECASE
)

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
    "Referer": "https://www.idealista.com/alquiler-viviendas/murcia-murcia/",
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

# URL base y configuración de páginas a recorrer
base_url = "https://www.idealista.com/alquiler-viviendas/murcia-murcia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc"
num_paginas = 40  # Cambia este número según la cantidad de páginas que quieras recorrer

# La fecha de ejecución del script
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Función para clasificar elementos de ubicación
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
        if not categorias_asignadas["ciudad"] and any(ciudad.lower() in elemento_lower for ciudad in ciudades_murcia):
            ciudad_match = next(ciudad for ciudad in ciudades_murcia if ciudad.lower() in elemento_lower)
            clasificacion["ciudad"] = ciudad_match
            categorias_asignadas["ciudad"] = True
            continue
        if not categorias_asignadas["zona"]:
            for dir_cardinal in direcciones_cardinales:
                if dir_cardinal in elemento_lower:
                    clasificacion["zona"] = dir_cardinal.capitalize()
                    categorias_asignadas["zona"] = True
                    break
        clasificacion["otros"].append(elemento_strip)
    return clasificacion

# Bucle principal para recorrer las páginas y extraer datos
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
            # Extraer título
            titulo = soup.find("span", {"class": "main-info__title-main"})
            titulo_text = titulo.get_text(strip=True) if titulo else "N/A"
            # Extraer precio
            price_info = soup.find("span", {"class": "info-data-price"})
            price_text = price_info.get_text(strip=True) if price_info else "N/A"
            # Extraer precio por metro cuadrado
            meter_container = soup.find("p", {"class" :"flex-feature squaredmeterprice"})
            meter = [me.text for me in meter_container.find_all("span")] if meter_container else []
            meter_price = meter[1] if len(meter) > 1 else "N/A"
            # Extraer referencia
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

            # Extraer ubicación
            location = soup.find("div", {"id": "headerMap"})
            if location:
                loc = [lo.text.strip() for lo in location.find_all("li")]
                direccion_clasificada = clasificar_elementos(loc)
                street = direccion_clasificada['direccion'] or "N/A"
                ciudad = direccion_clasificada['ciudad'] or "Murcia"
                barrio = direccion_clasificada['barrio'] or "Murcia"
                zona = direccion_clasificada['zona'] or "N/A"
                direccion_completa = ', '.join(loc)
            else:
                street = barrio = zona = "N/A"
                direccion_completa = "N/A"

            # Extraer detalles de la propiedad
            c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})
            basics = [caract.text.strip() for caract in c1.find_all("li")] if c1 else []
            # Extraer número de teléfono
            phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"
            telefono = "N/A"
            try:
                res_phone = session.get(phone_url)
                res_phone.raise_for_status()
                telefono_res = res_phone.json()
                if 'phone1' in telefono_res and telefono_res['phone1'] and telefono_res['phone1'].get('number'):
                    telefono = telefono_res['phone1']['number']
            except requests.RequestException as e:
                print(f"Error al intentar acceder al teléfono para {data_element_id}: {e}")
            # Limpiar y procesar los datos extraídos
            titulo_text = titulo_text.replace('Alquiler de ', '').strip()
            tipo_inmueble = titulo_text.split(' ')[0]
            street = street.replace('\n', '').strip()
            ciudad = ciudad.replace('\n', '').strip()
            direccion_completa = direccion_completa.replace('\n', '').strip()
            price_text = price_text.replace('\n', '').replace('€/mes', '').replace('.', '').strip()
            meter_price = meter_price.replace('\n', '').replace('€/m²', '').replace('.', '').strip()
            barrio = barrio.replace('Barrio ', '').strip()
            zona = zona.replace('Área de ', '').strip()
            # Convertir teléfono y precios a números si es posible
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
                'superficie', 'superficie_util', 'terraza', 'garaje', 'estado',
                'armarios', 'trastero', 'orientacion', 'calefaccion', 'planta', 'ascensor', 'construccion'
            ]
            extra_data = {col: None for col in columnas_extra}

            # Definir patrones regex para extraer características
            patterns = {
                'superficie': re.compile(r'(\d+)\s*m² construidos', re.IGNORECASE),
                'habitaciones': re.compile(r'(\d+)\s*habitaciones?', re.IGNORECASE),
                'baños': re.compile(r'(\d+)\s*baños?', re.IGNORECASE),
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
            # Función para extraer datos de 'caracteristicas'
            def extract_data(row, patterns):
                data = {col: None for col in patterns.keys()}
                if not row:
                    return data
                for key, pattern in patterns.items():
                    match = pattern.search(row)
                    if match:
                        if key == 'planta':
                            data['planta'] = match.group(1)
                            data['exterior_interior'] = match.group(2)
                        elif key == 'ascensor':
                            data[key] = 'Sí' if 'Con' in match.group(0) else 'No'
                        elif key == 'amueblado':
                            # Detección específica para "amueblado" con exclusión de "no" y "sin"
                            if re.search(r'\b(no|sin)\b', row, re.IGNORECASE):
                                data[key] = 'No amueblado'
                            else:
                                data[key] = 'Amueblado'
                        elif key == 'calefaccion':
                            calef = match.group(1)
                            data[key] = calef if calef != 'No disponible calefaccion' else 'No disponible'
                        elif key == 'orientacion':
                            data[key] = match.group(1)
                        else:
                            data[key] = match.group(1)
                return data

            # Aplicar la función de extracción
            caracteristicas_texto = ', '.join(basics)
            extraidos = extract_data(caracteristicas_texto, patterns)
            # Crear un diccionario con todos los datos limpios del inmueble
            inmueble_data = {
                "id_inmueble": data_element_id,
                "tipo": tipo_inmueble,
                "tipo_transaccion": "Alquiler",
                "titulo": titulo_text,
                "calle": street,
                "barrio": barrio,
                "zona": zona,
                "ciudad": ciudad,
                "localizacion": direccion_completa,
                "precio": precio,
                "precio_metro": precio_metro,
                "caracteristicas": basics,
                "referencia": ref_num,
                "anunciante": anunciante,
                "nombre": nombre_anun,
                "telefono": telefono,
                "url": inmueble_url,
                "fecha": fecha_actual,
                'fuente': 'idealista',
                'disponibilidad': 'disponible',
            }
            # Añadir las características extraídas
            if(inmueble_existe(inmueble_data['id_inmueble'])):
                print('El inmueble ya existe')

            else:
                contacto= verificar_insertar_contacto(
                    inmueble_data['nombre'],
                    str(inmueble_data['telefono']),
                    str(inmueble_data["anunciante"])
                )

            time.sleep(random.uniform(1,3))
            
