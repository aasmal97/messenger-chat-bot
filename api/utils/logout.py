from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.links import home_page
from utils.wait_for_element import wait_for_element


def logout(driver: webdriver.Chrome):
    driver.get(home_page)
    anchor_xpath = "//div[contains(@aria-label, 'Account Controls')][@role='navigation']//*[local-name()='svg'][contains(@aria-label, 'profile')]/ancestor::div[@role='button']"
    logout_btn_xpath = "//*[contains(text(),'Log Out')]/ancestor::div[@role='button']"

    # wait for menu anchor element
    wait_for_element(driver, anchor_xpath, "Could not find profile anchor element")
    anchor = driver.find_element(By.XPATH, anchor_xpath)
    driver.execute_script("arguments[0].click();", anchor)
    # wait for logout button
    wait_for_element(driver, logout_btn_xpath, "Could not find logout button")
    logout_btn = driver.find_element(By.XPATH, logout_btn_xpath)
    driver.execute_script("arguments[0].click();", logout_btn)
    
    return driver.quit()
