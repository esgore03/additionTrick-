from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time




load_dotenv()
browser = os.getenv("BROWSER")
browser_path = os.getenv("BROWSER_PATH")
webdriver_path = os.getenv("WEBDRIVER_PATH")
username = os.getenv("SIRA_USERNAME")
password = os.getenv("SIRA_PASSWORD")
course_code = os.getenv("COURSE_CODE")
group_number = os.getenv("GROUP_NUMBER")

if not all([browser, browser_path, webdriver_path, username, password, course_code, group_number]):
    raise ValueError("Error: All required environment variables must be set")

chrome_options = Options()
if browser == "BRAVE":
    chrome_options.binary_location = browser_path
        
while True:
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://sira1.univalle.edu.co/sra")


    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()
    except:
        print("No alert found")

    try:
        user_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "usu_login_aut"))
        )
        password_input = driver.find_element(By.NAME, "usu_password_aut")

        user_input.send_keys(username)
        password_input.send_keys(password)
        password_input.submit()
    except:
        print("Error: login fields not found")

    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present()).accept()
    except:
        print("No alert found")

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='image'][title='Matrícula Académica']"))
    )
    element.click()

    close_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "icono_cerrar"))
    )
    close_icon.click()

    try:
        course_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "asm_asi_codigo"))
        )
        group_input = driver.find_element(By.NAME, "asm_grupo")
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[title='Haciendo clic en este botón ud. podrá Adicionar la asignatura deseada']"))
        )
        course_input.send_keys(course_code)
        group_input.send_keys(group_number)
        add_button.click()
    except:
        print("Error: Fields for course code or group number not found")

    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "botonAceptar"))
    )
    accept_button.click()

    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert_text = alert.text

        if "No hay cupo para la asignatura" in alert_text:
            alert.accept()
            print("No hay cupo, reintentando todo el proceso...")
            driver.quit()  # Cierra el navegador antes de reiniciar

            continue  # Reinicia el proceso desde el principio
        else:
            alert.accept()
            WebDriverWait(driver, 5).until(EC.alert_is_present()).accept()
    except:
        print("No alert found")

    break  # Si se llega aquí, significa que la inscripción fue exitosa y se sale del bucle

input("Press Enter to close...")
driver.quit()
