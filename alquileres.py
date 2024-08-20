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
        "Ciudad", "Área", "Precio", "Fianza", "Precio/m²" "Características", "Referencia", 
        "Anunciante", "Nombre Anunciante", "Última Actualización", "Teléfono"
    ])

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "no-store,max-age=0",
    "cookie":
        "_pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1ma3h5eXAzfGx6d2oxaGQzIn0%3D; _pcid=%7B%22browserId%22%3A%22lzwj1hczfkdi5ptf%22%2C%22_t%22%3A%22mfkxyyq9%7Clzwj1he9%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAGYBrAB4BPcQEcARgB9UALwDuAKwCMACygyQAXyA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22D1wXAFBUdY3QkESsiDYK%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxNWE5NmUtZjVmYi02NWUxLThlY2EtMTYzMjcxNzAwYzI3IiwiY3JlYXRlZCI6IjIwMjQtMDgtMTZUMDk6NDg6NDYuODE1WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTE2VDA5OjQ4OjUwLjU0NFoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQDceEAQDceEAAHABBENBBFgAAAAAAAAAAAAAAAAAACkoAMAAQUxKQAYAAgpiQgAwABBTEdABgACCmISADAAEFMQ.YAAAAAAAAAAA; smc=\"{}\"; galleryHasBeenBoosted=true; utag_main__prevCompleteClickName=; userUUID=f2240d16-a373-42be-b98e-114f09a0d46d; contactb78172ad-8c7d-48da-abf0-5f5f07183ea7=\"{'maxNumberContactsAllow':10}\"; SESSION=eea26d055b230b2a~b78172ad-8c7d-48da-abf0-5f5f07183ea7; utag_main__sn=3; utag_main_ses_id=1724148993832%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Fventa-viviendas%2Fmurcia-murcia%2F%3Bexp-1724152593884; utag_main__prevVtUrlReferrer=%3Bexp-1724152593884; utag_main__prevVtSource=Direct traffic%3Bexp-1724152593884; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724152593884; utag_main__prevVtCampaignCode=%3Bexp-1724152593884; utag_main__prevVtCampaignLinkName=%3Bexp-1724152593884; utag_main__prevVtRecipientId=%3Bexp-1724152593884; utag_main__prevVtProvider=%3Bexp-1724152593884; utag_main__ss=0%3Bexp-session; _last_search=officialZone; dicbo_id=%7B%22dicbo_fetch%22%3A1724148994683%7D; cookieSearch-1=\"/alquiler-viviendas/murcia-murcia/:1724149001961\"; discrentingbdmi=true; sendb78172ad-8c7d-48da-abf0-5f5f07183ea7=\"{}\"; utag_main__pn=3%3Bexp-session; utag_main__se=5%3Bexp-session; utag_main__st=1724150921225%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewAdDetail%3Bexp-1724152721239; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724152721239; datadome=IrK6HiC7XTPPXxAk9L~wteOvPyB2QMlM_FN1j6tMHXtc4LvSCJtV7tIlgh0tHG3G7aAGcyS8L0S614e9~PjrCOE2Vbplw_EN_GJJr7AVf14pCdecAT3BAkzBSU~18rBr",    "Priority": "u=0, i",
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
# Bucle para recorrer cada página
for i in range(1, num_paginas + 1):
    # Generar la URL de la página actual
    url = base_url.format(i)

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

                    actual_container = soup.find("div", {"id" : "stats"})
                    if actual_container:
                        actual = actual_container.find("p").get_text(strip=True)

                    # Extract anunciante
                    anun_container = soup.find("div", {"class": "professional-name"})
                    if anun_container:
                        anun = anun_container.find("div", {"class": "name"})
                        anunciante = anun.get_text(strip=True) if anun else "N/A"

                        nombre_anun = anun_container.find("span").get_text(strip=True) if anun else "N/A"



                    # Extract location list
                    location = soup.find("div", {"id": "headerMap"})
                    loc = [lo.text for lo in location.find_all("li")]

                    for lo in loc:
                        street = loc[0],
                        neighborhood = loc[1],
                        district = loc[2],
                        city = loc[3],
                        area = loc[4]

                    # Extract property details

                    # feat = soup.find("div", {"class", "details-property"})
                    # features = [f.text for f in feat.find_all("details-property_features")]

                    c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

                    c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})

                    mas = [caract.text.strip() for caract in c2.find_all("details-property_features")]

                    c3 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

                    basics = [caract.text for caract in c1.find_all("li")]

                    phone_url = f"https://www.idealista.com/es/ajax/ads/{data_element_id}/contact-phones"

                    res_phone = session.get(phone_url)
                    telefono = "N/A"
                    if res_phone.status_code != 200:
                        print('f')
                    else:
                        telefono_res = res_phone.json()
                        if ('phone1' in telefono_res and telefono_res['phone1'] and 'number' in telefono_res['phone1']):
                            telefono = telefono_res['phone1']['number']


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
                    # print(basics)
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
                    # "Subtítulo": subtitle_text,
                    "Precio": price_text,
                    "Fianza": deposit,
                    # "Características": features,
                    "Características Básicas": basics,
                    "Más Características": mas,
                    "Referencia": ref_num,
                    "Anunciante": anunciante,
                    "Nombre Anunciante": nombre_anun,
                    "Última Actualización": actual,
                    "Teléfono": telefono
                }, ignore_index=True)
                df.to_excel(excel_file, index=False)
                print(f"ID {data_element_id} guardado en el Excel.")
                time.sleep(random.uniform(1, 3))  # Añadir un retraso

# Guardar el DataFrame actualizado en el archivo Excel
df.to_excel(excel_file, index=False)
print(f"Datos guardados en {excel_file}.")