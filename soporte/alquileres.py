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

cookie = "didomi_token=eyJ1c2VyX2lkIjoiMTkwYTY0NjAtNGU2Yy02NjAyLWIzYjctZjY5ZTMwODYyZWJmIiwiY3JlYXRlZCI6IjIwMjQtMDctMTJUMDk6Mjg6NDUuMDMwWiIsInVwZGF0ZWQiOiIyMDI0LTA3LTEyVDA5OjI4OjQ2LjI1MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQBpHQAQBpHQAAHABBENA8EsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpWUgAwABBSshABgACClY6ADAAEFKwkAGAAIKVgAA.f_wAAAAAAAAA; galleryHasBeenBoosted=true; askToSaveAlertPopUp=false; userUUID=8f2f71a2-57a2-4f40-b912-17aa11d16e88; contactd2c49e00-88aa-4144-83e4-cb3749c16641=\"{'maxNumberContactsAllow':10}\"; sendd2c49e00-88aa-4144-83e4-cb3749c16641=\"{}\"; SESSION=66e212c9a678c6d6~d2c49e00-88aa-4144-83e4-cb3749c16641; utag_main__sn=17; utag_main_ses_id=1725010208762%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Finmueble%2F105846164%2F%3Bexp-1725013808775; utag_main__prevVtUrlReferrer=http://euspay.com/%3Bexp-1725013808775; utag_main__prevVtSource=Direct traffic%3Bexp-1725013808775; utag_main__prevVtCampaignName=organicWeb%3Bexp-1725013808775; utag_main__prevVtCampaignCode=%3Bexp-1725013808775; utag_main__prevVtCampaignLinkName=%3Bexp-1725013808775; utag_main__prevVtRecipientId=%3Bexp-1725013808775; utag_main__prevVtProvider=%3Bexp-1725013808775; utag_main__ss=0%3Bexp-session; _last_search=officialZone; cookieSearch-1=\"/venta-viviendas/murcia-murcia/:1725010507017\"; datadome=Bp7TWXnkrBDFz_ebDR4cvawOYgt8naGZZGdDxGeeN~FIRgFP9mz02Yl5e9qQbGiUFZwrckRLtZcFkBJGymetrNgxe64v4Iwqdm6BtOQl7mDe~jw4VoLQjujrSQoF~sso; utag_main__pn=13%3Bexp-session; utag_main__prevCompleteClickName=; utag_main__se=36%3Bexp-session; utag_main__st=1725012332163%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewAdDetail%3Bexp-1725014132171; utag_main__prevLevel2=005-idealista/portal%3Bexp-1725014132171"
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
