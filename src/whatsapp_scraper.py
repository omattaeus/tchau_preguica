from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

WHATSAPP_URL = "https://web.whatsapp.com/"
DOWNLOAD_PATH = "data/"

def setup_driver():
    """Initialize Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=selenium")  # Keeps session logged in
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(WHATSAPP_URL)
    return driver

def ensure_download_path():
    """Ensure that the download directory exists."""
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

def download_image(img_url, filename):
    """Download an image from a given URL."""
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"✅ Image saved: {filename}")
        else:
            print(f"⚠️ Failed to download image: {img_url}")
    except Exception as e:
        print(f"❌ Error downloading image: {e}")

def download_receipts(driver, contact_name):
    """Download receipt images from a specific contact's chat."""
    ensure_download_path()
    
    print(f"🔍 Searching for contact: {contact_name}")
    search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
    search_box.send_keys(contact_name)
    time.sleep(2)

    chat = driver.find_element(By.XPATH, f"//span[contains(text(), '{contact_name}')]")
    chat.click()
    time.sleep(2)

    images = driver.find_elements(By.TAG_NAME, "img")
    
    print(f"📥 Found {len(images)} images in {contact_name}'s chat.")
    
    for index, img in enumerate(images):
        img_url = img.get_attribute("src")
        if img_url and img_url.startswith("http"):
            filename = os.path.join(DOWNLOAD_PATH, f"{contact_name}_receipt_{index}.jpg")
            download_image(img_url, filename)

    print(f"✅ Finished downloading receipts from {contact_name}")

if __name__ == "__main__":
    driver = setup_driver()
    input("📱 Scan the QR code on WhatsApp Web and press Enter to continue...")
    download_receipts(driver, "Bank XYZ")
    driver.quit()