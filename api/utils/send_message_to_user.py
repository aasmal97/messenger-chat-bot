from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.wait_for_element import wait_for_element
from utils.links import messages_link


def send_message_to_user(driver: webdriver.Chrome, search_query: str, message: str, chat_option_idx: int | None):
    driver.get(messages_link)
    new_message_btn_xpath = "//a/span[contains(text(),'New Message')]"
    messages_form_xpath = "//form[@id='m-messages-touch-composer-form']"
    to_input_xpath = "//input[@data-sigil='xm-tokenizer-input']"
    message_input_xpath = "//textarea[contains(@data-sigil, 'm-textarea-input')]"
    to_input_option_xpath = "//div[@role='checkbox'][contains(@data-sigil,'recipient-option')]"
    send_btn_xpath = '//button[@type="submit][value="Send"]'
    # wait for new message button
    wait_for_element(driver, new_message_btn_xpath, "Could not find new message button")
    new_message_btn = driver.find_element(By.XPATH, new_message_btn_xpath).parent
    new_message_btn.click()
    # wait for message form
    wait_for_element(driver, messages_form_xpath, "Could not find message form")
    messages_form = driver.find_element(By.XPATH, messages_form_xpath)
    message_input = messages_form.find_element(By.XPATH, message_input_xpath)
    message_input.send_keys(message)
    # wait for to input
    wait_for_element(driver, to_input_xpath, "Could not find 'to:' input element")
    to_input = messages_form.find_element(By.XPATH, to_input_xpath)
    to_input.send_keys(search_query)
    # wait for to input options
    wait_for_element(driver, to_input_option_xpath, "Could not find 'to:' input options element")
    to_input_options = driver.find_elements(By.XPATH, to_input_option_xpath)
    if len(to_input_option_xpath) <= 0:
        return driver.quit()
    if chat_option_idx:
        to_input_options[chat_option_idx].click()
    else:
        to_input_options[0].click()
    # wait for send button
    wait_for_element(driver, send_btn_xpath, "Could not find message send button")
    send_btn = driver.find_element(By.XPATH, send_btn_xpath)
    send_btn.click()
    return driver
