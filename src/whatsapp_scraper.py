# main.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.google_drive_uploader import add_contact, save_receipt, get_contact
from src.ocr_processor import extract_receipt_data
from src.utils import download_image

def setup_driver():
    """Configura o WebDriver para o WhatsApp Web."""
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=selenium")  # Mantém o login ativo entre sessões
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)  # Aguarda o login no WhatsApp Web
    return driver

def monitor_messages(driver):
    """Monitora as mensagens recebidas no WhatsApp Web."""
    print("📡 Bot ativo! Monitorando mensagens...")
    while True:
        chats = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'unread')]")
        for chat in chats:
            chat.click()
            time.sleep(2)

            contact_name = driver.find_element(By.XPATH, "//header//span").text
            contact_number = contact_name.replace(" ", "").replace("+", "").strip()
            contact_id = get_contact(contact_number)

            if not contact_id:
                add_contact(contact_number, contact_name)
                send_message(driver, contact_name, "✅ Você foi registrado! Envie um comprovante para salvá-lo automaticamente.")
                contact_id = get_contact(contact_number)

            attachments = driver.find_elements(By.TAG_NAME, "img") + driver.find_elements(By.TAG_NAME, "a")
            for index, attachment in enumerate(attachments):
                file_url = attachment.get_attribute("href") or attachment.get_attribute("src")
                if file_url and "blob:" not in file_url:
                    filename = f"./downloads/{contact_number}_{index}"
                    download_file(file_url, filename)

                    if detect_receipt(filename):
                        receipt_data = detect_receipt(filename)
                        if receipt_data:
                            save_receipt(contact_id, filename, receipt_data["amount"], receipt_data["date"])
                            send_message(driver, contact_name, "📥 Comprovante salvo com sucesso!")

        time.sleep(5)

    """Monitora as mensagens recebidas no WhatsApp Web."""
    print("📡 Bot ativo! Monitorando mensagens...")
    while True:
        chats = driver.find_elements(By.XPATH, "//div[contains(@aria-label, 'unread')]")
        for chat in chats:
            chat.click()
            time.sleep(2)

            contact_name = driver.find_element(By.XPATH, "//header//span").text
            contact_number = contact_name.replace(" ", "").replace("+", "").strip()
            contact_id = get_contact(contact_number)

            if not contact_id:
                add_contact(contact_number, contact_name)
                send_message(driver, contact_name, "✅ Você foi registrado! Envie um comprovante para salvá-lo automaticamente.")
                contact_id = get_contact(contact_number)

            # Processa as imagens recebidas
            images = driver.find_elements(By.TAG_NAME, "img")
            for index, img in enumerate(images):
                img_url = img.get_attribute("src")
                if img_url and "blob:" not in img_url:
                    filename = f"./downloads/{contact_number}_{index}.jpg"
                    download_image(img_url, filename)

                    if detect_receipt(filename):
                        receipt_data = extract_receipt_data(filename)
                        save_receipt(contact_id, filename, receipt_data["amount"], receipt_data["date"])
                        send_message(driver, contact_name, "📥 Comprovante salvo com sucesso!")

        time.sleep(5)

def send_message(driver, contact, message):
    """Envia uma mensagem para um contato no WhatsApp."""
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.send_keys(contact)
    time.sleep(2)

    chat = driver.find_element(By.XPATH, f"//span[contains(text(), '{contact}')]")
    chat.click()
    time.sleep(2)

    input_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)
    time.sleep(2)

def detect_receipt(image_path):
    """Detecta se a imagem é um comprovante."""
    return True

if __name__ == "__main__":
    driver = setup_driver()
    monitor_messages(driver)
    driver.quit()
