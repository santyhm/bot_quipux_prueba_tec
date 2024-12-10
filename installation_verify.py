from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import requests
import platform
import zipfile

def get_latest_chromedriver_version():
    url = 'https://googlechromelabs.github.io/chrome-for-testing/#stable'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    version = soup.find('div', class_='table-wrapper summary').find('code').text
    return version

def download_chromedriver(version):
    os_type = get_os_type()
    driver_filename = f'chromedriver_{os_type}.zip'

    if os_type == 'mac':
        base_url = 'https://storage.googleapis.com/chrome-for-testing-public/{}/mac-x64/chromedriver-mac-x64.zip'
    elif os_type == 'windows':
        base_url = 'https://storage.googleapis.com/chrome-for-testing-public/{}/win64/chromedriver-win64.zip'
    else:
        # print('Sistema operativo no compatible')
        return

    driver_url = base_url.format(version)
    response = requests.get(driver_url)
    with open(f'chromedriver_{os_type}.zip', 'wb') as f:
        f.write(response.content)

    # Extraer el archivo ZIP
    extract_dir = f'chromedriver_{os_type}'
    with zipfile.ZipFile(driver_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(driver_filename)

def get_chrome_version():
    if platform.system() == 'Windows':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return version
    elif platform.system() == 'Darwin':
        import subprocess
        process = subprocess.Popen(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
        version = process.communicate()[0].decode('UTF-8').replace('Google Chrome ', '').strip()
        return version
    else:
        return None
    
def get_installed_chromedriver_version():
    try:
        os_type = get_os_type()
        if os_type == 'mac':
            chromedriver_path = f"chromedriver_{os_type}/chromedriver-mac-x64/chromedriver"
        elif os_type == 'windows':
            chromedriver_path = f"chromedriver_{os_type}/chromedriver-win64/chromedriver.exe"
        else:
            return None
        
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)
        version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        driver.quit()
        return version
    except Exception as e:
        # print(f"Error al obtener la versión de ChromeDriver instalado: {e}")
        return None

def verify_version_driver():
    chrome_version = get_chrome_version()
    # print('Versión actual de Chrome:', chrome_version)

    installed_chromedriver_version = get_installed_chromedriver_version()
    # print('Versión de ChromeDriver instalado:', installed_chromedriver_version)

    if chrome_version:
        if installed_chromedriver_version:
            if chrome_version == installed_chromedriver_version:
                pass
                # print('El ChromeDriver está actualizado')
            else:
                # print('Descargando la versión actualizada de ChromeDriver...')
                download_chromedriver(chrome_version)
        else:
            # print('No se encontró una versión instalada de ChromeDriver. Descargando...')
            download_chromedriver(chrome_version)
    else:
        pass
        # print('No se pudo verificar las versiones')

def get_os_type():
    system = platform.system().lower()
    if system == 'darwin':
        return 'mac'
    elif system == 'windows':
        return 'windows'
    else:
        # print('Sistema operativo no compatible')
        return None
    
