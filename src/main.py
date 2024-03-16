from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

from scraper import scrape_sony_preview, scrape_cameras_specs, scrape_camera_images

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

cameras = []
cameras_preview = scrape_sony_preview(driver)
cameras.extend(cameras_preview)
for camera in cameras:
    camera['images'] = scrape_camera_images(camera['detailed_link'], driver)
    camera['specs'] = scrape_cameras_specs(camera['detailed_link'], driver)
driver.quit()


def save_data(cameras_arg):
    """
    Saves scraped camera data to a JSON file.
    """
    for camera_arg in cameras_arg:
        with open('sony_cameras.json', 'a') as json_file:
            json.dump(camera_arg, json_file, indent=4)
            json_file.write(',\n')


save_data(cameras)
