from pydantic import BaseModel
import json
import os


class SonyPreview(BaseModel):
    name: str
    price: str
    description: str

    def save_json(self):
        file_path = 'sony/results/sony_preview.json'

        dir_name = os.path.dirname(file_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, 'a') as json_file:
            json.dump(dict(self), json_file, indent=4)
