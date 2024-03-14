from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

LAST_PAGE_URL = 'https://electronics.sony.com/imaging/interchangeable-lens-cameras/c/all-interchangeable-lens-cameras?currentPage=2'

def wait_for_page_load(driver):
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(1)


def scroll_page_until_last_page(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom of the page
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        # Wait for new elements to load
        time.sleep(2)

        # Check if the current page is the last page
        current_url = driver.current_url
        if current_url == LAST_PAGE_URL:
            print("Reached the last page. Stopping scrolling.")
            break

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the current page but not the last page. Attempting to scroll more...")
            break  # or continue based on your requirement

        last_height = new_height