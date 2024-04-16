from pydantic import BaseModel
from typing import List, Dict

class OCRRequest(BaseModel):
    template_name: str
    page: int
    rectangles: List[Dict[str, int]]  # Each rectangle will now include more detailed information
    description: str
    classifier: str
    value_length: int
    field_types: Dict[str, str]  # New field to specify data types (e.g., 'date', 'number', 'text')

    # Adding validation rules for the OCR fields
    validation_rules: Dict[str, Dict[str, str]]  # e.g., {'field_name': {'regex': '...', 'min_length': 3}}
