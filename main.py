from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from dotenv import load_dotenv
import os
import time
import json


load_dotenv()

browser = os.getenv("BROWSER")
browser_path = os.getenv("BROWSER_PATH")
webdriver_path = os.getenv("WEBDRIVER_PATH")
username = os.getenv("SIRA_USERNAME")
password = os.getenv("SIRA_PASSWORD")

print(f"BROWSER: {browser}")
print(f"BROWSER_PATH: {browser_path}")
print(f"WEBDRIVER: {webdriver_path}")
print(f"USERNAME: {username}")
print(f"PASSWORD: {password}")

if not browser or not browser_path or not webdriver_path or not username or not password:
	raise ValueError("Error: BROWSER, WEBDRIVER, SIRA_USERNAME and SIRA_PASSWORD environment variables must be set")

chrome_options = Options()
if browser == "BRAVE":
	chrome_options.binary_location = browser_path
elif browser == "GOOGLE_CHROME":
	pass


service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# ---------------------------------------------------------------------------- #
#                                PLATFORM LOGIN                                #
# ---------------------------------------------------------------------------- #

driver.get("https://sira1.univalle.edu.co/sra")

try:
	alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
	alert.accept()
except NoAlertPresentException:
	print("No alert found")

try:
	user_input = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "usu_login_aut"))
	)
	password_input = driver.find_element(By.NAME, "usu_password_aut")

	user_input.send_keys(username)
	password_input.send_keys(password)
	password_input.submit()
except TimeoutException:
	print("Error: login fields not found")

try:
	alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
	alert.accept()
except NoAlertPresentException:
	print("Error: no alert found")

try:
	element = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable(
			(By.CSS_SELECTOR, "input[type='image'][title='Matrícula Académica']")
		)
	)
	element.click()
except:
	print("Error: element not found")
	driver.quit()
	exit()

# ---------------------------------------------------------------------------- #
#                             LOAD OF THE SUBJECTS                             #
# ---------------------------------------------------------------------------- #

subject_codes = []
subject_groups = []
subject_was_not_enrolled = []

with open("subjects_to_enroll.json", "r") as file:
	subjects = json.load(file)

for subject in subjects:
	subject_codes.append(subject["code"])
	subject_groups.append(subject["group"])
	subject_was_not_enrolled.append(True)

# ---------------------------------------------------------------------------- #
#                              SUBJECTS ENROLLMENT                             #
# ---------------------------------------------------------------------------- #

i = 0

while any(subject_was_not_enrolled):
	if not subject_was_not_enrolled[i]: # Already enrrolled
		i = (i + 1) % len(subject_codes)
		continue

	subject_code = subject_codes[i]
	subject_group = subject_groups[i]

	print(f"Enrolling subject with code: {subject_code} and group: {subject_group}")

	try:
		code_input = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.NAME, "asm_asi_codigo"))
		)
		group_input = driver.find_element(By.NAME, "asm_grupo")

		code_input.send_keys(subject_code)
		group_input.send_keys(subject_group)
		group_input.send_keys("\n") # Simulate an enter
	except TimeoutException:
		print("Error: enrollment field not found")

	try:
		accept_button = WebDriverWait(driver, 10).until(
			EC.element_to_be_clickable((By.NAME, "botonAceptar"))
		)
		accept_button.click()
	except TimeoutException:
		print("Error: accept button not found")

	there_was_an_error_alert = False
	try:
		alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
		alert_text = alert.text

		if not "No hay cupo para la asignatura" in alert_text:
			subject_was_not_enrolled[i] = False
		else:
			there_was_an_error_alert = True # If an error has occurred, the first alert indicates
											# the error and the second that the subject could be enrolled.

		alert.accept()
	except NoAlertPresentException:
		print("Error: no alert found")

	if there_was_an_error_alert:
		try:
			alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
			alert.accept()
		except NoAlertPresentException:
			print("Error: no alert found")

	i = (i + 1) % len(subject_codes)

	time.sleep(2)


input("Press Enter to close...")
driver.quit()
