from app.models.template import OCRRequest
from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

TEMPLATES_DIR = "templates"

@router.post("/process_ocr/")
async def process_ocr(request: OCRRequest):
    template_name = request.template_name
    page = request.page
    rectangles = request.rectangles
    description = request.description
    classifier = request.classifier
    value_length = request.value_length

    # Save the template data to a JSON file
    template_data = {
        "template_name": template_name,
        "page": page,
        "rectangles": rectangles,
        "description": description,
        "classifier": classifier,
        "value_length": value_length
    }

    # Ensure the templates directory exists
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)

    try:
        with open(os.path.join(TEMPLATES_DIR, f"{template_name}.json"), "w") as f:
            json.dump(template_data, f)
        return {"message": f"Template {template_name} saved successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving template: {str(e)}")
