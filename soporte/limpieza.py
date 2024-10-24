import pandas as pd
import numpy as np
import re

# Configurar las opciones de visualización de pandas para mostrar todas las columnas y sin límite de ancho
pd.set_option("display.max_columns", None)
pd.set_option('display.max_colwidth', None)

# Cargar los datasets de ventas y alquileres
ventas = pd.read_csv("../src/ventas.csv")
alquileres = pd.read_csv("../src/alquileres.csv")

# # Eliminar columnas innecesarias del dataframe de alquileres
# alquileres.drop(['Metros_construidos', 'Metros_utilesBaños'], axis=1, inplace=True)

# # Renombrar columnas en el dataframe de ventas para asegurar consistencia en los nombres
# ventas.rename(columns={"Precio/m²": "Precio_por_metro"}, inplace=True)

# Definir el orden de las columnas deseado para ambos dataframes
ventas_order = [
    "id_inmueble", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion",
    "precio", "precio_metro", "caracteristicas", "habitaciones", "m_construidos", "m_utiles",
    "baños", "referencia", "anunciante", "nombre", "ultima_atualizacion", "tlf", "URL", "fecha"
]
alquileres_order = [
    "id_inmueble", "tipo", "titulo", "calle", "barrio", "zona", "ciudad", "localizacion",
    "precio", "precio_metro", "caracteristicas", "habitaciones", "m_construidos", "m_utiles",
    "baños", "referencia", "anunciante", "nombre", "ultima_atualizacion", "tlf", "URL", "fecha"
]

# Reorganizar las columnas en los dataframes según el orden definido
ventas = ventas.reindex(columns=ventas_order)
alquileres = alquileres.reindex(columns=alquileres_order)

# Combinar los dataframes de ventas y alquileres en un único dataframe, eliminando columnas no necesarias
df = pd.concat([alquileres, ventas], axis=0, ignore_index=True)
# df.drop(['Fianza', 'Comunidad'], axis=1, inplace=True)

# Normalizar nombres de columnas a minúsculas y reemplazar espacios con guiones bajos
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Renombrar columnas específicas para consistencia
df.rename(columns={
    'id_inmueble': 'id',
    # 'título': 'titulo',
    # 'área': 'area',
    # 'características': 'caracteristicas',
    # 'teléfono': 'tlf',
    # 'última_actualización': 'ultima_actualizacion'
}, inplace=True)

# Limpiar el texto en ciertas columnas eliminando saltos de línea y palabras innecesarias
cols_to_clean = ['calle', 'ciudad', 'localizacion', 'precio', 'precio_metro']
for col in cols_to_clean:
    df[col] = df[col].str.replace('\n', '', regex=False)
    df[col] = df[col].str.replace('€/mes', '', regex=False)
    df[col] = df[col].str.replace('€/m²', '', regex=False)

df['titulo'] = df['titulo'].str.replace('Alquiler de ', '', regex=False)
df['zona'] = df['zona'].str.replace('Área de ', '', regex=False)
df['barrio'] = df['barrio'].str.replace('Barrio ', '', regex=False)
# df['distrito'] = df['distrito'].str.replace('Distrito ', '', regex=False)


# Convertir el número de teléfono a formato numérico, manejando errores y rellenando valores nulos con 0
df['tlf'] = pd.to_numeric(df['tlf'], errors='coerce').fillna(0).astype(int)

# Inicializar columnas adicionales para almacenar las características extraídas
columnas_extra = [
    'superficie', 'superficie_util', 'habitaciones', 'baños', 'terraza', 'garaje', 'estado',
    'armarios', 'trastero', 'orientacion', 'amueblado', 'calefaccion', 'planta', 'ascensor',
    'construccion', 'movilidad_reducida', 'exterior_interior'
]
for col in columnas_extra:
    df[col] = None

# Definir patrones regex para extraer características de la columna 'caracteristicas'
patterns = {
    'superficie': re.compile(r'(\d+)\s*m² construidos', re.IGNORECASE),
    # 'superficie_util': re.compile(r'(\d+)\s*m² útiles', re.IGNORECASE),
    'habitaciones': re.compile(r'(\d+)\s*habitaciones?', re.IGNORECASE),
    'baños': re.compile(r'(\d+)\s*baños?', re.IGNORECASE),
    'terraza': re.compile(r'(Terraza|Balcón)', re.IGNORECASE),
    'garaje': re.compile(r'(Plaza de garaje)', re.IGNORECASE),
    'estado': re.compile(r'(Segunda mano\b.*buen estado)', re.IGNORECASE),
    'armarios': re.compile(r'(Armarios empotrados)', re.IGNORECASE),
    'trastero': re.compile(r'(Trastero)', re.IGNORECASE),
    'orientacion': re.compile(r'Orientación\s([\w\s,]+)', re.IGNORECASE),
    'amueblado': re.compile(r'(Amueblado y cocina equipada|Cocina sin equipar y casa sin amueblar)', re.IGNORECASE),
    'calefaccion': re.compile(r'Calefacción (central|individual|No disponible calefaccion)', re.IGNORECASE),
    'planta': re.compile(r'Planta\s(\d+)(?:ª|\s)?(exterior|interior)', re.IGNORECASE),
    'ascensor': re.compile(r'(Con ascensor|Sin ascensor)', re.IGNORECASE),
    'construccion': re.compile(r'Construido en (\d{4})', re.IGNORECASE),
    'movilidad_reducida': re.compile(r'(Solo acceso exterior adaptado para personas con movilidad reducida)', re.IGNORECASE)
}

def extract_data(row, patterns):
    data = {col: np.nan for col in patterns.keys()}
    data['exterior_interior'] = np.nan  # Columna adicional para almacenar si es exterior/interior
    if pd.isna(row):  # Si el valor es nulo, devolver diccionario vacío
        return data
    for key, pattern in patterns.items():
        match = pattern.search(row)
        if match:
            if key == 'planta':
                data['planta'] = match.group(1)
                data['exterior_interior'] = match.group(2)
            elif key == 'ascensor':
                data[key] = 'Sí' if 'Con' in match.group(0) else 'No'
            elif key == 'amueblado':
                data[key] = 'Amueblado' if 'Amueblado' in match.group(0) else 'No amueblado'
            elif key == 'calefaccion':
                data[key] = match.group(1) if match.group(1) != 'No disponible calefaccion' else 'No disponible'
            elif key == 'orientacion':
                data[key] = match.group(1)
            else:
                data[key] = match.group(1)
    return data

# Aplicar la función de extracción de datos a la columna 'caracteristicas'
df_extracted = df['caracteristicas'].apply(lambda row: extract_data(row, patterns))

# Convertir la serie de diccionarios a un DataFrame y asegurarse de que los índices coincidan
df_extracted = pd.DataFrame(list(df_extracted), index=df.index)

# Actualizar el DataFrame original con las características extraídas
df.update(df_extracted)

# Guardar el DataFrame resultante en un archivo CSV
df.sort_values(by="fecha", ascending=False, inplace=True)
df.to_csv('../web_2/data/inmuebles.csv', index=False)
