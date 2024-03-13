from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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
    products = []
    for url in urls:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        name = soup.find('p').text if soup.find('p') else 'Name not found'

        price_div = soup.find('div', class_='custom-product-summary__price')
        price = price_div.find('span').text if price_div and price_div.find('span') else 'Price not found'

        unordered_lists = soup.find_all('ul', class_='pdp-summary-highlights__content')[0:4]
        descriptions = [' '.join(ul.get_text(strip=True) for ul in unordered_list.find_all('li')) for unordered_list in
                        unordered_lists]
        description = ' | '.join(descriptions)
        print(description)

        products.append({'name': name, 'price': price, 'description': description})
    return products


page_url = fetch_urls()
print(parse_each_page(page_url))
driver.quit()
