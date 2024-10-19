import requests
import time
import random
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
import traceback
from datetime import datetime
import json

# URL base para scraping de inmuebles en Idealista
base_url = "https://www.idealista.com/venta-viviendas/murcia-murcia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc"
csv_file = "../src/ventas-corregido.csv"

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "id_inmueble", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion", 
        "precio", "precio_metro", "caracteristicas", "habitaciones", "m_construidos", "m_utiles",
        "baños", "referencia", "anunciante", "nombre", "ultima_atualizacion", "tlf", "url", "fecha"
    ])

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
    "Sucina": "Sucina"  # Nota: Sucina es una pedanía de Murcia, no un municipio independiente
}


# Patrón regex para identificar barrios y distritos que comienzan por "barrio" o "distrito"
barrio_regex = re.compile(r"^barrio\s+.+", re.IGNORECASE)
distrito_regex = re.compile(r"^distrito\s+.+", re.IGNORECASE)

direcciones_cardinales = ["norte", "sur", "este", "oeste", "centro"]
# Patrón regex para identificar direcciones (simplificado)
direccion_regex = re.compile(
    r"^(Calle|Avda\.?|Avenida|Carril|Plaza|Camino|Carretera|C\.|Paseo|Pza\.?|de|Ronda|Senda|Donantes|Arroyo|Atlantico)\s+.+", 
    re.IGNORECASE
)


# Cargar la cookie desde el archivo JSON
cookie = ""
with open('cookie.json', 'r') as cookie_file:
    config = json.load(cookie_file)
    cookie = config['cookie']

# Cabeceras HTTP para las peticiones normales
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": cookie,
    "Priority": "u=0, i",
    "Referer": "https://www.idealista.com/venta-viviendas/murcia-murcia/",
    "Sec-Ch-Device-Memory": "8",
    "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.119", "Chromium";v="127.0.6533.119"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

# Sesión de requests con headers personalizados
session = requests.Session()
session.headers.update(headers)

# Definir el rango de páginas que quieres recorrer
num_paginas = 159  # Cambia este número según la cantidad de páginas que quieras recorrer

# Función para hacer scraping con múltiples estrategias
def scrape_url(url, use_session=False, is_phone_url=False):
    # Diccionario con las diferentes estrategias de scraping
    scraping_methods = {
        "Normal Requests": {
            "url": url,
            "use_scrapingbee": False,
        },
        "ScrapingBee Básico": {
            "url": f"https://app.scrapingbee.com/api/v1/",
            "use_scrapingbee": True,
            "params": {
                "url": url,
            },
        },
        "ScrapingBee Premium Proxy": {
            "url": f"https://app.scrapingbee.com/api/v1/",
            "use_scrapingbee": True,
            "params": {
                "url": url,
                "premium_proxy": "true"
            },
        },
        "ScrapingBee Stealth Proxy": {
            "url": f"https://app.scrapingbee.com/api/v1/",
            "use_scrapingbee": True,
            "params": {
                "url": url,
                "stealth_proxy": "true"
            },
        }
    }

    api_key = "YC3H4DMMSSCHAOPAA8IJUNWYK1LB6N5P8DK4I7VY1Y3R5OCX36IXA18G90YOBOC757LVHL24VO9SNVIG"

    # Comprobar si estamos intentando la URL del teléfono
    if is_phone_url:
        print(f"Obteniendo datos del teléfono desde {url}")
        
        # Proceso normal (sin ScrapingBee)
        if not use_session:
            try:
                response = session.get(url)
                if response.status_code == 200:
                    return response.json()  # El contenido es directamente JSON
                else:
                    print(f"Error al obtener el teléfono, código de estado: {response.status_code}")
            except Exception as e:
                print(f"Error al procesar la URL de teléfonos {url}: {str(e)}")
            return None

        # Proceso con ScrapingBee (tratamos el contenido como HTML)
        else:
            for method, config in scraping_methods.items():
                if config["use_scrapingbee"]:
                    try:
                        response = requests.get(
                            config["url"],
                            params={**config["params"], "api_key": api_key}
                        )
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            pre_tag = soup.find('pre')
                            if pre_tag:
                                json_data = json.loads(pre_tag.text)
                                return json_data  # Devolver el JSON parseado
                            else:
                                print("No se encontró la etiqueta <pre> en la respuesta.")
                        else:
                            print(f"{method} fallido con código de estado {response.status_code}")
                    except Exception as e:
                        print(f"Error en {method}: {str(e)}")
                        traceback.print_exc()

            return None  # Si todo falla
    else:
        # Recorremos los diferentes métodos de scraping en orden para otras URLs
        for method, config in scraping_methods.items():
            try:
                # Si es una petición normal, usamos la sesión con los headers
                if config["use_scrapingbee"] is False:
                    if use_session:
                        response = session.get(config["url"])  # Usar la sesión para peticiones normales
                    else:
                        response = requests.get(config["url"], headers=headers)  # Usar la sesión por defecto

                # Si el método usa ScrapingBee, añadimos la clave de API y hacemos la petición
                else:
                    response = requests.get(
                        config["url"],
                        params={**config["params"], "api_key": api_key}
                    )

                # Si obtenemos respuesta exitosa
                if response.status_code == 200:
                    return response.content
                else:
                    print(f"{method} fallido con status code {response.status_code}")
            except Exception as e:
                print(f"Error en {method}: {str(e)}")
                traceback.print_exc()

        # Si todos los métodos fallan, retornamos None
        print("Todas las peticiones fallaron")
        return None

# La fecha de ejecución de la script
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Variable para controlar si debemos detener el scraping
detener_scraping = False

# Bucle para recorrer cada página de Idealista
for i in range(1, num_paginas + 1):
    if detener_scraping:
        break  # Detener todo el scraping si alcanzamos 5 IDs consecutivos

    url = base_url.format(i)
    try:
        contenido = scrape_url(url, use_session=True)  # Usar sesión para la petición normal

        if not contenido:
            print(f"No se pudo obtener contenido para la página {i}.")
            continue

        soup = BeautifulSoup(contenido, 'html.parser')
        articles = soup.find_all('article')

        id_consecutivos = 0  # Contador de IDs consecutivos encontrados

        for article in articles:
            if detener_scraping:
                break  # Rompe el bucle de artículos si se ha alcanzado el límite de IDs consecutivos

            data_element_id = article.get('data-element-id')
            if data_element_id:
                data_element_id = int(data_element_id)

                # Comprobar si el ID ya existe
                if data_element_id in df["id_inmueble"].values:
                    id_consecutivos += 1
                    print(f"ID {data_element_id} ya existe. Consecutivos: {id_consecutivos}")

                    
                    # Detener el proceso si encuentra 5 IDs consecutivos
                    if id_consecutivos >= 5:
                        print('ª')
                        # print("Se encontraron 5 IDs consecutivos. Deteniendo proceso.")
                        # detener_scraping = True
                        # break
                        
                    continue
                else:
                    id_consecutivos = 0  # Reiniciar el contador si no es consecutivo

                    # Simular comportamiento humano con pausa aleatoria
                    time.sleep(random.uniform(1, 3))

                    # Detalles del inmueble
                    inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
                    contenido_inmueble = scrape_url(inmueble_url, use_session=True)  # Usar sesión para la petición normal

                    if not contenido_inmueble:
                        print(f"No se pudo obtener contenido para el inmueble {data_element_id}.")
                        continue

                    try:
                        soup_inmueble = BeautifulSoup(contenido_inmueble, 'lxml')
                        
                        # Extraer título del inmueble
                        titulo = soup_inmueble.find("span", {"class": "main-info__title-main"})
                        titulo_text = titulo.get_text(strip=True) if titulo else "N/A"

                        # Extraer subtítulo o tipo
                        subtitle = soup_inmueble.find("span", {"class": "main-info__title-minor"})
                        subtitle_text = subtitle.get_text(strip=True) if subtitle else "N/A"

                        # Extraer el precio
                        price_info = soup_inmueble.find("span", {"class": "info-data-price"})
                        price_text = price_info.get_text(strip=True) if price_info else "N/A"

                        # Extraer precio por metro cuadrado
                        meter_container = soup_inmueble.find("p", {"class": "flex-feature squaredmeterprice"})
                        meter_price = meter_container.find_all("span")[1].text if meter_container else "N/A"

                        # Extraer gastos de comunidad
                        community_section = soup_inmueble.find("section", {"class": "flex-features__container"})
                        community = community_section.find("p", {"class": "flex-feature-details"}).get_text(strip=True) if community_section else "N/A"

                        # Extraer referencia
                        reference_container = soup_inmueble.find("div", {"class": "ad-reference-container"})
                        ref_num = reference_container.find("p", {"class": "txt-ref"}).get_text(strip=True) if reference_container else "N/A"

                        # Extraer última actualización
                        actual_container = soup_inmueble.find("div", {"id": "stats"})
                        actual = actual_container.find("p").get_text(strip=True) if actual_container else "N/A"

                        # Extraer nombre del anunciante
                        anun_container = soup_inmueble.find("div", {"class": "professional-name"})
                        anunciante = anun_container.find("div", {"class": "name"}).get_text(strip=True) if anun_container else "N/A"
                        nombre_anun = anun_container.find("span").get_text(strip=True) if anun_container else "N/A"

                        def clasificar_elementos(lista_elementos):
                            clasificacion = {
                                "direccion": None,
                                "barrio": None,
                                "distrito": None,
                                "ciudad": None,
                                "zona": None,
                                "otros": []
                            }
                            
                            # Diccionario para controlar si una categoría ya ha sido asignada
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
                                
                                # Verificar si 'direccion' está vacía y si el elemento es una dirección
                                if not categorias_asignadas["direccion"] and direccion_regex.match(elemento_strip):
                                    clasificacion["direccion"] = elemento_strip
                                    categorias_asignadas["direccion"] = True
                                    continue  # Pasar al siguiente elemento
                                
                                # Verificar si 'barrio' está vacío y si el elemento es un barrio
                                if not categorias_asignadas["barrio"] and barrio_regex.match(elemento_strip):
                                    clasificacion["barrio"] = elemento_strip
                                    categorias_asignadas["barrio"] = True
                                    continue  # Pasar al siguiente elemento
                                
                                # Verificar si 'distrito' está vacío y si el elemento es un distrito
                                if not categorias_asignadas["distrito"] and distrito_regex.match(elemento_strip):
                                    clasificacion["distrito"] = elemento_strip
                                    categorias_asignadas["distrito"] = True
                                
                                # Verificar si 'ciudad' está vacía y si el elemento contiene una ciudad
                                if not categorias_asignadas["ciudad"] and any(ciudad.lower() in elemento_lower for ciudad in ciudades_murcia):
                                    # Encontrar la primera ciudad que coincide
                                    ciudad_match = next(ciudad for ciudad in ciudades_murcia if ciudad.lower() in elemento_lower)
                                    clasificacion["ciudad"] = ciudad_match
                                    categorias_asignadas["ciudad"] = True
                                    continue  # Pasar al siguiente elemento
                                if not categorias_asignadas["zona"]:
                                    for dir_cardinal in direcciones_cardinales:
                                        if dir_cardinal in elemento_lower:
                                            clasificacion["zona"] = dir_cardinal.capitalize()
                                            categorias_asignadas["zona"] = True
                                            break  # Dejar de buscar direcciones cardinales
                                # Si no ha sido clasificado, añadir a 'otros'
                                clasificacion["otros"].append(elemento_strip)
                            return clasificacion

                        # Modificar dentro del bucle donde extraemos la localización
                        location = soup_inmueble.find("div", {"id": "headerMap"})
                        if location:
                            loc = [lo.text.strip() for lo in location.find_all("li")]
                            # Se coge toda la dirección y se clasfican los elementos
                            # SI hay elementos que no entience, los pone en 'otros'
                            # Eso se puede usar para ir corrigiendo las expresiones regulares
                            direccion_clasificada = clasificar_elementos(loc)
                            street = direccion_clasificada['direccion'] or "N/A"
                            # Si no se detecta ciudad, se pone Murcia
                            ciudad = direccion_clasificada['ciudad'] or "Murcia"
                            # Si no se detectó barrio pero la ciudad es Murcia, ponemos "Murcia" como barrio
                            barrio = direccion_clasificada['barrio'] or "Murcia"
                            # Zona
                            zona = direccion_clasificada['zona'] or "N/A"  # Detecta zona cardinal (Norte, Sur, Este, Oeste)
                            # Concatenar toda la dirección en una sola columna
                            direccion_completa = ', '.join(loc)
                        else:
                            ciudad = street = barrio = zona = "N/A"
                            direccion_completa = "N/A"

                        # Extract property details
                        c1 = soup_inmueble.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})
                        c2 = soup_inmueble.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})
                        basics = [caract.text.strip() for caract in c1.find_all("li")] if c1 else []
                        # TODO: This is not correct
                        if basics:
                            metros = basics[0] if len(basics) > 0 else "N/A"
                            habitaciones = basics[1] if len(basics) > 1 else "N/A"
                            baños = basics[2] if len(basics) > 2 else "N/A"
                        # Extraer teléfono usando la función scrape_url
                        phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"
                        contenido_telefono = scrape_url(phone_url, use_session=False, is_phone_url=True)  # Usar la sesión normal o ScrapingBee
                        telefono = 'N/A'
                        if contenido_telefono:
                            try:
                                if 'phone1' in contenido_telefono and contenido_telefono['phone1']:
                                    telefono = contenido_telefono['phone1']['number']
                            except json.JSONDecodeError:
                                print(f"Error al decodificar el JSON de teléfono para {data_element_id}")
                        else:
                            print(f"Teléfono fallo para el inmueble {data_element_id}")

                        # Agregar el inmueble al DataFrame
                        df = df._append({
                            "id_inmueble": data_element_id,
                            "tipo" : "Ventas",
                            "titulo": titulo_text,
                            "calle": street,
                            "barrio": barrio,
                            "zona": zona,
                            "ciudad": ciudad,
                            "localizacion": direccion_completa,
                            # "direccion_completa": direccion_completa,
                            "precio": price_text,
                            # "Comunidad": community,
                            "precio_metro": meter_price,
                            "caracteristicas": basics,
                            "habitaciones": habitaciones,
                            "baños": baños,
                            "referencia": ref_num,
                            "anunciante": anunciante,
                            "nombre": nombre_anun,
                            "ultima_actualizacion": actual,
                            "tlf": telefono,
                            "URL": inmueble_url,
                            "fecha": fecha_actual,
                        }, ignore_index=True)
                        df.to_csv(csv_file, index=False)
                        print(f"ID {data_element_id} guardado en el CSV.")

                    except Exception as e:
                        print(f"Error procesando el inmueble {data_element_id}: {str(e)}")
                        traceback.print_exc()

    except Exception as e:
        print(f"Error al procesar la página {url}: {str(e)}")
        traceback.print_exc()

# Guardar el DataFrame actualizado en el archivo CSV
df.sort_values(by="fecha", ascending=False, inplace=True)
df.to_csv(csv_file, index=False)
print(f"Datos guardados en {csv_file}.")
