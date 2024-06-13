import os
import subprocess

# Check if Tesseract is installed
def is_tesseract_installed():
    try:
        subprocess.run(['tesseract', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Download and install Tesseract if not installed
def setup_tesseract():
    if not is_tesseract_installed():
        print("Tesseract not found. Installing Tesseract...")
        # Download and install Tesseract for Ubuntu
        os.system('sudo apt update && sudo apt install -y tesseract-ocr')
