import os
import shutil
from datetime import datetime

DATA_PATH = "data/"
ORGANIZED_PATH = "organized_receipts/"

def classify_receipts(receipts):
    """Classify receipts based on extracted data."""
    for receipt in receipts:
        year = receipt["date"].split("/")[-1]
        month = receipt["date"].split("/")[1]
        category = receipt["recipient"]

        folder_path = os.path.join(ORGANIZED_PATH, year, month, category)
        os.makedirs(folder_path, exist_ok=True)

        for file in os.listdir(DATA_PATH):
            shutil.move(os.path.join(DATA_PATH, file), folder_path)

if __name__ == "__main__":
    extracted_data = process_receipts()
    classify_receipts(extracted_data)