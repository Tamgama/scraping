import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd
import traceback
from datetime import datetime
import json

base_url = "https://www.idealista.com/venta-viviendas/murcia-murcia/pagina-{}.htm?ordenado-por=fecha-publicacion-desc"
csv_file = "../src/ventas.csv"

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "ID Inmueble", "Tipo", "Título", "Calle", "Barrio", "Distrito", "Ciudad", 
        "Área", "Precio", "Comunidad", "Precio/m²", "Características", "Habitaciones", "Baños",
        "Referencia", "Anunciante", "Nombre_Anunciante", "Última Actualización", "Teléfono", "URL", "fecha"
    ])


cookie = "userUUID=d24af10d-f04c-473f-aa91-e3423aba66bb; contact1fd4dec7-1c4f-45f9-8c89-8da78f511e15=\"{'maxNumberContactsAllow':10}\"; cookieSearch-1=\"/venta-viviendas/murcia-provincia/:1725101672378\"; SESSION=020cfe1ee892acc9~1fd4dec7-1c4f-45f9-8c89-8da78f511e15; utag_main__pn=17%3Bexp-session; utag_main__sn=1; utag_main_ses_id=1725101674032%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Fventa-viviendas%2Fmurcia-provincia%2Fpagina-2.htm%3Bexp-1725105274103; utag_main__prevVtUrlReferrer=https://www.idealista.com/venta-viviendas/murcia-provincia/%3Bexp-1725105274103; utag_main__prevVtSource=Portal sites%3Bexp-1725105274103; utag_main__prevVtCampaignName=organicWeb%3Bexp-1725105274103; utag_main__prevVtCampaignCode=%3Bexp-1725105274103; utag_main__prevVtCampaignLinkName=%3Bexp-1725105274103; utag_main__prevVtRecipientId=%3Bexp-1725105274103; utag_main__prevVtProvider=%3Bexp-1725105274103; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1nNmZ4YzRkfG0waTB6dXNkIn0%3D; utag_main__ss=0%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1725105274210; utag_main__prevLevel2=005-idealista/portal%3Bexp-1725105274210; _last_search=officialZone; _pcid=%7B%22browserId%22%3A%22m0i0zus9qb0ed4eq%22%2C%22_t%22%3A%22mg6fxc6h%7Cm0i0zuuh%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAOYA2AGYAPAMbD6AH34AGegoBeYMPRABfIA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%222HYtSm2sFoFP17uisl5c%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxYTgxMjgtY2I2Ni02M2U4LWFlYzMtNzc1N2QzNTA1MTAxIiwiY3JlYXRlZCI6IjIwMjQtMDgtMzFUMTA6NTQ6MzMuNjU0WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTMxVDEwOjU0OjM2LjcyNVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQEN6IAQEN6IAAHABBENBDFsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpiUgAwABBTEhABgACCmI6ADAAEFMQkAGAAIKYgAA.f_wAAAAAAAAA; dicbo_id=%7B%22dicbo_fetch%22%3A1725101676758%7D; utag_main__se=3%3Bexp-session; utag_main__st=1725103476777%3Bexp-session; utag_main__prevCompleteClickName=255-idealista/others > > errorClickNameNOTdefined; _gcl_au=1.1.1783634721.1725101677; cto_bundle=YsJnm19lVGMxJTJGN3lqYmZXJTJCekdsJTJGMnFlQ1hic0o3VE1MZDRBemFmdE1Lck9TaEg1RUk4TGJwcDQlMkJEJTJCTlpxVHV3eFdBZ2pOeSUyQlMyYVYybWdpYnZpckQ1Tlg4djZ0Y2FJdUJjMHJXMElEcHolMkJuMlJZekFnb0FMZUdIOE1oWDJzUk1UaFNV; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.idealista.com%252Fventa-viviendas%252Fmurcia-provincia%252Fpagina-2.htm; ABTasty=uid=b5p918fnw1bvn9fb&fst=1725101677227&pst=-1&cst=1725101677227&ns=1&pvt=1&pvis=1&th=; _uetsid=6a4f0e80678711ef8945df302a19b158; _uetvid=6a4f2d30678711ef9fb519bd8a039402; _hjSessionUser_250321=eyJpZCI6IjRiOWFiYWFlLTUyYjktNTM1Ni1iNjkzLTc0M2IzNTBhYmM0ZSIsImNyZWF0ZWQiOjE3MjUxMDE2Nzc0NjYsImV4aXN0aW5nIjpmYWxzZX0=; _hjSession_250321=eyJpZCI6ImUxNjI4NjY5LTExYTEtNDFiNC1iNjE0LTZlZjlhZWU0YjY2NyIsImMiOjE3MjUxMDE2Nzc0NjcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _hjHasCachedUserAttributes=true; _tt_enable_cookie=1; _ttp=BXelFliGdUiDSKR0vifQeBxDYU1; _clck=78hiqq%7C2%7Cfos%7C0%7C1704; _clsk=wh4pel%7C1725101678096%7C1%7C0%7Cu.clarity.ms%2Fcollect; datadome=QS0~dbpUwQju0uV~5xWsu8n~k8OlwdnnTwtQMlhBHjt_vDlSXi6NQndntwg8uExQhZIXqU7vFIlg9nCslzTOgblbnUYtEjTmZK4dIu80Oc0gXZUekcXwT1AZ9lQRn88A"
with open('cookie.json', 'r') as cookie_file:
    config = json.load(cookie_file)
    cookie = config['cookie']
cookie = cookie.encode('utf-8')

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

session = requests.Session()
session.headers.update(headers)  # Actualiza los headers de la sesión con los headers personalizados

# Definir el rango de páginas que quieres recorrer
num_paginas = 162  # Cambia este número según la cantidad de páginas que quieras recorrer

# Contador de IDs consecutivos encontrados
id_consecutivos = 0
# La fecha de ejecuciión de la script
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Bucle para recorrer cada página
for i in range(1, num_paginas + 1):
    url = base_url.format(i)
    try:
        r = session.get(url)
        # Detener el proceso si se recibe un status_code 403 o 429
        if r.status_code in [403, 429]:
            print(f"Deteniendo proceso debido a un status_code {r.status_code} en la página {url}")
            break

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                data_element_id = article.get('data-element-id')
                if data_element_id:
                    data_element_id = int(data_element_id)

                    # Comprobar si el ID ya existe
                    if data_element_id in df["ID Inmueble"].values:
                        id_consecutivos += 1
                        # print(f"ID {data_element_id} ya existe. Saltando...")
                        if id_consecutivos >= 5:
                            print("Se encontraron 5 IDs consecutivos. Deteniendo proceso.")
                            break
                        continue
                    else:
                        id_consecutivos = 0

                    # print(f"Página {i} - data-element-id: {data_element_id}")
                    time.sleep(random.uniform(1, 3))
                    inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
                    try:
                        r = session.get(inmueble_url)
                        # Detener el proceso si se recibe un status_code 403 o 429
                        if r.status_code in [403, 429]:
                            print(f"Deteniendo proceso debido a un status_code {r.status_code} en la URL del inmueble {inmueble_url}")
                            break
                        if r.status_code == 200:
                            soup = BeautifulSoup(r.text, 'lxml')

                            # Extract the title
                            titulo = soup.find("span", {"class": "main-info__title-main"})
                            titulo_text = titulo.get_text(strip=True) if titulo else "N/A"
                            # Extract the subtitle
                            subtitle = soup.find("span", {"class": "main-info__title-minor"})
                            subtitle_text = subtitle.get_text(strip=True) if subtitle else "N/A"

                            # Extract the price
                            price_info = soup.find("span", {"class": "info-data-price"})
                            price_text = price_info.get_text(strip=True) if price_info else "N/A"

                            # Extract the discounted price if available
                            discounted_price_info = soup.find("span", {"class": "pricedown"})
                            discounted_price_text = discounted_price_info.get_text(strip=True) if discounted_price_info else "Sin rebaja"
                            # Extract meter price
                            meter_container = soup.find("p", {"class": "flex-feature squaredmeterprice"})
                            if meter_container:
                                meter = [me.text for me in meter_container.find_all("span")]
                                meter_price = meter[1] if len(meter) > 1 else "N/A"
                            else:
                                meter_price = "N/A"
                            # Extract community expenses
                            community_section = soup.find("section", {"class": "flex-features__container"})
                            if community_section:
                                community = community_section.find("p", {"class": "flex-feature-details"}).get_text(strip=True)
                            else:
                                community = "N/A"

                            reference_container = soup.find("div", {"class": "ad-reference-container"})
                            if reference_container:
                                reference = reference_container.find("p", {"class": "txt-ref"})
                                ref_num = reference.get_text(strip=True) if reference else "N/A"
                            else:
                                ref_num = "N/A"

                            actual_container = soup.find("div", {"id": "stats"})
                            actual = actual_container.find("p").get_text(strip=True) if actual_container else "N/A"

                            anun_container = soup.find("div", {"class": "professional-name"})
                            if anun_container:
                                anun = anun_container.find("div", {"class": "name"})
                                anunciante = anun.get_text(strip=True) if anun else "N/A"
                                nombre_anun = anun_container.find("span").get_text(strip=True) if anun else "N/A"
                            else:
                                anunciante = nombre_anun = "N/A"

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
                            details_section = soup.find("section", {"id": "details"})
                            if details_section:
                                c1 = details_section.find("div", {"class": "details-property-feature-one"})
                                basics = [caract.text for caract in c1.find_all("li")] if c1 else []
                                metros = basics[0] if len(basics) > 0 else "N/A"
                                habitaciones = basics[1] if len(basics) > 1 else "N/A"
                                baños = basics[2] if len(basics) > 2 else "N/A"
                            else:
                                metros = habitaciones = baños = "N/A"

                            phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"
                            res_phone = session.get(phone_url) #('https://api.scraperapi.com', params={'api_key': '98018a479f6fa03d99c74e4ad03fe46b', 'url': phone_url})
                            telefono = 'N/A'
                            if res_phone.status_code == 200:
                                telefono_res = res_phone.json()
                                if ('phone1' in telefono_res and telefono_res['phone1'] and 'number' in telefono_res['phone1']):
                                    telefono = telefono_res['phone1']['number']
                            else:
                                print(f"Teléfono fallo {r.status_code} en la URL {phone_url}")
                            # print(f"Title: {titulo_text}")
                            # print(f"Street: {street}")
                            # print(f"Neighborhood: {neighborhood}")
                            # print(f"District: {district}")
                            # print(f"City: {city}")
                            # print(f"Area: {area}")
                            # print(f"Price: {price_text}")
                            # print(f"Comunidad: {community}")
                            # print(f"€/m²: {meter_price}")
                            # print(f"Caracteristicas: {basics}")
                            # print(f"Metros construidos: {metros}")
                            # print(f"Habitaciones: {habitaciones}")
                            # print(f"Baños: {baños}")
                            # print(f"Referencia: {ref_num}")
                            # print(f"Anunciante: {anunciante}")
                            # print(f"Nombre Anunciante: {nombre_anun}")
                            # print(f"Teléfono: {telefono}")
                            # print(f"URL: {inmueble_url}")
                            df = df._append({
                                "ID Inmueble": data_element_id,
                                "Tipo": "venta",
                                "Título": titulo_text,
                                "Calle": street,
                                "Barrio": neighborhood,
                                "Distrito": district,
                                "Ciudad": city,
                                "Área": area,
                                "Precio": price_text,
                                "Comunidad": community,
                                "Precio/m²": meter_price,
                                "Características": basics,
                                "Habitaciones": habitaciones,
                                "Baños": baños,
                                "Referencia": ref_num,
                                "Anunciante": anunciante,
                                "Nombre_Anunciante": nombre_anun,
                                "Última Actualización": actual,
                                "Teléfono": telefono,
                                "URL": inmueble_url,
                                "fecha": fecha_actual,
                            }, ignore_index=True)
                            df.to_csv(csv_file, index=False)
                            print(f"ID {data_element_id} guardado en el CSV.")
                            time.sleep(random.uniform(1, 3))
                        else:
                            # print(f"Failed to retrieve the webpage for {inmueble_url}. Status code: {r.status_code}")
                            pass
                    except Exception as e:
                        # print(f"Error en la página del inmueble {inmueble_url}: {str(e)}")
                        traceback.print_exc()
                else:
                    # print(f"No se encontró 'data-element-id' en la página {i}.")
                    pass

            if id_consecutivos >= 5:
                print("Se encontraron 5 IDs consecutivos. Deteniendo proceso.")
                break
        else:
            print(f"Failed to retrieve the main page {url}. Status code: {r.status_code}")
            pass
    except Exception as e:
        print(f"Error al procesar la página {url}: {str(e)}")
        traceback.print_exc()

# Guardar el DataFrame actualizado en el archivo CSV
df.sort_values(by="fecha", ascending=False, inplace=True)
df.to_csv(csv_file, index=False)
print(f"Datos guardados en {csv_file}.")
