import os
from logger import setup_logger
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv

load_dotenv(".env")

logger = setup_logger("selenium automation", "app.log")

URL = "https://systmonline.tpp-uk.com"

# --- DEBUG DELAY ---
def delay():
    t = random.uniform(2, 5)
    time.sleep(t)

username = os.getenv("SYSTM_USERNAME"),
password = os.getenv("SYSTM_PASSWORD")

if not username:
    logger.error("SYSTM_USERNAME is not set")
    raise ValueError("SYSTM_USERNAME missing")

if not password:
    logger.error("SYSTM_PASSWORD is not set")
    raise ValueError("SYSTM_PASSWORD missing")

driver = None

logger.info("Starting automation...")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get(URL)
delay()

# ==== LOGIN ====
# ==== LOGIN ====
logger.info("Logging in...")

try:
    username_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "Username"))
    )
    username_input.send_keys(username)

    password_input = wait.until(
        EC.visibility_of_element_located((By.NAME, "Password"))
    )
    password_input.send_keys(password + Keys.ENTER)

    # Wait for either successful login or login error
    wait.until(
        lambda driver: (
            "/2/MainMenu" in driver.current_url
            or "Your username or password is incorrect" in driver.page_source
        )
    )

    # Check for incorrect credentials
    if "Your username or password is incorrect" in driver.page_source:
        logger.error("Login failed: Incorrect username or password.")
        raise Exception("Incorrect username or password.")

    logger.info("Login successful.")

except Exception as e:
    logger.error(f"Login process failed: {str(e)}")
    raise

delay()

if driver:
    delay()
    driver.quit()
    logger.info("Driver closed")