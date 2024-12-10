from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from installation_verify import *
import pandas as pd
import time
#Comienza la automatización

session_id = None
def open_url(url):
    global session_id
    global driver
    verify_version_driver()
    os_type = get_os_type()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    if os_type == 'mac':
        service = Service(executable_path=f"chromedriver_{os_type}/chromedriver-mac-x64/chromedriver")
    if os_type == 'windows':
        service = Service(executable_path=f"chromedriver_{os_type}/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    session_id = driver.session_id
    driver.get(url)
    return driver

def read_excel(route_excel):
    df = pd.read_excel(route_excel)
    return df.to_dict(orient='records')

def paste_form(driver, data):
    for field, value in data.items():
        try:
            # Cambia el selector según los atributos de tu formulario
            input_element = driver.find_element(By.ID, field)
            input_element.clear()
            input_element.send_keys(str(value))
        except Exception as e:
            print(f"Error con el campo '{field}': {e}")

    try:
        # boton_enviar = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-submit') or text()=' Enviar ']")
        btn_send = driver.find_element(By.XPATH, "//form//button")
        btn_send.click()
        # time.sleep(3)
    except Exception as e:
        print(f"Error al enviar el formulario: {e}")

