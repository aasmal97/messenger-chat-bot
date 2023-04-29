from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.links import messages_link
from utils.wait_for_element import wait_for_element


def send_message_to_active_chats(driver: webdriver.Chrome, message: str, search_term: str, optionNum: int | None):
    driver.get(messages_link)
    search_bar_x_path = "//input[@placeholder='Search Messenger']"
    thread_container_xpath = "//div[@id='threadlist_rows']"
    send_btn_xpath = '//button[@type="submit][value="Send"]'
    message_input_xpath = "//textarea[contains(@data-sigil, 'm-textarea-input')]"
    # search for chat
    search_bar = driver.find_element(By.XPATH, search_bar_x_path)
    search_bar.send_keys(search_term)
    # find active chat threads
    wait_for_element(driver, thread_container_xpath, "Could not find thread container")
    thread_container = driver.find_element(By.XPATH, thread_container_xpath)
    thread_options = thread_container.find_elements(By.XPATH, "//a")
    if optionNum:
        thread_options[optionNum].click()
    else:
        thread_options[0].click()
    # send message
    wait_for_element(driver, message_input_xpath, "Could not find message input")
    message_input = driver.find_element(By.XPATH, message_input_xpath)
    message_input.send_keys(message)
    send_btn_xpath = driver.find_element(By.XPATH, send_btn_xpath)
    send_btn_xpath.click()
