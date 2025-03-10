import os

DOWNLOAD_PATH = os.path.join(os.getcwd(), "data")
ORGANIZED_PATH = os.path.join(os.getcwd(), "organized_receipts")

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "12345678@Ta",
    "database": "whatsapp_bot",
    "port": 3306
}

CHROME_DRIVER_PATH = r"./chromedriver.exe"