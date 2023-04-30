import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def wait_for_element(driver: webdriver.Chrome, xpath: str, err_message: str):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        # add random wait time to avoid getting blocked by the bot
        time.sleep(random.randint(3, 7))
    except TimeoutError:
        driver.quit()
        return Exception(err_message)