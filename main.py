from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from filtering import SonyPreview

# Initialize WebDriver
driver = webdriver.Chrome()


def fetch_urls():
    url = "https://electronics.sony.com/imaging/interchangeable-lens-cameras/c/all-interchangeable-lens-cameras?currentPage=2"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".custom-product-grid-item__content")))
    camera_elements = driver.find_elements(By.CSS_SELECTOR,
                                           ".custom-product-grid-item__content a.custom-product-grid-item__info")
    urls = [element.get_attribute('href') for element in camera_elements]
    return urls


def parse_each_page(urls):
    for url in urls:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # Returns Name
        name = soup.find('p').text if soup.find('p') else 'Name not found'
        # Returns Price
        price_div = soup.find('div', class_='custom-product-summary__price')
        price = price_div.find('span').text if price_div and price_div.find('span') else 'Price not found'
        # Returns full Information about item on webpage
        desc_div = soup.find_all('div', class_='pdp-summary-highlights')
        for div in desc_div:
            unordered_lists = div.find_all('ul', class_='pdp-summary-highlights__content')
            descriptions = []
            for unordered_list in unordered_lists:
                for li in unordered_list.find_all('li'):
                    text = li.get_text(strip=True)
                    if text not in ["Check Camera to Lens Compatibility", "Check Accessory Compatibility"]:
                        descriptions.append(text)

            description = ' | '.join(descriptions)

        # Creates Pydantic class of sony camera and saves it as json file
        sony_obj = {'name': name, 'price': price, 'description': description}
        sony_instance = SonyPreview(**sony_obj)
        sony_instance.save_json()


page_url = fetch_urls()
parse_each_page(page_url)
driver.quit()
