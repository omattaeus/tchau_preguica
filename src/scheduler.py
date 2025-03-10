import schedule
import time

def run_automation():
    driver = setup_driver()
    download_receipts(driver, "Bank XYZ")
    driver.quit()

    extracted_data = process_receipts()
    classify_receipts(extracted_data)
    upload_to_drive(extracted_data)

schedule.every().day.at("10:00").do(run_automation)

while True:
    schedule.run_pending()
    time.sleep(1)