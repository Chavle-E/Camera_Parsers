import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from filtering import SonyPreview
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()


def fetch_urls():
    url = "https://electronics.sony.com/imaging/interchangeable-lens-cameras/c/all-interchangeable-lens-cameras?currentPage=2"
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "custom-product-grid-item__content")))
    camera_elements = driver.find_elements(By.CLASS_NAME,
                                           "custom-product-grid-item__content a.custom-product-grid-item__info")
    urls = [element.get_attribute('href') for element in camera_elements]
    return urls


def click_specifications(driver_arg, ID):
    WebDriverWait(driver_arg, 10).until(EC.element_to_be_clickable((By.ID, ID))).click()


def click_view_more(driver_arg, Xpath):
    WebDriverWait(driver_arg, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath))).click()


def specs_see_more(driver_arg):
    # Click on the "Specifications" heading to reveal the "See More" button
    click_specifications(driver_arg, "PDPSpecificationsLink")
    # Wait for the "See More" button to become clickable after the click action above
    click_view_more(driver_arg, "(//button[contains(text(),'See More')])[2]")

    # Return the BeautifulSoup object of the page for parsing
    return BeautifulSoup(driver_arg.page_source, 'html.parser')


def parse_each_page(urls):
    for url in urls:
        driver.get(url)
        time.sleep(3)
        soup = specs_see_more(driver)
        time.sleep(3)
        # Returns Name
        name = soup.find('p').text if soup.find('p') else 'Name not found'
        # Returns Price
        price_div = soup.find('div', class_='custom-product-summary__price')
        price = price_div.find('span').text if price_div and price_div.find('span') else 'Price not found'
        # Returns Specs for each camera
        full_specs = soup.find_all('div', class_="full-specifications__specifications-single-card")

        temp = {}
        for full_spec in full_specs:
            keys = full_spec.find_all('h4', class_='full-specifications__specifications-single-card__sub-list__name')
            values = full_spec.find_all('p', class_='full-specifications__specifications-single-card__sub-list__value')
            spec_entries = zip(keys, values)
            for key, value in spec_entries:
                temp[key.text.strip()] = value.text.strip()

        # Creates Pydantic class of sony camera and saves it as json file
        sony_obj = {'name': name, 'price': price, 'specs': temp}
        sony_instance = SonyPreview(**sony_obj)
        sony_instance.save_json()


page_url = fetch_urls()
parse_each_page(page_url)
driver.quit()
