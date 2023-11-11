import sys
import logging
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import os

from io import StringIO

# Create a StringIO object to accumulate log messages
log_accumulator = StringIO()

logging.basicConfig(
    stream=log_accumulator,  # sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s ",
)

# URL de la página a monitorear
URL = "https://apps.ute.com.uy/LlamadosExternos/LstLlamados.aspx"

# Palabras clave (sin tildes y en mayúsculas)
KEYWORDS = [
    "TIC",
    "SISTEMAS",
    "INFORMATICA",
    "COMPUTACION",
    "TECNOLOGICO",
    "ESTUDIANTES",
    "AVANZADOS",
]


def obtener_contenido_pagina(url):
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        return response.text

    print("Error al acceder a la página:", response.status_code)
    return None


# Función para verificar si una publicación contiene palabras clave
def contiene_palabras_clave(publicacion, palabras_clave):
    for palabra in palabras_clave:
        if palabra in publicacion:
            return True
    return False


def format_publicacion(title, code):
    return f"""
Publicación encontrada: 
    * Titulo: {title}
    * Codigo: {code}
------------------------------
"""


def notify(text):
    flags = "--expire-time=7000 --icon='/usr/share/icons/Mint-Y/apps/64/caffeine.png' --category='Work'"
    os.system(f"notify-send {flags} 'UTE scrapper bot:\n\n' '{text}'")


def main():
    try:
        contenido_pagina = obtener_contenido_pagina(URL)
        if not contenido_pagina:
            return

        soup = BeautifulSoup(contenido_pagina, "html5lib")

        table = soup.find(id="Gridvigentes")
        publicaciones = table.find_all("tr")

        for publicacion in publicaciones:
            info = publicacion.find("td")
            if not info:
                continue
            info = info.find("span", class_="Fullview")
            if not info:
                continue
            info = info.text

            code, *title = info.strip().split("-")
            # Normalizacion del texto
            title = unidecode("".join(title).strip()).upper()

            if contiene_palabras_clave(title, KEYWORDS):
                logging.info(format_publicacion(title, code))

        logging.info("%s publicaciones analizadas", len(publicaciones))
        notification_body = log_accumulator.getvalue()
        notify(notification_body)

    except Exception:
        logging.error("While analyzing %s", publicacion)
        raise


if __name__ == "__main__":
    main()
