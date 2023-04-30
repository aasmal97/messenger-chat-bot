from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.links import home_page
from utils.wait_for_element import wait_for_element


def logout(driver: webdriver.Chrome):
    driver.get(home_page)
    anchor_xpath = "//a[@role='button'][@name='More'][contains(@data-sigil,'menu-link icon')]"
    logout_btn_xpath = "//a[contains(@data-sigil, 'logout')]"
    # wait for menu anchor element
    wait_for_element(driver, anchor_xpath, "Could not find menu anchor element")
    anchor = driver.find_element(By.XPATH, anchor_xpath)
    driver.execute_script("arguments[0].click();", anchor)
    # wait for logout button
    wait_for_element(driver, logout_btn_xpath, "Could not find logout button")
    logout_btn = driver.find_element(By.XPATH, logout_btn_xpath)
    driver.execute_script("arguments[0].click();", logout_btn)
    
    return driver.quit()
