from selenium import webdriver
from mongo import sony_collection
import json

from sony.scraper import scrape_sony_preview


def save_data(cameras):
    """
    Saves scraped camera data to MongoDB and a JSON file.
    """
    with open('nikon_cameras.json', 'w') as file:
        json.dump(cameras, file, default=json.default, indent=4)

    sony_collection.insert_many(cameras)


driver = webdriver.Chrome()
driver.maximize_window()

scrape_sony_preview(driver)

# def main():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     try:
#         cameras = []
#         urls = fetch_urls()
#         try:
#             cameras_preview = scrape_sony_preview(urls, driver)
#             cameras.extend(cameras_preview)
#         except Exception as e:
#             print(f"Error scraping previews for category: {e}")
#
#         try:
#             cameras['specs'] = scrape_cameras_specs(urls, driver)
#         except Exception as e:
#             print(f"Error scraping details for camera: {e}")
#         save_data(cameras)
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()
