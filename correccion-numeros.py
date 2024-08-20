import pandas as pd
import requests
import time
import random

headers = {
    "authority": "www.idealista.com",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": "didomi_token=eyJ1c2VyX2lkIjoiMTkwYTY0NjAtNGU2Yy02NjAyLWIzYjctZjY5ZTMwODYyZWJmIiwiY3JlYXRlZCI6IjIwMjQtMDctMTJUMDk6Mjg6NDUuMDMwWiIsInVwZGF0ZWQiOiIyMDI0LTA3LTEyVDA5OjI4OjQ2LjI1MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpsaW5rZWRpbi1tYXJrZXRpbmctc29sdXRpb25zIiwiYzptaXhwYW5lbCIsImM6YWJ0YXN0eS1MTGtFQ0NqOCIsImM6aG90amFyIiwiYzpiZWFtZXItSDd0cjdIaXgiLCJjOnRlYWxpdW1jby1EVkRDZDhaUCIsImM6dGlrdG9rLUtaQVVRTFo5IiwiYzpnb29nbGVhbmEtNFRYbkppZ1IiLCJjOmlkZWFsaXN0YS1MenRCZXFFMyIsImM6aWRlYWxpc3RhLWZlUkVqZTJjIiwiYzpjb250ZW50c3F1YXJlIiwiYzptaWNyb3NvZnQiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInZlcnNpb24iOjIsImFjIjoiQ2hHQUVBRmtGQ0lBLkFBQUEifQ==; euconsent-v2=CQBpHQAQBpHQAAHABBENA8EsAP_gAAAAAAAAHXwBwAIAAqABaAFsAUgC8wHXgAAAFJQAYAAgpWUgAwABBSshABgACClY6ADAAEFKwkAGAAIKVgAA.f_wAAAAAAAAA; userUUID=443c4bb3-401a-4cb8-a32e-d3db477f4ce6; SESSION=e87100649bd6e940~a2bf2ff4-88a9-4272-95dd-d24838ce6713; utag_main__sn=6; utag_main_ses_id=1724068701892%3Bexp-session; utag_main__prevVtUrl=https%3A%2F%2Fwww.idealista.com%2F%3Bexp-1724072301945; utag_main__prevVtUrlReferrer=%3Bexp-1724072301945; utag_main__prevVtSource=Direct traffic%3Bexp-1724072301945; utag_main__prevVtCampaignName=organicWeb%3Bexp-1724072301945; utag_main__prevVtCampaignCode=%3Bexp-1724072301945; utag_main__prevVtCampaignLinkName=%3Bexp-1724072301945; utag_main__prevVtRecipientId=%3Bexp-1724072301945; utag_main__prevVtProvider=%3Bexp-1724072301945; utag_main__ss=0%3Bexp-session; contacta2bf2ff4-88a9-4272-95dd-d24838ce6713=\"{'maxNumberContactsAllow':10}\"; cookieSearch-1=\"/venta-viviendas/murcia-murcia/:1724068708141\"; _last_search=officialZone; senda2bf2ff4-88a9-4272-95dd-d24838ce6713=\"{}\"; utag_main__pn=4%3Bexp-session; utag_main__prevCompletePageName=005-idealista/portal > portal > detail > openGallery%3Bexp-1724072746057; utag_main__prevLevel2=005-idealista/portal%3Bexp-1724072746057; utag_main__se=10%3Bexp-session; utag_main__st=1724070947956%3Bexp-session; utag_main__prevCompleteClickName=005-idealista/portal > portal > closeGallery; datadome=hyjMqJcB2mt_N8dXXo3pGz~c8~Zl6nK5UhLIYlHdru4CL7NEr5jxCTaMawj4WZBrBZXE66lZsMWjoxJnO5~QCAewHiFgD1CwrAZdkJr7Lsni_yo1hFynlwl5aAtxKBQm",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-device-memory": "8",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.88\", \"Chromium\";v=\"127.0.6533.88\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": "\"\"",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}


session = requests.Session()
session.headers.update(headers)
# Leer el archivo Excel
df = pd.read_excel("inmuebles.xlsx")

# Definir la URL base para obtener el número de teléfono
url_base = "https://www.idealista.com/es/ajax/ads/{}/contact-phones"
print(url_base)
# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    if pd.isna(row['Teléfono']) or row['Teléfono'] == 'N/A':
        id_inmueble = int(row['ID Inmueble'])
        url = url_base.format(id_inmueble)   
        # Hacer una solicitud a la URL para obtener el número de teléfono
        print(url)
        response = session.get(url)
        time.sleep(random.uniform(1, 5))  # Añadir un retraso
        if response.status_code == 200:
            data = response.json()
            print (data)
            if 'phone1' in data and data['phone1'] and 'number' in data['phone1']:
                phone_number = data['phone1']['number']
                df.at[index, 'Teléfono'] = phone_number
                df.to_excel('numeros-bien.xlsx', index=False)
            else:
                print(f"No se encontró el número de teléfono para el ID de inmueble: {id_inmueble}")
        else:
            print(f"Error {response.status_code} al obtener los datos para el ID de inmueble: {id_inmueble}")
# Guardar el archivo Excel actualizado
df.to_excel('numeros-bien.xlsx', index=False)