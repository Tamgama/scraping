import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd

csv_file = "alquileres.csv"

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "ID Inmueble", "Tipo", "Título", "Calle", "Barrio", "Distrito", "Ciudad", 
        "Área", "Precio", "Fianza", "Precio/m²", "Características", "Habitaciones", "Baños",
        "Referencia", "Anunciante", "Nombre Anunciante", "Última Actualización", "Teléfono", "URL"
    ])

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": "userUUID=e422d466-febb-41b8-bfce-91b7746ca9a4; SESSION=b736c720ecc0095b~3173737a-ec63-437e-889c-0b98ec436821; utag_main__sn=1; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1mdGRudWxzfG0wNHlxZDlzIn0%3D; _pcid=%7B%22browserId%22%3A%22m04yqd9nqilrs7m0%22%2C%22_t%22%3A%22mftdnv5k%7Cm04yqdtk%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAGb5WSAG4BWfgB9%2BABgAsATwCOrfPxABfIA; didomi_token=eyJ1c2VyX2lkIjoiMTkxNzhmZTMtMzhiMS02NGRjLWIyODAtNDMzYzZiMDM1Y2M4IiwiY3JlYXRlZCI6IjIwMjQtMDgtMjJUMDc6MzA6MTAuOTU1WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTIyVDA3OjMwOjIzLjI4OFoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQDwPsAQDwPsAAHABBENBCFgAAAAAAAAAAAAAAAAAACkoAMAAQUxKQAYAAgpiQgAwABBTEdABgACCmISADAAEFMQ.YAAAAAAAAAAA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22VGLuhkDkzeXqiHVZToIo%22%7D; contact3173737a-ec63-437e-889c-0b98ec436821=\"{'maxNumberContactsAllow':10}\"; _last_search=officialZone; utag_main__prevCompleteClickName=; send3173737a-ec63-437e-889c-0b98ec436821=\"{}\"; cookieSearch-1=\"/alquiler-viviendas/murcia-murcia/:1724312755408\"; datadome=eDYCX7XHZNwZg~MvNbMEgw_B~~3t7N6f7g5BQtJL5RFUkDzwTAYBo9~umAyf6oA9lszhVtxQUwQMgE2x6vLL1EPDxVHX92NbYgDu4X7LkHy8QB~JCOjaNvERUs0H4zIc",
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

            # mas = [caract.text.strip() for caract in c2.find_all("details-property_features")] if c2 else []

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
            print(f"Metros construidos: {metros}")
            print(f"habitaciones: {habitaciones}")
            print(f"baños: {baños}")
            # print(f"otras caracteristicas: {mas}")
            print(f"referencia: {ref_num}")
            print(f"anunciante: {anunciante}")
            print(f"nombre anunciante: {nombre_anun}")
            print(f"tlf: {telefono}")
            print(f"URL: {inmueble_url}")

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
                "m construidos": metros,
                "Habitaciones": habitaciones,
                "Baños": baños,
                # "Más Características": mas,
                "Referencia": ref_num,
                "Anunciante": anunciante,
                "Nombre Anunciante": nombre_anun,
                "Última Actualización": actual,
                "Teléfono": telefono,
                "URL": inmueble_url
            }, ignore_index=True)
            
            # Guardar después de cada inmueble para evitar pérdida de datos en caso de error
            try:
                df.to_csv(csv_file, index=False)
                print(f"ID {data_element_id} guardado en el CSV.")
            except Exception as e:
                print(f"Error al intentar guardar en CSV: {e}")
            
            time.sleep(random.uniform(1, 3))  # Añadir un retraso

# Guardar el DataFrame actualizado en el archivo CSV
try:
    df.to_csv(csv_file, index=False)
    print(f"Datos guardados en {csv_file}.")
except Exception as e:
    print(f"Error al intentar guardar en CSV: {e}")
