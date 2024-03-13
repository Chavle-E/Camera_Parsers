from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

url = 'https://www.usa.canon.com/shop/cameras/mirrorless-cameras'

driver.get(url)


def wait_for_page_load():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))


def click_load_more():
    try:
        # Wait for the "Load More" button to be clickable
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="amasty-shopby-product-list"]/button')))
        driver.execute_script("arguments[0].click();", load_more_button)

        time.sleep(5)
    except Exception as e:
        print(f"Error clicking 'Load More': {e}")


wait_for_page_load()
click_load_more()

page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')
filter_links = soup.find_all('h2', class_="product name product-item-name")
for link in filter_links:
    url = link.find('a', class_="product-item-link")
    print(url.get('href'))


driver.quit()
