from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.links import messages_link
from utils.wait_for_element import wait_for_element
from operator import itemgetter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ui_templates_xpath_dict = {
    "template_1": {
        "search_bar_x_path": "//input[@placeholder='Search Messenger']",
        "search_bar_submit_btn_xpath": None,
        "thread_container_xpath": "//div[@id='threadlist_rows']",
        "send_btn_xpath": '//button[@type="submit][value="Send"]',
        "message_input_xpath": "//textarea[contains(@data-sigil, 'm-textarea-input')]",
        "thread_options_xpath": "//div[@id='threadlist_rows']//a",
    },
    "template_2": {
        "search_bar_x_path": "//h3[contains(text(), 'SEARCH')]/following-sibling::form//input[@value='Search']/parent::td/preceding-sibling::td//input",
        "search_bar_submit_btn_xpath": "//h3[contains(text(), 'SEARCH')]/following-sibling::form//input[@value='Search']",
        "thread_container_xpath": "//a[contains(text(), 'Search for messages')]/parent::div/following-sibling::section",
        "send_btn_xpath": "//input[@value='Send'][@type='submit']",
        "message_input_xpath": "//textarea[@name='body']",
        "thread_options_xpath": "//a[contains(text(), 'Search for messages')]/parent::div/following-sibling::section//h3/a",
    },
}


def detect_template_used(driver: webdriver.Chrome):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, ui_templates_xpath_dict["template_2"]["search_bar_submit_btn_xpath"])
            )
        )
        return "template_2"
    except TimeoutError:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, ui_templates_xpath_dict["template_1"]["search_bar_xpath"]))
        )
        return "template_1"


def send_message_to_active_chats(
    driver: webdriver.Chrome, message: str, search_term: str, chat_option_idx: int | None = None
):
    driver.get(messages_link)
    template_used = detect_template_used(driver)
    # unpack ui template variables
    (
        search_bar_x_path,
        search_bar_submit_btn_xpath,
        thread_container_xpath,
        send_btn_xpath,
        message_input_xpath,
        thread_options_xpath,
    ) = itemgetter(
        "search_bar_x_path","search_bar_submit_btn_xpath", "thread_container_xpath", "send_btn_xpath", "message_input_xpath", "thread_options_xpath"
    )(
        ui_templates_xpath_dict[template_used]
    )
    # search for chat
    search_bar = driver.find_element(By.XPATH, search_bar_x_path)
    search_bar.send_keys(search_term)
    if search_bar_submit_btn_xpath:
        driver.find_element(By.XPATH, search_bar_submit_btn_xpath).click()
    # find active chat threads
    wait_for_element(driver, thread_container_xpath, "Could not find thread container")
    thread_options = driver.find_elements(By.XPATH, thread_options_xpath)
    thread_el = thread_options[chat_option_idx if chat_option_idx else 0]
    driver.execute_script("arguments[0].click();", thread_el)
    # send message
    wait_for_element(driver, message_input_xpath, "Could not find message input")
    message_input = driver.find_element(By.XPATH, message_input_xpath)
    message_input.send_keys(message)
    send_btn_el = driver.find_element(By.XPATH, send_btn_xpath)
    driver.execute_script("arguments[0].click();", send_btn_el)
