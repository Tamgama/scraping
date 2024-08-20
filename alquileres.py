import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd

excel_file = "alquileres.xlsx"

# Leer el archivo Excel si existe, si no, crear un DataFrame vacío
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=[
        "ID Inmueble", "Tipo", "Título", "Calle", "Barrio", "Distrito",
        "Ciudad", "Área", "Precio", "Fianza", "Precio/m²", "Características",
        "Referencia", "Anunciante", "Nombre Anunciante", "Última Actualización", "Teléfono"
    ])

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": "didomi_token=eyJ1c2VyX2lkIjoiMTkwYTY0NjAtNGU2Yy02NjAyLWIzYjctZjY5ZTMwODYyZWJmIiwiY3JlYXRlZCI6IjIwMjQtMDctMTJUMDk6Mjg6NDUuMDMwWiIsInVwZGF0ZWQiOiIyMDI0LTA3LTEyVDA5OjI4OjQ2LjI1MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQBpHQAQBpHQAAHABBENA8EsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpWUgAwABBSshABgACClY6ADAAEFKwkAGAAIKVgAA.f_wAAAAAAAAA; userUUID=13cf6c96-945f-4fd7-90b8-7a8507150668; _last_search=officialZone; SESSION=b172e53e2c112233~1ae4910c-9295-43eb-aab3-ab691a609b1d; utag_main__sn=8; utag_main_ses_id=1724153221828%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2F%3Bexp-1724156821867; utag_main__prevVtUrlReferrer=%3Bexp-1724156821867; utag_main__prevVtSource=Direct traffic%3Bexp-1724156821867; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724156821867; utag_main__prevVtCampaignCode=%3Bexp-1724156821867; utag_main__prevVtCampaignLinkName=%3Bexp-1724156821867; utag_main__prevVtRecipientId=%3Bexp-1724156821867; utag_main__prevVtProvider=%3Bexp-1724156821867; utag_main__ss=0%3Bexp-session; contact1ae4910c-9295-43eb-aab3-ab691a609b1d=\"{'maxNumberContactsAllow':10}\"; send1ae4910c-9295-43eb-aab3-ab691a609b1d=\"{}\"; galleryHasBeenBoosted=true; utag_main__prevCompleteClickName=; utag_main__pn=9%3Bexp-session; cookieSearch-1=\"/alquiler-viviendas/murcia-murcia/:1724154560515\"; askToSaveAlertPopUp=true; utag_main__se=33%3Bexp-session; utag_main__st=1724156360728%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1724158160746; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724158160746; datadome=qDBIrSsmQVMBMafHWPxa2vFFWhCTDlVF9egXtAIk4kyF4XRstJuUZ0gSbJ2YnO8JaPHsfTxWsu26aHbspcDzzfkPdZpd5LvmrddH7PXBT8uUBvBZ7jgcsJeTJd6qsygB",
    "Referer": "https://www.idealista.com/alquiler-viviendas/murcia-murcia/",
    "Sec-Ch-Device-Memory": "4",
    "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "Sec-Ch-Ua-Full-Version-List": '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.120", "Chromium";v="127.0.6533.120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

session = requests.Session()
session.headers.update(headers)

base_url = "https://www.idealista.com/alquiler-viviendas/murcia-murcia/pagina-{}.htm"

# Definir el rango de páginas que quieres recorrer
num_paginas = 2  # Cambia este número según la cantidad de páginas que quieras recorrer

for i in range(1, num_paginas + 1):
    url = base_url.format(i)
    try:
        r = session.get(url)
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
                print(f"Artículo en la página {i} no tiene 'data-element-id'.")
                continue
            if int(data_element_id) in df["ID Inmueble"].values:
                print(f"ID {data_element_id} ya existe. Saltando...")
                continue
            print(f"Página {i} - data-element-id: {data_element_id}")
            time.sleep(random.uniform(1, 3))  # Añadir un retraso
            inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
            try:
                r = session.get(inmueble_url)
                r.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al intentar acceder a {inmueble_url}: {e}")
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
            meter = soup.find("section", {"class" : "flex-features__container"})
            meter_price = meter.find("span", {"class" : "flex-feature-details"}).get_text(strip=True) if meter else "N/A"
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
            mas = [caract.text.strip() for caract in c2.find_all("details-property_features")] if c2 else []

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
            print(f"Title: {titulo_text}")
            print(f"Street: {street}")
            print(f"Neighborhood: {neighborhood}")
            print(f"District: {district}")
            print(f"City: {city}")
            print(f"Area: {area}")
            print(f"Price: {price_text}")
            print(f"Deposit: {deposit}")
            print(f"€/m²: {meter_price}")
            print(f"Caracteristicas: {basics}")
            print(mas)
            print(ref_num)
            print(anunciante)
            print(nombre_anun)
            print(telefono)

            df = df._append({
                "ID Inmueble": data_element_id,
                "Tipo" : "Alquiler",
                "Título": titulo_text,
                "Calle": street,
                "Barrio": neighborhood,
                "Distrito": district,
                "Ciudad": city,
                "Área": area,
                "Precio": price_text,
                "Fianza": deposit,
                "Características Básicas": basics,
                "Más Características": mas,
                "Referencia": ref_num,
                "Anunciante": anunciante,
                "Nombre Anunciante": nombre_anun,
                "Última Actualización": actual,
                "Teléfono": telefono
            }, ignore_index=True)
            
            # Guardar después de cada inmueble para evitar pérdida de datos en caso de error
            try:
                df.to_excel(excel_file, index=False)
                print(f"ID {data_element_id} guardado en el Excel.")
            except Exception as e:
                print(f"Error al intentar guardar en Excel: {e}")
            
            time.sleep(random.uniform(1, 3))  # Añadir un retraso

# Guardar el DataFrame actualizado en el archivo Excel
try:
    df.to_excel(excel_file, index=False)
    print(f"Datos guardados en {excel_file}.")
except Exception as e:
    print(f"Error al intentar guardar en Excel: {e}")
