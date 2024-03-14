from selenium import webdriver
from mongo import sony_collection
import json

from sony.scraper import scrape_sony_preview, scrape_cameras_specs

driver = webdriver.Chrome()
driver.maximize_window()

cameras = []
cameras_preview = scrape_sony_preview(driver)
cameras.extend(cameras_preview)
for camera in cameras:
    camera['specs'] = scrape_cameras_specs(camera['detailed_link'], driver)
driver.quit()


def save_data():
    """
    Saves scraped camera data to MongoDB and a JSON file.
    """
    for camera in cameras:
        with open('sony_cameras.json', 'w') as file:
            json.dump(camera, file, indent=4)
            file.write(',\n')


save_data()



