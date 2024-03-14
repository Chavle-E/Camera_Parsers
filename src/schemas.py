from pydantic import BaseModel
from typing import List


class SonyPreview(BaseModel):
    name: str
    price: str
    category: str
    detailed_link: str


class ImageURLS(BaseModel):
    images: List[str]
