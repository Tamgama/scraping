import requests
import time
import random
import json
from bs4 import BeautifulSoup
from itertools import cycle



id_inmueble = "105236581"

url = f"https://www.idealista.com/inmueble/{id_inmueble}/"


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9",
    "Cache-Control": "max-age=0",
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

r = session.get(url)
time.sleep(random.uniform(1, 3))  # Add a delay


"""h1 -> class="main-info__title-main"
   -> span -- txt

span -> class="main-info__title-block"
     -> span -- txt

div -> class="info-data"
    -> span --> class="info-data-price"
            --> span -- txt
    -> span --> class="pricedown"
            --> span -- txt

section -> id="details"
    div --> class="details-property"
            details 1 --> caracteristicas básicas
            details 2 --> h2 = key : div = value
                                    --> iteracion li"""



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

    # Extract reference
    reference_container = soup.find("div", {"class": "ad-reference-container"})
    if reference_container:
        reference = reference_container.find("p", {"class": "txt-ref"})
        ref_num = reference.get_text(strip=True) if reference else "N/A"
    else:
        ref_num = "N/A"

    # Extract anunciante
    anun_container = soup.find("div", {"class": "professional-name"})
    if anun_container:
        anun = anun_container.find("div", {"class": "name"})
        anunciante = anun.get_text(strip=True) if anun else "N/A"


    # Extract property details

    c1 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-one"})

    c2 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-two"})

    mas = [caract.text.strip() for caract in c2.find_all("li")]

    c3 = soup.find("section", {"id": "details"}).find("div", {"class": "details-property-feature-three"})

    basics = [caract.text for caract in c1.find_all("li")]

    # Print extracted information
    print(f"Title: {titulo_text}")
    print(f"Subtitle: {subtitle_text}")
    print(f"Price: {price_text}")
    print(f"Discounted Price: {discounted_price_text}")
    print(basics)
    print(mas)
    print(ref_num)
    print(anunciante)

    # If ref_num is valid, request phone number
    # if ref_num != "N/A":
    #     phone_url = f"https://www.idealista.com/es/ajax/ads/{ref_num}/contact-phones"
    #     phone_response = session.get(phone_url)
    #     time.sleep(random.uniform(1, 3))  # Add a delay

    #     if phone_response.status_code == 200:
    #         phone_data = phone_response.json()
    #         if 'phones' in phone_data:
    #             phone_number = phone_data['phones']
    #             print(f"Phone Number: {phone_number}")
    #         else:
    #             print("Phone number not found in the response.")
    #     else:
    #         print(f"Failed to retrieve the phone number. Status code: {phone_response.status_code}")

phone_url = f"https://www.idealista.com/es/ajax/ads/{id_inmueble}/contact-phones"

res_phone = requests.get(phone_url)

sopa = BeautifulSoup(res_phone.content, "html.parser")
print(sopa.prettify())

numero = sopa.find("number")
print(numero)