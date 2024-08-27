import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd
import traceback
from scrapingbee import ScrapingBeeClient

# client = ScrapingBeeClient(api_key="XEO00EHKJ3U98JFMIS5R545KO9ZJZVJTGPM3Z11QF9A24E47MMTX9O8H2ZGK2UZTGPHYH0LCQ87E7TP3")

base_url = "https://www.idealista.com/venta-viviendas/murcia-murcia/pagina-{}.htm"

# response = client.get(base_url, params={})

csv_file = "ventas.csv"

# Leer el archivo CSV si existe, si no, crear un DataFrame vacío
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=[
        "ID Inmueble", "Tipo", "Título", "Calle", "Barrio", "Distrito", "Ciudad", 
        "Área", "Precio", "Comunidad", "Precio/m²", "Características", "Habitaciones", "Baños",
        "Referencia", "Anunciante", "Nombre Anunciante", "Última Actualización", "Teléfono", "URL"
    ])

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie": "utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Fventa-viviendas%2Fmurcia-murcia%2F%3Bexp-1724746506830; utag_main__prevVtUrlReferrer=https://www.idealista.com/inmueble/105236581/%3Bexp-1724746506830; utag_main__prevVtSource=Portal sites%3Bexp-1724746506830; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724746506830; utag_main__prevVtCampaignCode=%3Bexp-1724746506830; utag_main__prevVtCampaignLinkName=%3Bexp-1724746506830; utag_main__prevVtRecipientId=%3Bexp-1724746506830; utag_main__prevVtProvider=%3Bexp-1724746506830; _last_search=officialZone; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1nMGlicGt5fG0wYzNlODh5In0%3D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22I2UUuCQM81LHvZ19EVwS%22%7D; _pcid=%7B%22browserId%22%3A%22m0c3e88spghftp6o%22%2C%22_t%22%3A%22mg0ibq6g%7Cm0c3e8ug%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAOYAGegCMAjgDYAFgB9%2BwgMYBmKAA4w9EAF8gA; SESSION=1b732e08a8140e05~af6f5e53-5f9c-4ec9-ae8e-72c234433188; smc=\"{}\"; utag_main__sn=2; utag_main_ses_id=1724745148632%3Bexp-session; utag_main__ss=0%3Bexp-session; dicbo_id=%7B%22dicbo_fetch%22%3A1724745149649%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxOTJiMDItZjBhNC02NjllLTliMzItZTU4MzI5ZjhlMmE3IiwiY3JlYXRlZCI6IjIwMjQtMDgtMjdUMDc6MTU6MDUuNjEwWiIsInVwZGF0ZWQiOiIyMDI0LTA4LTI3VDA3OjUyOjQwLjM1MloiLCJ2ZXJzaW9uIjoyLCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVuZG9ycyI6eyJkaXNhYmxlZCI6WyJnb29nbGUiLCJjOmxpbmtlZGluLW1hcmtldGluZy1zb2x1dGlvbnMiLCJjOm1peHBhbmVsIiwiYzphYnRhc3R5LUxMa0VDQ2o4IiwiYzpob3RqYXIiLCJjOmJlYW1lci1IN3RyN0hpeCIsImM6dGVhbGl1bWNvLURWRENkOFpQIiwiYzp0aWt0b2stS1pBVVFMWjkiLCJjOmdvb2dsZWFuYS00VFhuSmlnUiIsImM6aWRlYWxpc3RhLUx6dEJlcUUzIiwiYzppZGVhbGlzdGEtZmVSRWplMmMiLCJjOmNvbnRlbnRzcXVhcmUiLCJjOm1pY3Jvc29mdCJdfSwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQEAuYAQEAuYAAHABBENBDFgAAAAAAAAAAAAAAAAAACkoAMAAQUxKQAYAAgpiQgAwABBTEdABgACCmISADAAEFMQ.YAAAAAAAAAAA; utag_main__prevCompleteClickName=; contactaf6f5e53-5f9c-4ec9-ae8e-72c234433188=\"{'maxNumberContactsAllow':10}\"; cookieSearch-1=\"/venta-viviendas/murcia-murcia/:1724745170939\"; utag_main__pn=5%3Bexp-session; utag_main__se=13%3Bexp-session; utag_main__st=1724746972277%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1724748772287; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724748772287; datadome=FZ0eaLqf0cGfC1OQ4F3JeGvoO7uO7iq43BGQ2FgNRu7Rg5RTVr0CRIPXP99Xcdeap9tNuw~H_oNF0vpDeGhH_Ca2eRkcStn2KQFO_q62efw_nCEI5uABGQ2MgLlo0BOS",
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
session.headers.update(headers)


# Definir el rango de páginas que quieres recorrer
num_paginas = 162  # Cambia este número según la cantidad de páginas que quieras recorrer
# Bucle para recorrer cada página
for i in range(1, num_paginas + 1):
    # Generar la URL de la página actual
    url = base_url.format(i)
    try:
        r = session.get(base_url)
        if r.status_code == 200:
            # Parsear el contenido HTML
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Buscar todos los elementos 'article'
            articles = soup.find_all('article')
            
            # Extraer y mostrar el atributo 'data-element-id'
            for article in articles:
                data_element_id = article.get('data-element-id')
                if data_element_id:
                    data_element_id = int(data_element_id)
                    if data_element_id in df["ID Inmueble"].values:
                        print(f"ID {data_element_id} ya existe. Saltando...")
                        continue  # Saltar al siguiente inmueble si el ID ya existe
                    print(f"Página {i} - data-element-id: {data_element_id}")
                    time.sleep(random.uniform(1, 3))  # Añadir un retraso
                    inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
                    try:
                        r = session.get(inmueble_url)
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
                            res_phone = session.get(phone_url)
                            telefono = 'N/A'
                            if res_phone.status_code == 200:
                                telefono_res = res_phone.json()
                                if ('phone1' in telefono_res and telefono_res['phone1'] and 'number' in telefono_res['phone1']):
                                    telefono = telefono_res['phone1']['number']

                            print(f"Title: {titulo_text}")
                            print(f"Street: {street}")
                            print(f"Neighborhood: {neighborhood}")
                            print(f"District: {district}")
                            print(f"City: {city}")
                            print(f"Area: {area}")
                            print(f"Price: {price_text}")
                            print(f"Comunidad: {community}")
                            print(f"€/m²: {meter_price}")
                            print(f"Caracteristicas: {basics}")
                            print(f"Metros construidos: {metros}")
                            print(f"Habitaciones: {habitaciones}")
                            print(f"Baños: {baños}")
                            print(f"Referencia: {ref_num}")
                            print(f"Anunciante: {anunciante}")
                            print(f"Nombre Anunciante: {nombre_anun}")
                            print(f"Teléfono: {telefono}")
                            print(f"URL: {inmueble_url}")

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
                                "Nombre Anunciante": nombre_anun,
                                "Última Actualización": actual,
                                "Teléfono": telefono,
                                "URL": inmueble_url
                            }, ignore_index=True)

                            df.to_csv(csv_file, index=False)
                            print(f"ID {data_element_id} guardado en el CSV.")
                            time.sleep(random.uniform(1, 3))  # Añadir un retraso
                        else:
                            print(f"Failed to retrieve the webpage for {inmueble_url}. Status code: {r.status_code}")
                    except Exception as e:
                        print(f"Error en la página del inmueble {inmueble_url}: {str(e)}")
                        traceback.print_exc()
                else:
                    print(f"No se encontró 'data-element-id' en la página {i}.")
        else:
            print(f"Failed to retrieve the main page {url}. Status code: {r.status_code}")
    except Exception as e:
        print(f"Error al procesar la página {url}: {str(e)}")
        traceback.print_exc()

# Guardar el DataFrame actualizado en el archivo CSV
df.to_csv(csv_file, index=False)
print(f"Datos guardados en {csv_file}.")
