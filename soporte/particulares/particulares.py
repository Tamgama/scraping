import pandas as pd
import numpy as np

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
df = pd.read_csv("../web_2/data/inmuebles.csv")

particulares = df[df["anunciante"] == "Particular"]
# Autenticar la aplicación
gauth = GoogleAuth()
# gauth.LocalWebserverAuth()  # Esto abrirá una ventana del navegador para autenticarse

gauth.LoadCredentialsFile("./particulares/credentials.json")  # Cargar token de autenticación
if not gauth.credentials or gauth.access_token_expired:
    print('Please, retreive credentials manually')
    # gauth.LocalWebserverAuth()  # Autenticarse si no hay token o está vencido
    # gauth.SaveCredentialsFile("credentials.json")  # Guardar token para la próxima vez
else:
    drive = GoogleDrive(gauth)
    # Subir el archivo Excel a Google Drive
    file_drive = drive.CreateFile({'title': './particulares/particulares.xlsx'})  # Cambia el título según desees
    file_drive.SetContentFile('particulares.xlsx')  # Archivo que queremos subir
    file_drive.Upload()