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
        "Ciudad", "Área", "Precio", "Fianza", "Características", "Referencia", 
        "Anunciante", "Nombre Anunciante", "Última Actualización", "Teléfono"
    ])

headers = {
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "max-age=0",
    "cookie":
    "userUUID=b9b3bcef-e87d-49ac-9f01-e3af81da91ea; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1mcDQzcXAyfG0wMHA2OWQyIn0%3D; _pcid=%7B%22browserId%22%3A%22m00p69cya2bkot6y%22%2C%22_t%22%3A%22mfp43r8f%7Cm00p69wf%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAGYAHACwBmGAA4AVgB9%2BABkXCAbAE4A7jJABfIA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22G8LF1SQJJZjK50FkS10U%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxNjk5ZWEtOWE3OC02MTY1LWExMDctOWRjZTU3ZDgwNzcyIiwiY3JlYXRlZCI6IjIwMjQtMDgtMTlUMDc6NTE6MzEuNDk1WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTE5VDA3OjUyOjA5LjUzMloiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQDmW4AQDmW4AAHABBENBBFgAAAAAAAAAAAAAAAAAACkoAMAAQUxKQAYAAgpiQgAwABBTEdABgACCmISADAAEFMQ.YAAAAAAAAAAA; _last_search=officialZone; utag_main__prevCompleteClickName=; discrentingbdmi=true; galleryHasBeenBoosted=true; SESSION=aef06c73bc8de1dd~955637c9-93a9-4834-b97a-4ba15b1ddf90; smc=\"{}\"; utag_main__sn=6; utag_main_ses_id=1724076958070%3Bexp-session; utag_main__ss=0%3Bexp-session; contact955637c9-93a9-4834-b97a-4ba15b1ddf90=\"{'maxNumberContactsAllow':10}\"; send955637c9-93a9-4834-b97a-4ba15b1ddf90=\"{}\"; dicbo_id=%7B%22dicbo_fetch%22%3A1724078426948%7D; cookieSearch-1=\"/alquiler-viviendas/murcia-murcia/:1724078435030\"; utag_main__pn=12%3Bexp-session; utag_main__se=26%3Bexp-session; utag_main__st=1724080236814%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Falquiler-viviendas%2Fmurcia-murcia%2Fpagina-2.htm%3Bexp-1724082036880; utag_main__prevVtUrlReferrer=https://www.idealista.com/alquiler-viviendas/murcia-murcia/%3Bexp-1724082036880; utag_main__prevVtSource=Portal sites%3Bexp-1724082036880; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724082036880; utag_main__prevVtCampaignCode=%3Bexp-1724082036880; utag_main__prevVtCampaignLinkName=%3Bexp-1724082036880; utag_main__prevVtRecipientId=%3Bexp-1724082036880; utag_main__prevVtProvider=%3Bexp-1724082036880; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1724082036882; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724082036882; datadome=TiH0FLJnCEerwQn1fzkXpp4QYZbxEcI05~YGD1XLqdqSpN1ihZuTUnG~gaKsiStflpJQPTzbozkWiStFucje0uUBe5wnNQnHEyaMJjZFq88FgSiwH6aK7ZJaN9QcfXh3",
    "Priority": "u=0, i",
    "Referer": "https://www.idealista.com/alquiler-viviendas/murcia-murcia/",
    "Sec-Ch-Device-Memory": "8",
    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "Sec-Ch-Ua-Full-Version-List": '"Not;A Brand";v="8.0.0.0", "Chromium";v="126.0.6478.126", "Google Chrome";v="126.0.6478.126"',
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

base_url = "https://www.idealista.com/alquiler-viviendas/murcia-murcia.htm"

# Definir el rango de páginas que quieres recorrer
num_paginas = 2  # Cambia este número según la cantidad de páginas que quieras recorrer
# Bucle para recorrer cada página
for i in range(1, num_paginas + 1):
    # Generar la URL de la página actual
    url = base_url.format(i)
    try:
        r = session.get(url)
        if r.status_code == 200:
            # Parsear el contenido HTML
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Buscar todos los elementos 'article'
            articles = soup.find_all('article')
            
            # Extraer y mostrar el atributo 'data-element-id'
            for article in articles:
                data_element_id = article.get('data-element-id')
                if data_element_id:
                    if int(data_element_id) in df["ID Inmueble"].values:
                        print(f"ID {data_element_id} ya existe. Saltando...")
                        continue  # Saltar al siguiente inmueble si el ID ya existe
                    print(f"Página {i} - data-element-id: {data_element_id}")
                    time.sleep(random.uniform(1, 3))  # Add a delay
                    inmueble_url = f"https://www.idealista.com/inmueble/{data_element_id}/"
                    try:
                        r = session.get(inmueble_url)
                        if r.status_code != 200:
                            print(f"Failed to retrieve the webpage. Status code: {r.status_code}")
                        else:
                            soup = BeautifulSoup(r.text, 'lxml')

                            # Extract the title
                            titulo = soup.find("span", {"class": "main-info__title-main"})
                            titulo_text = titulo.get_text(strip=True) if titulo else "N/A"

                           #  Extract the subtitle
                            # subtitle = soup.find("span", {"class": "main-info__title-minor"})
                            # subtitle_text = subtitle.get_text(strip=True) if subtitle else "N/A"

                            # Extract the price
                            price_info = soup.find("span", {"class": "info-data-price"})
                            price_text = price_info.get_text(strip=True) if price_info else "N/A"

                            # Extract the deposit if available
                            deposit = soup.find("span", {"class": "txt-deposit"}).get_text(strip=True)

                            # Extract meter price
                            meter_price = soup.find("section", {"class" : "flex-features__container"}).find("p", {"class" : "flex-feature squaredmeterprice"})
                            
                            # Extract community expenses
                            community = soup.find("section", {"class" : "flex-features__container"}).find("p", {"class" : "flex-feature-details"})

                            # Extract reference
                            reference_container = soup.find("div", {"class": "ad-reference-container"})
                            if reference_container:
                                reference = reference_container.find("p", {"class": "txt-ref"})
                                ref_num = reference.get_text(strip=True) if reference else "N/A"
                            else:
                                ref_num = "N/A"

                            actual_container = soup.find("div", {"id" : "stats"})
                            if actual_container:
                                actual = actual_container.find("p").get_text(strip=True)

                            # Extract anunciante
                            anun_container = soup.find("div", {"class": "professional-name"})
                            if anun_container:
                                anun = anun_container.find("div", {"class": "name"})
                                anunciante = anun.get_text(strip=True) if anun else "N/A"

                                nombre_anun = anun_container.find("span").get_text(strip=True) if anun else "N/A"


                            # Extract property details

                            feat = soup.find("div", {"class", "details-property"})
                            features = [f.text for f in feat.find_all("details-property_features")]

                            # Extract location list
                            location = soup.find("div", {"class": "headerMap"})
                            loc = [l.text for l in location.find_all("li")]

                            for l in loc:
                                street = loc[0],
                                neighborhood = loc[1],
                                district = loc[2],
                                city = loc[3],
                                area = loc[4]


                            # c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

                            # c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})

                            # mas = [caract.text.strip() for caract in c2.find_all("details-property_features")]

                            # c3 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

                            # basics = [caract.text for caract in c1.find_all("li")]

                            phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"

                            res_phone = session.get(phone_url)
                            telefono = 'N/A'
                            if res_phone.status_code != 200:
                                print('f')
                            else:
                                telefono_res = res_phone.json()
                                if ('phone1' in telefono_res and telefono_res['phone1'] and 'number' in telefono_res['phone1']):
                                    telefono = telefono_res['phone1']['number']


                            # Print extracted information
                            print(f"Title: {titulo_text}")
                            # print(f"Subtitle: {subtitle_text}")
                            print(f"Street: {street}")
                            print(f"Neighborhood: {neighborhood}")
                            print(f"District: {district}")
                            print(f"City: {city}")
                            print(f"Area: {area}")
                            print(f"Price: {price_text}")
                            print(f"Deposit: {deposit}")
                            print(f"Caracteristicas: {features}")
                            # print(basics)
                            # print(mas)
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
                            # "Subtítulo": subtitle_text,
                            "Precio": price_text,
                            "Fianza": deposit,
                            "Características": features,
                            # "Características Básicas": basics,
                            # "Más Características": mas,
                            "Referencia": ref_num,
                            "Anunciante": anunciante,
                            "Nombre Anunciante": nombre_anun,
                            "Última Actualización": actual,
                            "Teléfono": telefono
                        }, ignore_index=True)
                        df.to_excel(excel_file, index=False)
                        print(f"ID {data_element_id} guardado en el Excel.")
                        time.sleep(random.uniform(1, 3))  # Añadir un retraso
                    except Exception:
                        pass
    except Exception:
        pass
# Guardar el DataFrame actualizado en el archivo Excel
df.to_excel(excel_file, index=False)
print(f"Datos guardados en {excel_file}.")