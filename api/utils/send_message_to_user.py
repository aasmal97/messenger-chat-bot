from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.wait_for_element import wait_for_element
from utils.links import messages_link


def send_message_to_user(driver: webdriver.Chrome, search_term: str, message: str, chat_option_idx: int | None = None):
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
    driver.execute_script("arguments[0].click();", new_message_btn)
    # wait for message form
    wait_for_element(driver, messages_form_xpath, "Could not find message form")
    messages_form = driver.find_element(By.XPATH, messages_form_xpath)
    message_input = messages_form.find_element(By.XPATH, message_input_xpath)
    message_input.send_keys(message)
    # wait for to input
    wait_for_element(driver, to_input_xpath, "Could not find 'to:' input element")
    to_input = messages_form.find_element(By.XPATH, to_input_xpath)
    to_input.send_keys(search_term)
    # wait for to input options
    wait_for_element(driver, to_input_option_xpath, "Could not find 'to:' input options element")
    to_input_options = driver.find_elements(By.XPATH, to_input_option_xpath)
    if len(to_input_option_xpath) <= 0:
        driver.quit()
        return Exception("No users found for current search term")
    to_input_option_el = to_input_options[chat_option_idx if chat_option_idx else 0]
    driver.execute_script("arguments[0].click();", to_input_option_el)
    # wait for send button
    wait_for_element(driver, send_btn_xpath, "Could not find message send button")
    send_btn = driver.find_element(By.XPATH, send_btn_xpath)
    driver.execute_script("arguments[0].click();", send_btn)
    return driver
