from pydantic import BaseModel
from typing import List

class OCRRequest(BaseModel):
    template_name: str
    page: int
    rectangles: List[List[int]]
    description: str
    classifier: str
    value_length: int
