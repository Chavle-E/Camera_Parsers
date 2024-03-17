from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper import scrape_sony_preview, scrape_cameras_specs, scrape_camera_images
from chatgpt import generate_description
from mongo import collection

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
    camera['description'] = generate_description(camera)


driver.quit()

collection.insert_many(cameras)
