import pandas as pd
import numpy as np

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# SALVA: 
# Como proceso completo se ejecuta desde la carpeta de soporte,
# web_2 solo necesita un ../ porque se hace la referencia desde el programa
# proceso completo y no desde particulaes
df = pd.read_csv("../web_2/data/inmuebles.csv")

particulares = df[df["anunciante"] == "Particular"]
# Autenticar la aplicación
gauth = GoogleAuth()
# SALVA: 
# Esto, como es un proceso automático bloquea la script.
# Si no tiene los credenciales hay que meterlos a mano, parecido a la cookie

# gauth.LocalWebserverAuth()  # Esto abrirá una ventana del navegador para autenticarse

# SALVA: 
# Se cambia la carpeta de credentials.json porque se está ejecutando
# desde proceso_completo.py, además hay que copiar el client_secrets.json
# a soporte porque los de Google son un poco máquinas y no te dejan elegir donde está
# el fichero
gauth.LoadCredentialsFile("./particulares/credentials.json")  # Cargar token de autenticación
if not gauth.credentials or gauth.access_token_expired:
    print('Please, retreive credentials manually')
    # SALVA: 
    # Lo mismo que antes, esto bloquea

    # gauth.LocalWebserverAuth()  # Autenticarse si no hay token o está vencido
    # gauth.SaveCredentialsFile("./particulares/credentials.json")  # Guardar token para la próxima vez
else:
    drive = GoogleDrive(gauth)
    # Subir el archivo Excel a Google Drive
    file_drive = drive.CreateFile({'title': 'particulares.xlsx'})  # Cambia el título según desees
    # SALVA: 
    # Aquí cambia también la ruta del fichero particulares, recordemos que estamos en la carpeta
    # soporte ejecutando proceso_completo.py
    file_drive.SetContentFile('./particulares/particulares.xlsx')  # Archivo que queremos subir
    file_drive.Upload()