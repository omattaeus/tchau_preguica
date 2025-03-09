from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

ORGANIZED_PATH = "organized_receipts/"

def authenticate():
    """Authenticate with Google Drive."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def upload_to_drive():
    """Upload receipts to Google Drive."""
    drive = authenticate()
    
    for root, dirs, files in os.walk(ORGANIZED_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            gfile = drive.CreateFile({'title': file})
            gfile.SetContentFile(file_path)
            gfile.Upload()
    
    print("All receipts uploaded to Google Drive.")

if __name__ == "__main__":
    upload_to_drive()