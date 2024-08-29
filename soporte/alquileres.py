import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

csv_file = "../src/alquileres.csv"

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "ID_Inmueble", "Tipo", "Título", "Calle", "Barrio", "Distrito", "Ciudad", "Área", 
        "Precio", "Fianza", "Precio_por_metro", "Características", "Habitaciones", "Metros_construidos", "Metros_utiles",
        "Baños", "Referencia", "Anunciante", "Nombre_Anunciante", "Última_Actualización", "Teléfono", "URL", "fecha"
    ])

cookie = "userUUID=aef1f78c-1f0d-4b80-b9d0-b3da669e6af2; SESSION=8d22938e76c6721d~748444cf-a939-444c-a0c3-a04405504f34; utag_main__sn=1; utag_main_ses_id=1724962906637%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2F%3Bexp-1724966506728; utag_main__prevVtUrlReferrer=https://www.idealista.com/%3Bexp-1724966506728; utag_main__prevVtSource=Portal sites%3Bexp-1724966506728; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724966506728; utag_main__prevVtCampaignCode=%3Bexp-1724966506728; utag_main__prevVtCampaignLinkName=%3Bexp-1724966506728; utag_main__prevVtRecipientId=%3Bexp-1724966506728; utag_main__prevVtProvider=%3Bexp-1724966506728; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1nNDViMm0zfG0wZnFkbGEzIn0%3D; utag_main__ss=0%3Bexp-session; _pcid=%7B%22browserId%22%3A%22m0fqdla0gbzyz29e%22%2C%22_t%22%3A%22mg45b2mh%7Cm0fqdlah%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAOYAWAKwAjAEz96AH34AGAGYBHVqkL0QAXyA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22GELapLMuNXE9mbrZrLGa%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxOWZjZDItMTFhZC02ZDFkLTkzZGYtZmRlMjZmYWNiYWRhIiwiY3JlYXRlZCI6IjIwMjQtMDgtMjlUMjA6MjE6NDYuMzk0WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTI5VDIwOjIxOjQ4Ljg2NVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQEHUQAQEHUQAAHABBENBDFsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpiUgAwABBTEhABgACCmI6ADAAEFMQkAGAAIKYgAA.f_wAAAAAAAAA; dicbo_id=%7B%22dicbo_fetch%22%3A1724962908919%7D; _hjSession_250321=eyJpZCI6IjUwNWVhNzM0LWZhZmUtNDRkMC04NmJkLTZiZTEyNjJkNDUyMiIsImMiOjE3MjQ5NjI5MDk0MjEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjHasCachedUserAttributes=true; _clck=12y5fnl%7C2%7Cfoq%7C0%7C1702; _tt_enable_cookie=1; _ttp=pTdm1SDYUKlCKQEJZx9RpzQPNsX; _hjSessionUser_250321=eyJpZCI6ImUyNjdjZDExLTVkMDktNTQwNS05NmU0LTQ1YmE5ZTE0ZTQ4YyIsImNyZWF0ZWQiOjE3MjQ5NjI5MDk0MTksImV4aXN0aW5nIjp0cnVlfQ==; _fbp=fb.1.1724962918367.300569546132576624; contact748444cf-a939-444c-a0c3-a04405504f34=\"{'maxNumberContactsAllow':10}\"; _last_search=officialZone; _gcl_au=1.1.1424415289.1724962921; send748444cf-a939-444c-a0c3-a04405504f34=\"{}\"; cookieSearch-1=\"/venta-viviendas/murcia-murcia/:1724962939495\"; askToSaveAlertPopUp=false; utag_main__pn=5%3Bexp-session; utag_main__prevCompleteClickName=; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.idealista.com%252F; ABTasty=uid=a5brb107k7p221ah&fst=1724962909255&pst=-1&cst=1724962909255&ns=1&pvt=6&pvis=6&th=1286379.-1.1.1.1.1.1724962940490.1724962940491.0.1; _uetsid=52072500664411ef99a2abbf7f062670; _uetvid=52074620664411efa99ebb4efe097569; utag_main__se=14%3Bexp-session; utag_main__st=1724964740784%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1724966540790; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724966540790; _clsk=j2aelk%7C1724962940921%7C6%7C0%7Cx.clarity.ms%2Fcollect; cto_bundle=5S0ecV9sd1JZaXolMkZSUlZUbjhkdkZOSkFuT0ZHZ0clMkJ0NUZMb0lPNWJUN1dMQTg0NTV6azM4biUyQmFKVFRMZDE3Vm5ibkw2TkJzNzRVeEdBOXRtMkN6WlFrbzg1ciUyQkhDbnRKaEw0JTJGRmVpeE81eGxWVWdYciUyRnUyb2pHZUlQWkQ0ciUyQnpWclBx; datadome=7K2RS8mGu0SRjcNx~T0PFLIkLXPVqYNJE2QLzHAHiUzR2sQJ0EmFP0FXEqZ4r6fhU~h0l1BcKW0djYF9zTIz7V7exFGxNV2_dOuI55Z~9BoVt6n6b6F0Wjq0bKNgHxkG"
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

base_url = "https://www.idealista.com/alquiler-viviendas/murcia-murcia/pagina-{}.htm"

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
            
            if data_element_id in df["ID_Inmueble"].values:
                id_consecutivos += 1
                # print(f"ID {data_element_id} ya existe. Saltando...")
                
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
            # Extract location list
            location = soup.find("div", {"id": "headerMap"})
            if location:
                loc = [lo.text for lo in location.find_all("li")]
                street = loc[0] if len(loc) > 0 else "N/A"
                neighborhood = loc[1] if len(loc) > 1 else "N/A"
                district = loc[2] if len(loc) > 2 else "N/A"
                city = loc[3] if len(loc) > 3 else "N/A"
                area = loc[4] if len(loc) > 4 else "N/A"
            else:
                street = neighborhood = district = city = area = "N/A"
            # Extract property details
            c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})
            c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})
            basics = [caract.text.strip() for caract in c1.find_all("li")] if c1 else []
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

            # Print extracted information
            # print(f"Título: {titulo_text}")
            # print(f"Calle: {street}")
            # print(f"Barrio: {neighborhood}")
            # print(f"Distrito: {district}")
            # print(f"Ciudad: {city}")
            # print(f"Área: {area}")
            # print(f"Precio: {price_text}")
            # print(f"Fianza: {deposit}")
            # print(f"Precio_por_metro: {meter_price}")
            # print(f"Caracteristicas: {basics}")
            # print(f"Metros_construidos: {metros}")
            # print(f"habitaciones: {habitaciones}")
            # print(f"baños: {baños}")
            # print(f"referencia: {ref_num}")
            # print(f"anunciante: {anunciante}")
            # print(f"nombre anunciante: {nombre_anun}")
            # print(f"tlf: {telefono}")
            # print(f"URL: {inmueble_url}")
            df = df._append({
                "ID_Inmueble": data_element_id,
                "Tipo" : "Alquiler",
                "Título": titulo_text,
                "Calle": street,
                "Barrio": neighborhood,
                "Distrito": district,
                "Ciudad": city,
                "Área": area,
                "Precio": price_text,
                "Fianza": deposit,
                "Precio_por_metro": meter_price,
                "Características": basics,
                "Habitaciones": habitaciones,
                "Baños": baños,
                "Referencia": ref_num,
                "Anunciante": anunciante,
                "Referencia": ref_num,
                "Anunciante": anunciante,
                "Nombre_Anunciante": nombre_anun,
                "Última_Actualización": actual,
                "Teléfono": telefono,
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
