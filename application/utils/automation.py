import os
from typing import List, Dict
from logger import setup_logger
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from dotenv import load_dotenv

load_dotenv(".env")

# --- LOGGER ---
logger = setup_logger("selenium automation", "app.log")

URL = "https://systmonline.tpp-uk.com"

# --- DEBUG DELAY ---
def delay():
    t = random.uniform(2, 5)
    time.sleep(t)

def request_medications(medication_names: List[str], dry_run: bool = True) -> Dict:
    username = os.getenv("SYSTM_USERNAME")
    password = os.getenv("SYSTM_PASSWORD")

    if not username:
        logger.error("SYSTM_USERNAME is not set")
        raise ValueError("SYSTM_USERNAME missing")

    if not password:
        logger.error("SYSTM_PASSWORD is not set")
        raise ValueError("SYSTM_PASSWORD missing")

    driver = None

    try:
        logger.info("Starting automation...")

        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)

        driver.get(URL)
        delay()

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

        # ==== NAVIGATE ====
        logger.info("Opening medication page...")

        try:
            medication_menu = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Medication')]")
                )
            )
            medication_menu.click()

        except Exception:
            logger.error("Medication button not found.")
            raise Exception("Medication button not found.")

        delay()

        try:
            request_medication = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//form[@action='Medication']//button"
                ))
            )
            request_medication.click()

        except Exception:
            logger.error("Request medication button not found.")
            raise Exception("Request medication button not found.")

        try:
            wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//h4[contains(., 'Regular Medication')]"
                ))
            )

            logger.info("Successfully navigated to Medication page.")

        except Exception:
            logger.error("Medication page did not load.")
            raise Exception("Medication page failed to load.")

        delay()

        # ==== SELECT MEDICATION ====
        logger.info(f"Selecting medications: {medication_names}")

        selected = []

        for med in medication_names:
            try:
                logger.info(f"Looking for: {med}")

                checkbox = wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        f"//h3[contains(.,'{med}')]/ancestor::tr//input"
                    ))
                )

                delay()
                checkbox.click()

                logger.info(f"Selected: {med}")
                selected.append(med)

                delay()

            except Exception:
                logger.warning(f"Failed to select medication: {med}")

        if not selected:
            logger.error("No medications selected.")
            raise Exception("No medications selected.")

        # ==== CONTINUE ====
        try:
            continue_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Continue')]")
                )
            )

            delay()
            continue_button.click()

            # Verify confirmation page loaded
            wait.until(
                lambda d: "/2/RequestMedication" in d.current_url
            )

            logger.info("Reached medication confirmation page.")

        except Exception:
            logger.error("Failed to reach confirmation page.")
            raise Exception("Confirmation page failed to load.")

        delay()

        # ==== DRY RUN STOP ====
        if dry_run:
            logger.info(f"DRY RUN: Would request: {', '.join(selected)}")
            delay()
            return {"success": True, "message": f"Dry run successful: {selected}"}

        # ==== FINAL SUBMIT ====
        try:
            final_submit = wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and normalize-space()='Request Medication']"
                ))
            )

            delay()
            final_submit.click()

            # Wait for confirmation text after submit
            wait.until(
                lambda d: (
                    "Medication Order Summary" in d.page_source
                    and "A request was sent to the practice to prescribe"
                    in d.page_source
                )
            )

            logger.info(
                f"Medication request submitted successfully: "
                f"{', '.join(selected)}"
            )

        except Exception:
            logger.error("Medication submission confirmation not found.")
            raise Exception(
                "Medication request may not have been submitted successfully."
            )

        return {
            "success": True,
            "dry_run": False,
            "selected_medications": selected,
            "message": "Medication request submitted successfully"
        }
    
    except TimeoutException:
        logger.exception("Automation timed out")
        return {
            "success": False,
            "message": "Automation timed out"
        }

    except Exception as e:
        logger.exception("Automation failed")
        return {
            "success": False,
            "message": str(e)
        }
    
    finally:
        if driver:
            delay()
            driver.quit()
            logger.info("Driver closed")

# --- RUN TEST ---
if __name__ == "__main__":
    result = request_medications(
        [
    "Resource ThickenUp Clear powder",
    "Baclofen 10mg tablets",
    "Trazodone 150mg tablets"
],
        dry_run=True
    )
    print(result)