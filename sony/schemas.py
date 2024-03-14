from pydantic import BaseModel
import json
import os


class SonyPreview(BaseModel):
    name: str
    price: str
    detailed_link: str



