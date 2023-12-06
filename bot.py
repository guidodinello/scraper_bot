import logging
import os
from io import StringIO

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s ",
)

open("./log.txt", "w").close()  # clean old logs
file_log = logging.FileHandler("./log.txt", encoding="utf-8")
logging.getLogger().addHandler(file_log)

log_accumulator = StringIO()
log_handler = logging.StreamHandler(log_accumulator)
log_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(log_handler)


URL = "https://apps.ute.com.uy/LlamadosExternos/LstLlamados.aspx"

# should be in caps and shouldnt contain accents
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

    logging.error("Error al acceder a la página: %i", response.status_code)
    return None


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
            else:
                logging.debug(format_publicacion(title, code) + "[NO MATCH]\n")

        logging.info("%s publicaciones analizadas", len(publicaciones))
        notification_body = log_accumulator.getvalue()
        notify(notification_body)

    except Exception:
        logging.error("Error al analizar publicacion: %s", publicacion)
        raise


if __name__ == "__main__":
    main()
