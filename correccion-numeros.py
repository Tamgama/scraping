import pandas as pd
import requests
from tqdm import tqdm

# Leer el archivo Excel
df = pd.read_excel("inmuebles.xlsx")

# Definir la URL base para obtener el número de teléfono
url_base = "https://www.idealista.com/es/ajax/ads/{}/contact-phones"

# Iterar sobre las filas del DataFrame
for index, row in tqdm(df.iterrows()):
    if pd.isna(row['Teléfono']) or row['Teléfono'] == 'N/A':
        id_inmueble = row['ID Inmueble']
        url = url_base.format(id_inmueble)
        
        # Hacer una solicitud a la URL para obtener el número de teléfono
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'number' in data:
                phone_number = data['number']
                df.at[index, 'Teléfono'] = phone_number
            else:
                print(f"No se encontró el número de teléfono para el ID de inmueble: {id_inmueble}")
        else:
            print(f"Error {response.status_code} al obtener los datos para el ID de inmueble: {id_inmueble}")
# Guardar el archivo Excel actualizado
df.to_excel('numeros-bien.xlsx', index=False)