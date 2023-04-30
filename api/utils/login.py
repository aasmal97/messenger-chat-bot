import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.links import login_link


def login_to_messenger(driver: webdriver.Chrome, email: str, pw: str, account_name: str | None = None):
    email_input_xpath = "//input[@name='email']"
    password_input_xpath = "//input[@name='pass']"
    login_button_xpath = "//button[@name='login']"
    driver.get(login_link)
    try:
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, email_input_xpath)))
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, password_input_xpath))
        )
        time.sleep(random.randint(1, 3))

    except TimeoutError:
        driver.quit()
        raise Exception("Could not find login fields")
    email_field = driver.find_element(By.XPATH, email_input_xpath)
    password_field = driver.find_element(By.XPATH, password_input_xpath)
    email_field.send_keys(email)
    password_field.send_keys(pw)
    login_button = driver.find_element(By.XPATH, login_button_xpath)
    login_button.click()
    try:
        one_tap_page_txt = "Log in with one tap"
        x_path_conditions = [By.XPATH,f"//*[contains(text(),'{one_tap_page_txt}')]"]
        if account_name:
            x_path_conditions.append(f"//*[contains(text(),'{account_name}')]")
        # find neccessary elements to know we are logged in
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(tuple(x_path_conditions)))
        time.sleep(random.randint(1, 3))

    except TimeoutError:
        driver.quit()
        raise Exception("Login failed")
    return driver
