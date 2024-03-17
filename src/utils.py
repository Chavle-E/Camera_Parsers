from scraper import scrape_cameras_specs

import json

def save_data(cameras_arg):
    """
    Saves scraped camera data to a JSON file.
    """
    for camera_arg in cameras_arg:
        with open('sony_cameras.json', 'a') as json_file:
            json.dump(camera_arg, json_file, indent=4)
            json_file.write(',\n')

def get_unique_specifications(cameras, driver):
    unique_specifications = set()
    for camera in cameras:
        specifications = scrape_cameras_specs(camera['detailed_link'], driver)
        for specification in specifications:
            for specification_name in specification:
                unique_specifications.add(specification_name)
    return unique_specifications

def save_unique_specifications(cameras, driver):
    specifications = get_unique_specifications(cameras, driver)
    with open("sony_specifications.txt", "w") as f:
        for specification in specifications:
            f.write(f"{specification}\n")
