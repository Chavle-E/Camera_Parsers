from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from sony.schemas import SonyPreview
from sony.selenium_utils import wait_for_page_load, scroll_page_to_bottom

BASE_URL = 'https://electronics.sony.com'


def click_specifications(driver, ID):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ID))).click()


def click_view_more(driver, Xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath))).click()


def specs_see_more(driver):
    # Click on the "Specifications" heading to reveal the "See More" button
    click_specifications(driver, "PDPSpecificationsLink")
    # Wait for the "See More" button to become clickable after the click action above
    click_view_more(driver, "(//button[contains(text(),'See More')])[2]")

    # Return the BeautifulSoup object of the page for parsing
    return BeautifulSoup(driver.page_source, 'html.parser')


def click_picture(driver, selector):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()


def picture_parser(driver):
    driver.refresh()
    click_picture(driver, "img[width='8'][height='7']")


def scrape_sony_preview(driver):
    url = 'https://electronics.sony.com/imaging/interchangeable-lens-cameras/c/all-interchangeable-lens-cameras'
    driver.get(url)
    wait_for_page_load(driver)
    scroll_page_to_bottom(driver)
    wait_for_page_load(driver)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    camera_elements = soup.find_all('li', {'class': 'col-12 col-sm-6 col-md-6 col-lg-4'})

    validated_data = []

    for camera in camera_elements:
        price_div = camera.find('div', class_="custom-product-grid-item__price")
        camera_dict = {
            "name": camera.find('p').text.strip() if camera.find('p') else camera.find('a',
                                                                                       class_='custom-product-grid-item__info').text.strip(),
            "price": price_div.text.strip() if price_div else "Not Available",
            "detailed_link": BASE_URL + camera.find('a', class_='custom-product-grid-item__info')['href']
        }
        print(camera_dict)
        SonyPreview.parse_obj(camera_dict)
        validated_data.append(camera_dict)

    return validated_data


def scrape_cameras_specs(url, driver):
    driver.get(url)
    wait_for_page_load(driver)
    soup = specs_see_more(driver)
    full_specs = soup.find_all('div', class_="full-specifications__specifications-single-card")

    result = []
    for full_spec in full_specs:
        keys = full_spec.find_all('h4', class_='full-specifications__specifications-single-card__sub-list__name')
        values = full_spec.find_all('p', class_='full-specifications__specifications-single-card__sub-list__value')
        if len(keys) == len(values):
            for i in range(len(keys)):
                result.append([{keys[i].text.strip(): values[i].text.strip()}])

    return result


def scrape_camera_images():
    """  # Get Pictures Through Soup
        picture_div = soup.find_all('div',
                                    class_="custom-pdp-image__thumb-container custom-pdp-image__thumb-container--image")
        pic_temp = []
        for picture in picture_div:
            pic_src = picture.find('img', alt=True).get('src')
            pic_temp.append(pic_src)"""

    pass
