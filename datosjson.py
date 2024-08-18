import pandas as pd

# Lee el archivo Excel
df = pd.read_excel('inmuebles.xlsx')

# Convierte el DataFrame a JSON
df.to_json('datos.json', orient='records')
