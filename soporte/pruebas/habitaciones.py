import requests
import time
import random
import os
import re
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, 'habitaciones.csv')  # Ruta local al csv

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

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "id_inmueble", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion", 
        "precio", "precio_metro", "caracteristicas", "habitaciones",
        "baños", "referencia", "anunciante", "nombre", "tlf", "url", "fecha"
    ])

cookie = "userUUID=1f1ee681-4f5b-4298-b36e-a09be8a51f45; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1tcWZmc213fG03MjBpYmF3In0%3D; _pcid=%7B%22browserId%22%3A%22m720ibasigb7eljq%22%2C%22_t%22%3A%22mmqffsr8%7Cm720ibf8%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbfgEcAZiIgwARgB9%2BAdgBMABnqSRkkAF8gA; didomi_token=eyJ1c2VyX2lkIjoiMTk0ZmE5NTMtZTZmMS02OTI2LTliZGQtZTVmMDUwM2ZiZDJjIiwiY3JlYXRlZCI6IjIwMjUtMDItMTJUMTQ6MzQ6MzIuNDMxWiIsInVwZGF0ZWQiOiIyMDI1LTAyLTEyVDE0OjM0OjM0LjMwOFoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQMtu0AQMtu0AAHABBENBcFgAAAAAAAAAAAAAAAAAACkoAMAAQVnKQAYAAgrOQgAwABBWcdABgACCs4SADAAEFZw.YAAAAAAAAAAA; _last_search=officialZone; galleryHasBeenBoosted=true; askToSaveAlertPopUp=false; utag_main__sn=2; utag_main__prevTsReferrer=https://www.idealista.com/alquiler-habitacion/murcia-murcia/?ordenado-por; contact9c4ee63f-bbe0-457f-8de2-40544d385a51=\"{'maxNumberContactsAllow':10}\"; cookieSearch-1=\"/alquiler-habitacion/murcia-murcia/:\"; utag_main__prevCompleteClickName=; send9c4ee63f-bbe0-457f-8de2-40544d385a51=\"{}\"; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-02-12T15%3A56%3A11.216Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22KVh9yFAe0tLRSu8IlFhk%22%2C%22expiryDate%22%3A%222026-02-12T15%3A56%3A11.216Z%22%7D; SESSION=9eaffb1dddf32854~2b1f2560-eacb-420d-90a4-b227822bde79; datadome=3FDXW8RbxUOyti2WjLJMv~F~98zYIebNHcgjzguLCTjlNXK8Dob8ood4PQ5veqcgWN49Jzd9gTIfQcjvhKuxYSITeuXeIDNg2CVFh6JiRqGyzBqE~zVVLYX~QhoX9qb4"
# with open(os.path.join(base_dir, './cookie.json'), 'r') as cookie_file:
#     config = json.load(cookie_file)
#     cookie = config['cookie']
cookie = cookie.encode('utf-8')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": cookie,
    "Referer": "https://www.idealista.com/alquiler-habitacion/murcia-murcia/",
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

base_url = "https://www.idealista.com/alquiler-habitacion/murcia-murcia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc"

# Definir el rango de páginas que quieres recorrer
num_paginas = 40  # Cambia este número según la cantidad de páginas que quieras recorrer

# Contador de IDs consecutivos encontrados
id_consecutivos = 0

# La fecha de ejecución de la script
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for i in range(1, num_paginas + 1):
    url = base_url.format(i)
    try:
        r = session.get(url)
        # Detener el proceso si se recibe un status_code 403 o 429
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
    # Extraer y mostrar el atributo 'data-element-id'
        for article in articles:
            data_element_id = article.get('data-element-id')
            if not data_element_id:
                # print(f"Artículo en la página {i} no tiene 'data-element-id'.")
                continue
            data_element_id = int(data_element_id)
            
            if data_element_id in df["id_inmueble"].values:
                id_consecutivos += 1
                print(f"ID {data_element_id} ya existe. Saltando...")
                
                # Si se encuentran 5 IDs consecutivos, detener el proceso
                if id_consecutivos >= 5:
                    print("Se encontraron 5 IDs consecutivos. Deteniendo proceso.")
                    break
                continue
            else:
                id_consecutivos = 0  # Reiniciar contador si se encuentra un ID nuevo

            # print(f"Página {i} - data-element-id: {data_element_id}")
            time.sleep(random.uniform(1, 3))  # Añadir un retraso

            inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
            try:
                r = session.get(inmueble_url)
                
                # Detener el proceso si se recibe un status_code 403 o 429
                if r.status_code in [403, 429]:
                    print(f"Deteniendo proceso debido a un status_code {r.status_code} en la URL del inmueble {inmueble_url}")
                    break
                r.raise_for_status()
            except requests.RequestException as e:
                # print(f"Error al intentar acceder a {inmueble_url}: {e}")
                continue
            soup = BeautifulSoup(r.text, 'lxml')
            
            # Extract the title
            titulo = soup.find("span", {"class": "main-info__title-main"})
            titulo_text = titulo.get_text(strip=True) if titulo else "N/A"
            # Extract the price
            price_info = soup.find("span", {"class": "info-data-price"})
            price_text = price_info.get_text(strip=True) if price_info else "N/A"
            # Extract the deposit if available
            deposit_container = soup.find("span", {"class": "txt-deposit"})
            deposit = deposit_container.get_text(strip=True) if deposit_container else "N/A"

            # Extract meter price
            # meter_container = soup.find("p", {"class" :"flex-feature squaredmeterprice"})
            # meter = [me.text for me in meter_container.find_all("span")]
            # meter_price = meter[1] if len(meter) > 1 else "N/A"

            # Extract reference
            reference_container = soup.find("div", {"class": "ad-reference-container"})
            if reference_container:
                reference = reference_container.find("p", {"class": "txt-ref"})
                ref_num = reference.get_text(strip=True) if reference else "N/A"
            else:
                ref_num = "N/A"

            # Extract last update
            actual_container = soup.find("div", {"id" : "stats"})
            actual = actual_container.find("p").get_text(strip=True) if actual_container else "N/A"

            # Extract anunciante
            anun_container = soup.find("div", {"class": "professional-name"})
            if anun_container:
                anun = anun_container.find("div", {"class": "name"})
                anunciante = anun.get_text(strip=True) if anun else "N/A"
                nombre_anun = anun_container.find("span").get_text(strip=True) if anun else "N/A"
            else:
                anunciante = "N/A"
                nombre_anun = "N/A"
            
            # Función para detectar barrios o pueblos y asignarlos a la columna "barrio"
            def detectar_barrio(loc_data):
                # Buscamos Cualquier cosa que empiece por barrio
                barrio_pattern = r'\bbarrio [a-zA-Z]+\b'  # Detecta cualquier palabra que podría ser un barrio o pueblo
                # Detectamos si hay otro pueblo o barrio
                for loc in loc_data:
                    texto = loc
                    barrios = re.findall(barrio_pattern, texto, re.IGNORECASE)
                    if barrios:
                       return barrios[0]  # Puedes ajustar si detectas varios. Aquí guardamos el primer pueblo o barrio detectado.
                return ''
            
            # Función para identificar si una palabra está relacionada 
            # con cardinalidad (norte, sur, este, oeste)
            def detectar_zona(loc_data):
                for loc in loc_data:
                    texto = loc  
                    if re.search(r'\bnorte\b', texto, re.IGNORECASE):
                        return "Norte"
                    elif re.search(r'\bsur\b', texto, re.IGNORECASE):
                        return "Sur"
                    elif re.search(r'\beste\b', texto, re.IGNORECASE):
                        return "Este"
                    elif re.search(r'\boeste\b', texto, re.IGNORECASE):
                        return "Oeste"
                return ""
            
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
            location = soup.find("div", {"id": "headerMap"})
            if location:
                loc = [lo.text.strip() for lo in location.find_all("li")]
                # Se coge toda la dirección y se clasfican los elementos
                # Si hay elementos que no entience, los pone en 'otros'
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
                street = barrio = zona = "N/A"
                direccion_completa = "N/A"

            # Extract property details
            c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})
            c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})
            basics = [caract.text.strip() for caract in c1.find_all("li")] if c1 else []
            # TODO: This is not correct, for now is cleaned in limpieza,py
            if basics:
                metros = basics[0] if len(basics) > 0 else "N/A"
                habitaciones = basics[1] if len(basics) > 1 else "N/A"
                baños = basics[2] if len(basics) > 2 else "N/A"
            # Extract phone number
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

            df = df._append({
                "id_inmueble": data_element_id,
                "tipo" : "Habitación",
                "titulo": titulo_text,
                "calle": street,
                "barrio": barrio,
                "zona": zona,
                "ciudad": ciudad,
                "localizacion": direccion_completa,
                # "direccion_completa": direccion_completa,
                "precio": price_text,
                # "Fianza": deposit,
                "precio_metro": "0",
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

            # Guardar después de cada inmueble para evitar pérdida de datos en caso de error
            try:
                df.to_csv(csv_file, index=False)
                print(f"ID {data_element_id} guardado en el CSV.")
            except Exception as e:
                print(f"Error al intentar guardar en CSV: {e}")
            time.sleep(random.uniform(1, 3))  # Añadir un retraso
    if id_consecutivos >= 5:  # Salir del bucle principal si se encontraron 5 IDs consecutivos
        print("Se encontraron 5 IDs consecutivos. Deteniendo proceso.")
        break
# Guardar el DataFrame actualizado en el archivo CSV al finalizar el proceso
try:
    df.sort_values(by="fecha", ascending=False, inplace=True)
    df.to_csv(csv_file, index=False)
    print(f"Datos guardados en {csv_file}.")
except Exception as e:
    print(f"Error al intentar guardar en CSV: {e}")