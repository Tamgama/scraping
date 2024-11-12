#!/bin/bash

# Cargar la llave SSH
eval "$(ssh-agent -s)"
ssh-add /root/.ssh/equalityon@gmail.com

# Navegar al directorio de scraping
cd /root/scraping || exit

# Hacer git pull
git pull origin main

# Activar el entorno virtual
source .venv/bin/activate

# Ejecutar el script de Python en el directorio de soporte
cd ./soporte || exit
python3 proceso_completo.py

# Volver al directorio de scraping
cd /root/scraping || exit

# Añadir cambios, hacer commit y push
git add .
commit_message="[UPD] data_updated: $(date +'%Y-%m-%d %H:%M:%S')"
git commit -m "$commit_message"
git push origin main

# Detener el agente SSH
ssh-agent -k
