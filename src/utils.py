import requests
import os
from config import DOWNLOAD_PATH

def download_file(url, filename):
    """Baixa o arquivo (imagem ou PDF) da URL e salva no caminho especificado."""
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
        with open(filename, "wb") as file:
            file.write(response.content)