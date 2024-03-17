from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def wait_for_page_load(driver):
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(1)


def scroll_page_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page.
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        # Wait for new elements to load.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it means we've reached the bottom.
            print("Reached the bottom of the page.")
            break

        last_height = new_height


def click_specifications(driver, ID):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ID))).click()


def click_view_more(driver, Xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath))).click()


def click_picture(driver, selector):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, selector))).click()


def specs_see_more(driver):
    # Click on the "Specifications" heading to reveal the "See More" button
    click_specifications(driver, "PDPSpecificationsLink")
    # Wait for the "See More" button to become clickable after the click action above
    click_view_more(driver, "(//button[contains(text(),'See More')])[2]")

    # Return the BeautifulSoup object of the page for parsing
    return BeautifulSoup(driver.page_source, 'html.parser')


def picture_parser(driver):
    click_picture(driver, "is-initialized")

    return BeautifulSoup(driver.page_source, 'html.parser')


def remove_duplicates_preserve_order(specs_list):
    seen_keys = set()
    deduplicated_result = []

    for spec in specs_list:
        # Assuming each dictionary has only one key-value pair
        # Extract the key from the dictionary
        key = list(spec.keys())[0]

        # If the key has not been seen, preserve this dictionary
        if key not in seen_keys:
            deduplicated_result.append(spec)
            seen_keys.add(key)

    return deduplicated_result
