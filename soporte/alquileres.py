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
csv_file = os.path.join(base_dir, '../src/alquileres.csv')  # Ruta local al csv

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
        "precio", "precio_metro", "caracteristicas", "habitaciones", "m_construidos", "m_utiles",
        "baños", "referencia", "anunciante", "nombre", "ultima_atualizacion", "tlf", "url", "fecha"
    ])

cookie = "userUUID=d24af10d-f04c-473f-aa91-e3423aba66bb; contact1fd4dec7-1c4f-45f9-8c89-8da78f511e15=\"{'maxNumberContactsAllow':10}\"; cookieSearch-1=\"/venta-viviendas/murcia-provincia/:1725101672378\"; SESSION=020cfe1ee892acc9~1fd4dec7-1c4f-45f9-8c89-8da78f511e15; utag_main__pn=17%3Bexp-session; utag_main__sn=1; utag_main_ses_id=1725101674032%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Fventa-viviendas%2Fmurcia-provincia%2Fpagina-2.htm%3Bexp-1725105274103; utag_main__prevVtUrlReferrer=https://www.idealista.com/venta-viviendas/murcia-provincia/%3Bexp-1725105274103; utag_main__prevVtSource=Portal sites%3Bexp-1725105274103; utag_main__prevVtCampaignName=organicWeb%3Bexp-1725105274103; utag_main__prevVtCampaignCode=%3Bexp-1725105274103; utag_main__prevVtCampaignLinkName=%3Bexp-1725105274103; utag_main__prevVtRecipientId=%3Bexp-1725105274103; utag_main__prevVtProvider=%3Bexp-1725105274103; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1nNmZ4YzRkfG0waTB6dXNkIn0%3D; utag_main__ss=0%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1725105274210; utag_main__prevLevel2=005-idealista/portal%3Bexp-1725105274210; _last_search=officialZone; _pcid=%7B%22browserId%22%3A%22m0i0zus9qb0ed4eq%22%2C%22_t%22%3A%22mg6fxc6h%7Cm0i0zuuh%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAOYA2AGYAPAMbD6AH34AGegoBeYMPRABfIA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%222HYtSm2sFoFP17uisl5c%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxYTgxMjgtY2I2Ni02M2U4LWFlYzMtNzc1N2QzNTA1MTAxIiwiY3JlYXRlZCI6IjIwMjQtMDgtMzFUMTA6NTQ6MzMuNjU0WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTMxVDEwOjU0OjM2LjcyNVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQEN6IAQEN6IAAHABBENBDFsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpiUgAwABBTEhABgACCmI6ADAAEFMQkAGAAIKYgAA.f_wAAAAAAAAA; dicbo_id=%7B%22dicbo_fetch%22%3A1725101676758%7D; utag_main__se=3%3Bexp-session; utag_main__st=1725103476777%3Bexp-session; utag_main__prevCompleteClickName=255-idealista/others > > errorClickNameNOTdefined; _gcl_au=1.1.1783634721.1725101677; cto_bundle=YsJnm19lVGMxJTJGN3lqYmZXJTJCekdsJTJGMnFlQ1hic0o3VE1MZDRBemFmdE1Lck9TaEg1RUk4TGJwcDQlMkJEJTJCTlpxVHV3eFdBZ2pOeSUyQlMyYVYybWdpYnZpckQ1Tlg4djZ0Y2FJdUJjMHJXMElEcHolMkJuMlJZekFnb0FMZUdIOE1oWDJzUk1UaFNV; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.idealista.com%252Fventa-viviendas%252Fmurcia-provincia%252Fpagina-2.htm; ABTasty=uid=b5p918fnw1bvn9fb&fst=1725101677227&pst=-1&cst=1725101677227&ns=1&pvt=1&pvis=1&th=; _uetsid=6a4f0e80678711ef8945df302a19b158; _uetvid=6a4f2d30678711ef9fb519bd8a039402; _hjSessionUser_250321=eyJpZCI6IjRiOWFiYWFlLTUyYjktNTM1Ni1iNjkzLTc0M2IzNTBhYmM0ZSIsImNyZWF0ZWQiOjE3MjUxMDE2Nzc0NjYsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_250321=eyJpZCI6ImUxNjI4NjY5LTExYTEtNDFiNC1iNjE0LTZlZjlhZWU0YjY2NyIsImMiOjE3MjUxMDE2Nzc0NjcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjHasCachedUserAttributes=true; _tt_enable_cookie=1; _ttp=BXelFliGdUiDSKR0vifQeBxDYU1; _clck=78hiqq%7C2%7Cfos%7C0%7C1704; _clsk=wh4pel%7C1725101678096%7C1%7C0%7Cu.clarity.ms%2Fcollect; datadome=QS0~dbpUwQju0uV~5xWsu8n~k8OlwdnnTwtQMlhBHjt_vDlSXi6NQndntwg8uExQhZIXqU7vFIlg9nCslzTOgblbnUYtEjTmZK4dIu80Oc0gXZUekcXwT1AZ9lQRn88A"
with open(os.path.join(base_dir, './cookie.json'), 'r') as cookie_file:
    config = json.load(cookie_file)
    cookie = config['cookie']
cookie = cookie.encode('utf-8')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
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

base_url = "https://www.idealista.com/alquiler-viviendas/murcia-murcia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc"

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
            meter_container = soup.find("p", {"class" :"flex-feature squaredmeterprice"})
            meter = [me.text for me in meter_container.find_all("span")]
            meter_price = meter[1] if len(meter) > 1 else "N/A"
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
                "tipo" : "Alquiler",
                "titulo": titulo_text,
                "calle": street,
                "barrio": barrio,
                "zona": zona,
                "ciudad": ciudad,
                "localizacion": direccion_completa,
                # "direccion_completa": direccion_completa,
                "precio": price_text,
                # "Fianza": deposit,
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
