import schedule
import time
from whatsapp_scraper import download_receipts, setup_driver
from ocr_processor import process_receipts
from classifier import classify_receipts
from storage import upload_to_drive

def run_automation():
    driver = setup_driver()
    download_receipts(driver, "Bank XYZ")
    driver.quit()

    extracted_data = process_receipts()
    classify_receipts(extracted_data)
    upload_to_drive()

schedule.every().day.at("12:00").do(run_automation)

while True:
    schedule.run_pending()
    time.sleep(60)