import requests
import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd


excel_file = "inmuebles.xlsx"

# Leer el archivo Excel si existe, si no, crear un DataFrame vacío
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=[
        "ID Inmueble", "Título", "Subtítulo", "Precio", "Precio con Descuento", 
        "Características Básicas", "Más Características", "Referencia", 
        "Anunciante", "Nombre Anunciante", "Teléfono"
    ])

headers = {
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "max-age=0",
    "cookie":
    "userUUID=c7889446-ae97-4455-9845-6ca26cb28ea2; _pprv=eyJjb25zZW50Ijp7IjAiOnsibW9kZSI6Im9wdC1pbiJ9LCIxIjp7Im1vZGUiOiJvcHQtaW4ifSwiMiI6eyJtb2RlIjoib3B0LWluIn0sIjMiOnsibW9kZSI6Im9wdC1pbiJ9LCI0Ijp7Im1vZGUiOiJvcHQtaW4ifSwiNSI6eyJtb2RlIjoib3B0LWluIn0sIjYiOnsibW9kZSI6Im9wdC1pbiJ9LCI3Ijp7Im1vZGUiOiJvcHQtaW4ifX0sInB1cnBvc2VzIjpudWxsLCJfdCI6Im1ma3h5eXAzfGx6d2oxaGQzIn0%3D; _pcid=%7B%22browserId%22%3A%22lzwj1hczfkdi5ptf%22%2C%22_t%22%3A%22mfkxyyq9%7Clzwj1he9%22%7D; _pctx=%7Bu%7DN4IgrgzgpgThIC4B2YA2qA05owMoBcBDfSREQpAeyRCwgEt8oBJAE0RXSwH18yBbAGYBrAB4BPcQEcARgB9UALwDuAKwCMACygyQAXyA; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22D1wXAFBUdY3QkESsiDYK%22%7D; didomi_token=eyJ1c2VyX2lkIjoiMTkxNWE5NmUtZjVmYi02NWUxLThlY2EtMTYzMjcxNzAwYzI3IiwiY3JlYXRlZCI6IjIwMjQtMDgtMTZUMDk6NDg6NDYuODE1WiIsInVwZGF0ZWQiOiIyMDI0LTA4LTE2VDA5OjQ4OjUwLjU0NFoiLCJ2ZW5kb3JzIjp7ImRpc2FibGVkIjpbImdvb2dsZSIsImM6bGlua2VkaW4tbWFya2V0aW5nLXNvbHV0aW9ucyIsImM6bWl4cGFuZWwiLCJjOmFidGFzdHktTExrRUNDajgiLCJjOmhvdGphciIsImM6YmVhbWVyLUg3dHI3SGl4IiwiYzp0ZWFsaXVtY28tRFZEQ2Q4WlAiLCJjOnRpa3Rvay1LWkFVUUxaOSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzppZGVhbGlzdGEtTHp0QmVxRTMiLCJjOmlkZWFsaXN0YS1mZVJFamUyYyIsImM6Y29udGVudHNxdWFyZSIsImM6bWljcm9zb2Z0Il19LCJwdXJwb3NlcyI6eyJkaXNhYmxlZCI6WyJnZW9sb2NhdGlvbl9kYXRhIiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyJdfSwidmVyc2lvbiI6MiwiYWMiOiJBQUFBLkFBQUEifQ==; euconsent-v2=CQDceEAQDceEAAHABBENBBFgAAAAAAAAAAAAAAAAAACkoAMAAQUxKQAYAAgpiQgAwABBTEdABgACCmISADAAEFMQ.YAAAAAAAAAAA; _last_search=officialZone; smc=\"{}\"; galleryHasBeenBoosted=true; contact5b9f309c-f3ee-4bc3-ac61-abc676f62437=\"{'maxNumberContactsAllow':10}\"; send5b9f309c-f3ee-4bc3-ac61-abc676f62437=\"{}\"; SESSION=d7ab6b509870942b~5b9f309c-f3ee-4bc3-ac61-abc676f62437; utag_main__sn=2; utag_main_ses_id=1723825693684%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2Finmueble%2F105236581%2F%3Bexp-1723829293854; utag_main__prevVtUrlReferrer=https://www.idealista.com/venta-viviendas/murcia-murcia/%3Bexp-1723829293854; utag_main__prevVtSource=Portal sites%3Bexp-1723829293854; utag_main__prevVtCampaignName=organicWeb%3Bexp-1723829293854; utag_main__prevVtCampaignCode=%3Bexp-1723829293854; utag_main__prevVtCampaignLinkName=%3Bexp-1723829293854; utag_main__prevVtRecipientId=%3Bexp-1723829293854; utag_main__prevVtProvider=%3Bexp-1723829293854; utag_main__ss=0%3Bexp-session; dicbo_id=%7B%22dicbo_fetch%22%3A1723825695890%7D; utag_main__prevCompleteClickName=; cookieSearch-1=\"/venta-viviendas/murcia-murcia/:1723825777039\"; utag_main__pn=5%3Bexp-session; utag_main__se=11%3Bexp-session; utag_main__st=1723827579518%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > viewResults%3Bexp-1723829379535; utag_main__prevLevel2=005-idealista/portal%3Bexp-1723829379535; datadome=uD1DSM_QCag0XgpTMm_I8zAG81yninS6LLxrFWB8g0xBF1WU3~MJUDyjVGBAtojjt~d1GkypWFfoJsz7HyJfo3VlCbaFupShQ2DPFdHj7Z1XFIRhNmlRAPQyquRjfDuQ",
    "Priority": "u=0, i",
    "Referer": "https://www.idealista.com/venta-viviendas/murcia-murcia/",
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

base_url = "https://www.idealista.com/venta-viviendas/murcia-murcia/pagina-{}.htm"

# Definir el rango de páginas que quieres recorrer
num_paginas = 160  # Cambia este número según la cantidad de páginas que quieras recorrer
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
                            # meter_price = soup.find("section", {"class" : "flex-features__container"}).find("p", {"class" : "flex-feature squaredmeterprice"})
                            
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

                            c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

                            c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})

                            mas = [caract.text.strip() for caract in c2.find_all("li")]

                            c3 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-three"})

                            basics = [caract.text for caract in c1.find_all("li")]

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
                            print(f"Subtitle: {subtitle_text}")
                            print(f"Price: {price_text}")
                            print(f"Discounted Price: {discounted_price_text}")
                            # print(f"€/m²: {meter_price}")
                            print(basics)
                            print(mas)
                            print(ref_num)
                            print(anunciante)
                            print(nombre_anun)
                            print(telefono)

                            df = df._append({
                            "ID Inmueble": data_element_id,
                            "Tipo" : "venta",
                            "Título": titulo_text,
                            "Subtítulo": subtitle_text,
                            "Precio": price_text,
                            "Precio con Descuento": discounted_price_text,
                            # "Precio por m²": meter_price,
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
                    except Exception:
                        pass
    except Exception:
        pass
# Guardar el DataFrame actualizado en el archivo Excel
df.to_excel(excel_file, index=False)
print(f"Datos guardados en {excel_file}.")