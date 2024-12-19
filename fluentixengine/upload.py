import os
import subprocess
import sys
from colorama import Fore, Style, init
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.service_account import Credentials
except:
    with open(os.path.dirname(os.path.abspath(__file__)) + '/fluentix.data', 'w') as f:
        f.write("0")

import re
from .get import do

init(autoreset=True)

SCOPES = ['https://www.googleapis.com/auth/drive']

UPLOAD_JSON = os.path.dirname(os.path.abspath(__file__)) + "/file.json"

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def is_package_installed():
    """Check if a package is already installed."""
    try:
        with open(os.path.dirname(os.path.abspath(__file__)) + '/fluentix.data', 'r') as f:
            return f.read() == "1"
    except FileNotFoundError:
        return False

def authenticate():
    """Authenticate the service account and return the Drive API service."""
    # Load the credentials from the JSON file
    with open(UPLOAD_JSON, 'r') as json_file:
        creds = Credentials.from_service_account_file(json_file.name, scopes=SCOPES)
        
    return build('drive', 'v3', credentials=creds)

def upload_file(file_path):
    """Upload a file to Google Drive and return the shareable link."""
    try:
        # Authenticate and get the Drive API service
        service = authenticate()

        # File metadata for the upload
        file_metadata = {'name': os.path.basename(file_path)}

        # Media upload object
        media = MediaFileUpload(file_path, resumable=True)

        # Upload the file
        print(f"{Fore.WHITE}[INFO] Uploading {file_path} to Fluentix's lib...")
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')

        # Set permissions to make the file publicly accessible
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        # Generate the shareable link
        link = f"https://drive.google.com/uc?id={file_id}&export=download"

        return link
    except Exception as e:
        print(f"{Fore.RED}[ERROR] An error occurred: {e}")
        return None

def delete(file_link):
    """Delete a file from Google Drive using its download link."""
    try:
        # Extract file ID from the link
        file_id_match = re.search(r'id=([^&]+)', file_link)
        if not file_id_match:
            print(f"{Fore.RED}[ERROR] Invalid file link provided.")
            return

        file_id = file_id_match.group(1)

        # Authenticate and get the Drive API service
        service = authenticate()

        # Delete the file
        service.files().delete(fileId=file_id).execute()
        print(f"{Fore.GREEN}[SUCCESS] File with ID {file_id} has been deleted.")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] An error occurred while deleting the file: {e}")

def main(path):
    """Main function to handle package installation and file upload."""
    packages = [
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client'
    ]

    if is_package_installed() and do():
        return upload_file(path)

    sys.stdout.write(f"{Fore.WHITE}[INFO] In order to use command 'upload/manage-package', you would have to install an additional of approximately 19 MBs for the 'Upload extension'.\n")

    user_input = input(f"{Fore.WHITE}[INPUT] Would you like to continue installing the missing packages (y/n)? ").strip().lower()

    if user_input == 'y':
        for package in packages:
            try:
                print(f"{Fore.WHITE}Installing {package}...")
                install(package)
                print(f"{Fore.GREEN}[SUCCESS] Successfully installed {package}")

                with open(os.path.dirname(os.path.abspath(__file__)) + '/fluentix.data', 'w') as f:
                    f.write("1")

                return upload_file(path)

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to install {package}. Error: {e}")
    else:
        print(f"{Fore.RED}[ABORT] Installation aborted.")